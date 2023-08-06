#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import with_statement, print_function
import argparse
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import math
import numpy as np
import pandas as pd
import os
from natf.mesh import Mesh
from natf.source_particle import SourceParticle
from natf.cell import Cell, get_cell_index, is_item_cell
from natf.material import Material, create_pseudo_mat, get_material_index
from natf.part import Part, get_part_index, get_part_index_by_name, \
    get_part_index_by_cell_id, is_cell_id_in_parts, is_item_part
from natf.radwaste_standard import RadwasteStandard, rwc_to_int, ctr_to_int
from natf.utils import sgn, cooling_time_sec, format_single_output, str2float, \
    scale_list, is_blank_line, log, get_energy_group, is_close, is_float
from natf.mcnp_input import is_comment, get_cell_cid_mid_den, is_cell_title, \
    cell_title_change_mat
from natf.mcnp_output import get_cell_neutron_flux, get_cell_names_from_line, \
    get_cell_vol_mass, get_cell_tally_info, get_cell_vols_from_line, \
    is_cell_info_start, get_cell_icl_cellid_matid_matdensity, get_cell_basic_info
from natf.plot import get_rwcs_by_cooling_times, calc_rwc_cooling_requirement, \
    calc_recycle_cooling_requirement
from natf.fispact_output import get_fispact_out_line_info, read_fispact_out_act, \
    get_interval_from_line, found_interval_line, is_interval_in_line, \
    read_fispact_out_sdr, read_fispact_out_dpa, get_interval_list


@log
def check_input(filename="input"):
    """Read the 'input' file and check the variables.
    if the required variable is not given, this function will give error
    message."""

    config = ConfigParser.ConfigParser()
    config.read(filename)
    # general
    WORK_DIR = config.get('general', 'WORK_DIR')
    AIM = config.get('general', 'AIM')
    # check the input variables
    AIMS = (
        'CELL_ACT_PRE', 'CELL_ACT_POST', 'CELL_DPA_PRE', 'CELL_DPA_POST',
        'COOLANT_ACT_PRE', 'COOLANT_ACT_POST', 'CELL_RWC_VIS')
    if AIM not in AIMS:  # check AIM validate
        raise ValueError(f"AIM: {AIM} not supported")

    # mcnp
    MCNP_INPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_INPUT'))
    MCNP_OUTPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_OUTPUT'))
    try:
        CONTINUE_OUTPUT = config.get('mcnp', 'CONTINUE_OUTPUT')
        if CONTINUE_OUTPUT != '':
            CONTINUE_OUTPUT = os.path.join(
                WORK_DIR, config.get('mcnp', 'CONTINUE_OUTPUT'))
    except:
        CONTINUE_OUTPUT = None

    # mcnp.n_group_size
    N_GROUP_SIZE = config.getint('mcnp', 'N_GROUP_SIZE')
    if N_GROUP_SIZE not in (69, 175, 315, 709):
        raise ValueError('N_GROUP_SIZE must be 69, 175, 315 or 709')

    # mcnp.tally_number
    TALLY_NUMBER = get_tally_number(config)
    if AIM in ['CELL_DPA_PRE', 'CELL_DPA_POST'] and N_GROUP_SIZE != 709:
        raise ValueError(
            'N_GROUP_SIZE only support 709 if you want to calculate DPA')

    # coolant_flow, available only for COOLANT_ACT mode
    if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
        # coolant_flow.coolant_flow_parameters, required in COOLANT_ACT mode
        COOLANT_FLOW_PARAMETERS = os.path.join(WORK_DIR,
                                               config.get('coolant_flow', 'COOLANT_FLOW_PARAMETERS'))
        if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST'] and COOLANT_FLOW_PARAMETERS is None:
            raise ValueError(
                "COOLANT_FLOW_PARAMETERS must be provided in COOLANT_ACT mode")
        # coolant_flow.flux_multiplier, required in COOLANT_ACT mode
        FLUX_MULTIPLIER = float(config.get('coolant_flow', 'FLUX_MULTIPLIER'))
        if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST'] and FLUX_MULTIPLIER is None:
            raise ValueError(
                "FLUX_MULTIPLIER must be provided in COOLANT_ACT mode")

    # fispact
    # fispact.fispact_material_list, optional
    try:
        FISPACT_MATERIAL_LIST = config.get('fispact', 'FISPACT_MATERIAL_LIST')
        if FISPACT_MATERIAL_LIST != '':
            FISACT_MATERIAL_LIST = os.path.join(
                WORK_DIR, FISPACT_MATERIAL_LIST)
    except:
        FISPACT_MATERIAS_LIST = ''
    # fispact.irradiation_scenario, required in CELL_ACT and CELL_DPA mode
    IRRADIATION_SCENARIO = config.get('fispact', 'IRRADIATION_SCENARIO')
    if AIM in ['CELL_ACT_PRE', 'CELL_ACT_POST', 'CELL_DPA_PRE', 'CELL_DPA_POST']:
        if IRRADIATION_SCENARIO == '':
            raise ValueError(
                "IRRADIATION_SCENARIO must be provided in CELL_ACT and CELL_DPA mode")
    if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
        if IRRADIATION_SCENARIO != '':
            raise ValueError(
                "IRRADIATION_SCENARIO is not required in COOLANT_ACT mode")
    IRRADIATION_SCENARIO = os.path.join(
        WORK_DIR, config.get('fispact', 'IRRADIATION_SCENARIO'))
    # fispact.nuc_treatment, optional
    try:
        NUC_TREATMENT = config.get('fispact', 'NUC_TREATMENT')
        if NUC_TREATMENT != '':
            NUC_TREATMENT = os.path.join(WORK_DIR, NUC_TREATMENT)
    except:
        NUC_TREATMENT = ''
    # fispact.fispact_files_dir, optional
    FISPACT_FILES_DIR = ''
    try:
        FISPACT_FILES_DIR = config.get('fispact', 'FISPACT_FILES_DIR')
        if FISPACT_FILES_DIR != '':
            FISPACT_FILES_DIR = os.path.join(WORK_DIR, FISPACT_FILES_DIR)
            os.system(f'mkdir -pv {FISPACT_FILES_DIR}')
    except:
        pass

    # model, required
    PART_CELL_LIST = os.path.join(WORK_DIR,
                                  config.get('model', 'PART_CELL_LIST'))
    # model.model_degree, optional
    try:
        MODEL_DEGREE = float(config.get('model', 'MODEL_DEGREE'))
        if MODEL_DEGREE < 0.0 or MODEL_DEGREE > 360.0:
            raise ValueError('MODEL_DEGREE must between 0 ~ 360')
    except:
        MODEL_DEGREE = 360.0

    # [radwaste] standard
    try:
        RADWASTE_STANDARDS = config.get(
            'radwaste', 'RADWASTE_STANDARDS').split(',')
        for rws in RADWASTE_STANDARDS:
            if rws not in ['', 'CHN2018', 'UK', 'USNRC', 'USNRC_FETTER', 'RUSSIAN']:
                raise ValueError(f"Radwaste standard: {rws} not supported!")
    except:
        pass

    return True


@log
def get_cooling_times(IRRADIATION_SCENARIO, AIM):
    """Read the irradiation_scenario, return cooling_time[]
        report error if the irradiation_scenario not fit the need of the AIM (CELL_DPA).
        CELL_DPA requirement: 1. only one pluse allowed, and this must be the FULL POWER YEAR, 1 year
                              2. no cooling time allowed."""
    # check the IRRADIATiON_SCENARIO file
    errormessage = ''.join(['IRRADIATION_SCENARIO ERROR:\n',
                            '1. Only one pulse allowed, and it must be a FPY (1 YEARS).\n',
                            '2. No cooling time allowed.'])
    # check there is only one Pulse in the content
    if AIM in ('CELL_DPA_PRE', 'CELL_DPA_POST'):
        fin = open(IRRADIATION_SCENARIO)
        time_count = 0
        for line in fin:
            line_ele = line.split()
            if line_ele == 0:  # end of the file
                continue
            if line[0] == '<' and line[1] == '<':  # this is a comment line
                continue
            if 'TIME' in line:  # this is the time information line
                time_count += 1
                if ' 1 ' not in line or ' YEARS ' not in line:  # error
                    raise ValueError(errormessage)
        fin.close()
        if time_count != 1:  # error
            raise ValueError(errormessage)

    cooling_time = []
    fin = open(IRRADIATION_SCENARIO)
    zero_flag = False
    for line in fin:
        line_ele = line.split()
        if len(line_ele) == 0:  # this is a empty line
            continue
        if line[0] == '<' and line[1] == '<':  # this is a comment line
            continue
        if 'ZERO' in line:
            zero_flag = True
            continue
        if 'TIME' in line and zero_flag:  # this is a information about the cooling time
            cooling_time.append(
                cooling_time_sec(float(line_ele[1]), line_ele[2]))
    fin.close()
    return cooling_time


def get_cooling_times_cul(cooling_times):
    """Calculate the culmulated cooling times."""
    cooling_times_cul = [0.0]*len(cooling_times)
    for i in range(len(cooling_times)):
        cooling_times_cul[i] = cooling_times_cul[i-1] + cooling_times[i]
    return cooling_times_cul


@log
def get_fispact_material_list(FISPACT_MATERIAL_LIST, AIM=None):
    """get_fispact_material_list: read the FISPACT_MATERIAL_LIST file to get the link of
    return the fispact_material_list (of int) and fispact_material_path (of string)
    Where the fispact_material_list contains the material id
              fispact_material_path contains the material file in fispact format"""

    fispact_material_list = []
    fispact_material_path = []
    # check for the input
    if FISPACT_MATERIAL_LIST == '':
        fispact_material_list, fispact_material_path = [], []
    else:
        # read the FISPACT_MATERIAL_LIST to get the information
        fin = open(FISPACT_MATERIAL_LIST)
        try:
            for line in fin:
                line_ele = line.split()
                # is this line a comment line?
                if line_ele[0] in ['c', 'C']:
                    pass
                else:
                    material_path = line_ele[0]
                    if material_path in fispact_material_path:
                        errormessage = ''.join(
                            ['material path:', material_path, ' defined more than once in FISPACT_MATERIAL_LIST\n'])
                        raise ValueError(errormessage)
                    else:
                        fispact_material_path.append(material_path)
                        if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
                            # part name supports explicit define only
                            fispact_material_list.append(line_ele[1:])
                        else:
                            fispact_material_list.append(
                                get_cell_ids(line_ele[1:]))
        except BaseException:
            errormessage = ''.join(
                ['Error produced when reading FISPACT_MATERIAL_LIST'])
            print(errormessage)
    check_material_list(fispact_material_list, AIM=AIM)
    return fispact_material_list, fispact_material_path


@log
def get_mesh_structure(MCNP_MESHTAL, MESH_GEOM, MESH_VEC, TALLY_NUMBER):
    """get_mesh_structure: read the meshtal to get the mesh structure.
    input parameters: MCNP_MESHTAL, the file path of the meshtal file,
                      MESH_GEOM, the geom of the mesh
                      MESH_VEC, the vector of the cyl mesh
                      TALLY_NUMBER, define which tally to read
    return value:mesh_boundaries, a tuple of 3 lists that contains the
                 boundaries of 3 directions if MESH_GEOM is xyz
                 mesh_boundaries, a tuple of 6 lists that contains the
                 boundaries of 3 direction and the origin, axs and vec if
                 the MESH_GEOM is cyl"""

    # input parameter check
    if MCNP_MESHTAL == '' or MESH_GEOM == '':
        raise ValueError('MCNP_MESHTAL and MESH_GEOM must be given!')
    # open meshtal file
    fin = open(MCNP_MESHTAL)
    if MESH_GEOM == 'xyz':
        x_boundary = []
        y_boundary = []
        z_boundary = []
        while True:
            line = fin.readline()
            if 'Mesh Tally Number' in line and str(
                    TALLY_NUMBER) in line:  # find the the given tally part
                while True:
                    line = fin.readline()
                    line_ele = line.split()
                    if 'X direction' in line:
                        x_boundary.extend(map(float, line_ele[2:]))
                    if 'Y direction' in line:
                        y_boundary.extend(map(float, line_ele[2:]))
                    if 'Z direction' in line:
                        z_boundary.extend(map(float, line_ele[2:]))
                    if 'R direction' in line:
                        raise ValueError(
                            'MESH_GEOM is xyz, but there are cyl mesh in meshtal!')
                    if 'Energy' in line:
                        break
                break
        mesh_boundary = (x_boundary, y_boundary, z_boundary)
    if MESH_GEOM == 'cyl':
        r_boundary = []
        z_boundary = []
        t_boundary = []
        origin = []
        axs = []
        while True:
            line = fin.readline()
            if 'Mesh Tally Number' in line and str(
                    TALLY_NUMBER) in line:  # find the the given tally part
                while True:
                    line = fin.readline()
                    line_ele = line.split()
                    if 'X direction' in line:
                        raise ValueError(
                            'MESH_GEOM is cyl, but there are xyz mesh in meshtal!')
                    if 'R direction' in line:
                        r_boundary.extend(map(float, line_ele[2:]))
                    if 'Z direction' in line:
                        z_boundary.extend(map(float, line_ele[2:]))
                    if 'Theta direction' in line:
                        t_boundary.extend(map(float, line_ele[3:]))
                    if 'Cylinder origin at' in line:
                        origin.extend(map(float, line_ele[3:5]))
                        origin.append(float(line_ele[5][:-1]))
                        axs.extend(map(int, map(float, line_ele[8:11])))
                    if 'Energy' in line:
                        break
                break
        mesh_boundary = (
            r_boundary,
            z_boundary,
            t_boundary,
            origin,
            axs,
            MESH_VEC)

    fin.close()
    return mesh_boundary


@log
def init_meshs(mesh_structure):
    """initial meshs according to the mesh_structure.
    input parameter: mesh_structure, a tuple of 3 or 6 lists.
    if geom is xyz, (tuple 3 lists), then set geom, id, xmin, xmax, ymin, ymax, zmin,, zmax, vol of the meshs;
     if geom is cyl, (tuple 6 lists), then set the geom, id, rmin,rmax, zmin, zmax, tmin, tmax,
                                                        origin, axs, vec of the meshs
     return a list of meshs : Meshes"""
    Meshes = []
    I = len(mesh_structure[0]) - 1
    J = len(mesh_structure[1]) - 1
    K = len(mesh_structure[2]) - 1
    if len(mesh_structure) == 3:  # geom is xyz
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    temp_mesh = Mesh()
                    temp_mesh.geom = 'xyz'
                    temp_mesh.id = k + K * j + K * J * i
                    temp_mesh.xmin = mesh_structure[0][i]
                    temp_mesh.xmax = mesh_structure[0][i + 1]
                    temp_mesh.ymin = mesh_structure[1][j]
                    temp_mesh.ymax = mesh_structure[1][j + 1]
                    temp_mesh.zmin = mesh_structure[2][k]
                    temp_mesh.zmax = mesh_structure[2][k + 1]
                    temp_mesh.cal_vol()
                    Meshes.append(temp_mesh)
    if len(mesh_structure) == 6:  # geom is cyl
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    temp_mesh = Mesh()
                    temp_mesh.geom = 'cyl'
                    temp_mesh.id = k + K * j + K * J * i
                    temp_mesh.rmin = mesh_structure[0][i]
                    temp_mesh.rmax = mesh_structure[0][i + 1]
                    temp_mesh.zmin = mesh_structure[1][j]
                    temp_mesh.zmax = mesh_structure[1][j + 1]
                    temp_mesh.tmin = mesh_structure[2][k]
                    temp_mesh.tmax = mesh_structure[2][k + 1]
                    temp_mesh.cal_vol()
                    Meshes.append(temp_mesh)
    return Meshes


def cal_pos(value, boundary):
    """cal_pos, calculate the position of a value in the boundary
    input parameter: value, a float number represents xxx, yyy or zzz
    input parameter: boundary, a list of float represents the boundary
    return: pos, a int number"""

    # value check
    pos = -1
    if value < min(boundary) or value > max(
            boundary):  # particle out of the range of mesh
        return -1
    for i in range(len(boundary) - 1):
        if i == 0:  # speacial treat for the first boundary
            if boundary[i] <= value <= boundary[i + 1]:
                pos = i
        else:
            if boundary[i] < value <= boundary[i + 1]:
                pos = i
    if pos == -1:  # check the value
        raise RuntimeError('pos mus be changed in cal_pos')
    return pos


def cal_rzt(s, mesh_structure):
    """cal_rzt, calculate the r, z, t value according to the xxx,yyy,zzz of a source and mesh_sturcture
    input parameter: s, a source particle
    input parameter: mesh_structure, a tuple contains mesh structure information
    return: r, z, t, three int number"""
    r, z, t = -1, -1, -1  # initial three number, used to check whether thay are changed
    origin = list(mesh_structure[3])
    axs = list(mesh_structure[4])
    vec = list(mesh_structure[5])
    x_d = s.xxx - origin[0]
    y_d = s.yyy - origin[1]
    z_d = s.zzz - origin[2]
    if axs == [0, 0, 1]:  # axs is 0 0 1
        r = math.sqrt(x_d ** 2 + y_d ** 2)
        z = s.zzz - origin[2]
        if vec == [1, 0, 0]:  # vec is 1 0 0
            t = (1 - sgn(y_d)) // 2 + (sgn(y_d) *
                                       (math.acos(x_d / r))) / (2 * math.pi)
        if vec == [0, 1, 0]:  # vec is 0 1 0
            t = (1 - sgn(-x_d)) // 2 + (sgn(-x_d)
                                        * (math.acos(y_d / r))) / (2 * math.pi)
    if axs == [1, 0, 0]:  # axs is 1 0 0
        r = math.sqrt(y_d ** 2 + z_d ** 2)
        z = s.xxx - origin[0]
        if vec == [0, 1, 0]:  # vec is 0 1 0
            t = (1 - sgn(z_d)) // 2 + (sgn(z_d) *
                                       (math.acos(y_d / r))) / (2 * math.pi)
        if vec == [0, 0, 1]:
            t = (1 - sgn(-y_d)) // 2 + (sgn(-y_d)
                                        * (math.acos(z_d / r))) / (2 * math.pi)
    if axs == [0, 1, 0]:  # axs is 0 1 0
        r = math.sqrt(x_d ** 2 + z_d * 2)
        z = s.yyy - origin[1]
        if vec == [1, 0, 0]:
            t = (1 - sgn(z_d)) // 2 + (sgn(z_d) *
                                       (math.acos(x_d / r))) / (2 * math.pi)
        if vec == [0, 0, 1]:
            t = (1 - sgn(-x_d)) // 2 + (sgn(-x_d)
                                        * (math.acos(z_d / r))) / (2 * math.pi)
    if r == -1 or z == -1 or t == -1:  # check r, z, t value
        raise RuntimeError('r, z, t of must be changed in  cal_rzt!')
    return r, z, t


def cal_mesh_id(s, mesh_structure):
    """cal_mesh_id, calculate the mesh_id of a source particle according to the mesh_structre
    input parameter: s, a source particle
    input parameter: mesh_structre, a tuple of mesh geomtry and boundaries
    return: mid, a int of mesh_id"""

    I = len(mesh_structure[0]) - 1
    J = len(mesh_structure[1]) - 1
    K = len(mesh_structure[2]) - 1
    mid = -1

    if len(mesh_structure) == 3:  # the mesh geom is xyz
        i = cal_pos(s.xxx, mesh_structure[0])
        j = cal_pos(s.yyy, mesh_structure[1])
        k = cal_pos(s.zzz, mesh_structure[2])
        if i == -1 or j == -1 or k == -1:  # they may particle out of mesh
            return -1
        mid = k + K * j + K * J * i
    if len(mesh_structure) == 6:  # the mesh geom is cyl
        r, z, t = cal_rzt(s, mesh_structure)
        i = cal_pos(r, mesh_structure[0])
        j = cal_pos(z, mesh_structure[1])
        k = cal_pos(t, mesh_structure[2])
        if i == -1 or j == -1 or k == -1:
            return -1
        mid = k + K * j + K * J * i

    if mid == -1:  # check the value
        raise RuntimeError('mid must be changed in cal_mesh_id')
    return mid


def get_mesh_id(value, mesh_structure):
    """get_mesh_id, calculate the mesh_id according to the x,y,z or r,z,t"""
    I = len(mesh_structure[0]) - 1
    J = len(mesh_structure[1]) - 1
    K = len(mesh_structure[2]) - 1
    mesh_id = -1
    i = cal_pos(value[0], mesh_structure[0])
    j = cal_pos(value[1], mesh_structure[1])
    k = cal_pos(value[2], mesh_structure[2])
    if i == -1 or j == -1 or k == -1:  # they may particle out of mesh
        raise ValueError('the positon not in any mesh, there must be error')
    mesh_id = k + K * j + K * J * i
    return mesh_id


@log
def match_source_particles_match(Source_Particles, Meshes, mesh_structure):
    """match_source_particles_match
    funciton: put the source partiles into meshes
    input parameters: Source_Particles, a list of SourceParticle
    input parameters: Meshes, a list of Mesh
    input parameters: mesh_structure, a tuple of mesh geometry and boundaries
    return: Source_Particles, Meshes edited"""

    count_s_m = 0
    count_s_n_m = 0
    for s in Source_Particles:
        mid = cal_mesh_id(s, mesh_structure)
        if mid == -1:  # this particle doesn't in any mesh
            count_s_n_m += 1
            continue
        if mid != -1:
            count_s_m += 1
            s.mesh_id = mid
    print('    Particles in meshes: {0}; Particles not in meshes: {1}'.format(
        count_s_m, count_s_n_m))

    # calculate the mesh_cell_list
    for m in Meshes:
        cell_list = []
        cell_counts = []
        mat_list = []
        mat_counts = []
        for s in Source_Particles:
            if s.mesh_id == m.mesh_id:
                cell_list.append(s.cell_id)
                mat_list.append(s.mid)
        cell_set = set(cell_list)
        mat_set = set(mat_list)
        for item in cell_set:
            cell_counts.append(cell_list.count(item))
        for item in mat_set:
            mat_counts.append(mat_list.count(item))
        m.mesh_cell_list = list(cell_set)
        m.mesh_cell_counts = cell_counts
        m.mesh_mat_list = list(mat_set)
        m.mesh_mat_counts = mat_counts
        for i in range(len(m.mesh_cell_list)):
            m.mesh_cell_vol_fraction.append(
                float(m.mesh_cell_counts[i]) / sum(m.mesh_cell_counts))
        for i in range(len(m.mesh_mat_list)):
            m.mesh_mat_vol_fraction.append(
                float(m.mesh_mat_counts[i]) / sum(m.mesh_mat_counts))
        # calculate the mesh packing factor
        if 0 in m.mesh_mat_list:
            m.packing_factor = 1.0 - \
                float(m.mesh_mat_counts[m.mesh_mat_list.index(
                    0)]) / sum(m.mesh_mat_counts)

    # check the counts of the meshes
    bad_mesh_counts = 0
    for m in Meshes:
        if sum(m.mesh_cell_counts) < 100:
            bad_mesh_counts += 1
    if float(bad_mesh_counts) / len(Meshes) > 0.05:
        raise ValueError(
            'bad sample meshes larger than 5%, please enlarge the ptrac nps')

    return Source_Particles, Meshes


@log
def get_material_info(MCNP_OUTPUT):
    """get_material_info, read the MCNP_OUTPUT file and returns the materials"""

    materials = []
    # read the MCNP_OUTPUT first time to get the numbers of material
    mat_list = []
    fin = open(MCNP_OUTPUT)
    while True:
        line = fin.readline()
        if line == '':
            raise ValueError('1cells not found in the file, wrong file!')
        if '1cells' in line:  # read 1cells
            # read the following line
            line = fin.readline()
            line = fin.readline()
            line = fin.readline()
            line = fin.readline()
            while True:
                line = fin.readline()
                if ' total' in line:  # end of the cell information part
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                mid, atom_density, gram_density = int(
                    line_ele[2]), float(
                    line_ele[3]), float(
                    line_ele[4])
                mat_list.append((mid, atom_density, gram_density))
            break
    fin.close()
    mat_list = list(set(mat_list))

    # initial the materials
    for i in range(len(mat_list)):
        m = Material()
        m.id = mat_list[i][0]
        m.atom_density = mat_list[i][1]
        m.density = mat_list[i][2]
        materials.append(m)

    # get the nuclide of the mcnp material
    fin = open(MCNP_OUTPUT)
    mid = -1
    nuc_list = []
    atom_fraction_list = []
    while True:
        line = fin.readline()
        if 'component nuclide, atom fraction' in line:  # read atom fraction
            # read the following line
            line = fin.readline()
            mat_flag = False
            while True:
                line = fin.readline()
                if 'material' in line:  # end of the material atom fraction part
                    midx = get_material_index(materials, mid)
                    materials[midx].mcnp_material_nuclide = list(nuc_list)
                    materials[midx].mcnp_material_atom_fraction = scale_list(
                        atom_fraction_list)
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                if len(line_ele) % 2 == 1:  # this line contains material id
                    if mat_flag:
                        midx = get_material_index(materials, mid)
                        materials[midx].mcnp_material_nuclide = list(
                            nuc_list)
                        materials[midx].mcnp_material_atom_fraction = scale_list(
                            atom_fraction_list)
                        nuc_list = []  # reset
                        atom_fraction_list = []  # reset
                    mid = int(line_ele[0])
                    mat_flag = True
                    for i in range(len(line_ele) // 2):
                        nuc, atom_fraction = line_ele[2 * i +
                                                      1][:-1], float(line_ele[2 * i + 2])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            atom_fraction_list.append(atom_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            atom_fraction_list[nuc_index] += atom_fraction
                if len(line_ele) % 2 == 0:
                    for i in range(len(line_ele) // 2):
                        nuc, atom_fraction = line_ele[2 *
                                                      i][:-1], float(line_ele[2 * i + 1])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            atom_fraction_list.append(atom_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            atom_fraction_list[nuc_index] += atom_fraction
            break
    fin.close()

    # get the mass fraction of the nuclide
    fin = open(MCNP_OUTPUT)
    mid = -1
    nuc_list = []
    mass_fraction_list = []
    while True:
        line = fin.readline()
        if 'component nuclide, mass fraction' in line:  # read mass fraction
            # read the following line
            line = fin.readline()
            mat_flag = False
            while True:
                line = fin.readline()
                if ' warning.' in line or '1cell' in line:  # end of the material atom fraction part
                    midx = get_material_index(materials, mid)
                    materials[midx].mcnp_material_nuclide = list(nuc_list)
                    materials[midx].mcnp_material_mass_fraction = scale_list(
                        mass_fraction_list)
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                if len(line_ele) % 2 == 1:  # this line contains material id
                    if mat_flag:
                        midx = get_material_index(materials, mid)
                        materials[midx].mcnp_material_nuclide = list(
                            nuc_list)
                        materials[midx].mcnp_material_mass_fraction = scale_list(
                            mass_fraction_list)
                        nuc_list = []  # reset
                        mass_fraction_list = []  # reset
                    mid = int(line_ele[0])
                    mat_flag = True
                    for i in range(len(line_ele) // 2):
                        nuc, mass_fraction = line_ele[2 * i +
                                                      1][:-1], float(line_ele[2 * i + 2])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            mass_fraction_list.append(mass_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            mass_fraction_list[nuc_index] += mass_fraction
                if len(line_ele) % 2 == 0:
                    for i in range(len(line_ele) // 2):
                        nuc, mass_fraction = line_ele[2 *
                                                      i][:-1], float(line_ele[2 * i + 1])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            mass_fraction_list.append(mass_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            mass_fraction_list[nuc_index] += mass_fraction
            break
    fin.close()
    return materials


@log
def convert_material_mcnp_to_fispact(materials):
    """convert_material_mcnp_to_fispact: convert the mcnp material to FISPACT material"""
    for m in materials:
        m.mat_mcnp2fispact()
    return materials


@log
def match_cells_materials(cells, materials):
    """match the cells and materials"""
    for c in cells:
        mid = get_material_index(materials, c.mid)
        c.mat = materials[mid]
    return cells


def cal_mesh_material_list(m, materials):
    """cal_material_list: calculate the materials for a specific mesh
    input:m, a mesh
    input:materials, the list of all the materials
    return: materials_list, a list a materials in the given mesh"""
    material_list = []
    for i in range(len(m.mesh_mat_list)):
        midx = get_material_index(materials, m.mesh_mat_list[i])
        material_list.append(materials[midx])
    return material_list


def mix_mesh_material(m, material_list):
    """mix_mesh_material: calculate the mixture material of the mesh
    input:m, the mesh
    input:materials_list, a list of the materials
    return: mesh_mat, a Material represent the material of given mesh"""

    mesh_mat = Material()  # initial a material
    density = 0.0
    atom_density = 0.0
    mcnp_material_nuclide = []
    mcnp_material_atom_fraction = []
    mcnp_material_mass_fraction = []

    for i in range(len(m.mesh_mat_list)):  # fill the material
        density += material_list[i].density * m.mesh_mat_vol_fraction[i]
        atom_density += material_list[i].atom_density * \
            m.mesh_mat_vol_fraction[i]
    mesh_mat.density, mesh_mat.atom_density = density, atom_density

    # calculate the mcnp nuclide information
    for i in range(len(m.mesh_mat_list)):
        mat = material_list[i]
        fraction = m.mesh_mat_vol_fraction[i]
        for j in range(len(mat.mcnp_material_nuclide)):
            # in the list, then add the nuc data
            if mat.mcnp_material_nuclide[j] in mcnp_material_nuclide:
                # get the index of the nuc in the nuc_list
                nidx = mcnp_material_nuclide.index(
                    mat.mcnp_material_nuclide[j])
                mcnp_material_atom_fraction[nidx] += mat.mcnp_material_atom_fraction[j] * fraction
                mcnp_material_mass_fraction[nidx] += mat.mcnp_material_mass_fraction[j] * fraction
            # not in the list, add it into the list
            if mat.mcnp_material_nuclide[j] not in mcnp_material_nuclide:
                mcnp_material_nuclide.append(
                    mat.mcnp_material_nuclide[j])  # add it into list
                # get the index of the nuc in the nuc_list
                nidx = mcnp_material_nuclide.index(
                    mat.mcnp_material_nuclide[j])
                mcnp_material_atom_fraction.append(
                    mat.mcnp_material_atom_fraction[j] * fraction)
                mcnp_material_mass_fraction.append(
                    mat.mcnp_material_mass_fraction[j] * fraction)
    mesh_mat.mcnp_material_nuclide = mcnp_material_nuclide
    mesh_mat.mcnp_material_atom_fraction = scale_list(
        mcnp_material_atom_fraction)
    mesh_mat.mcnp_material_mass_fraction = scale_list(
        mcnp_material_mass_fraction)
    # convert it into fispact format
    mesh_mat.mat_mcnp2fispact()
    return mesh_mat


@log
def cal_mesh_material(Meshes, materials):
    """cal_mesh_material: calculate the mesh material according to the Meshes, cells, and materials"""
    for m in Meshes:
        material_list = cal_mesh_material_list(
            m, materials)  # make a materials list for this mesh
        m.mat = mix_mesh_material(m, material_list)
    return Meshes


def get_energy_index(energy, energy_group):
    """return energy index according to the energy and energy_group"""
    e_index = -1
    if energy == 'Total':
        return len(energy_group)
    else:
        energy = float(energy)
    for i in range(len(energy_group)):
        if abs(energy - energy_group[i]) / energy_group[i] < 1e-3:
            e_index = i
    if e_index == -1:
        raise ValueError(
            'energy not found in the energy group! Only 175/709 group supported!')
    return e_index


@log
def get_mesh_neutron_flux(
        Meshes,
        MCNP_MESHTAL,
        TALLY_NUMBER,
        mesh_structure,
        N_GROUP_SIZE):
    """get_mesh_neutron_flux: get the neutron flux according to the meshtal"""
    fin = open(MCNP_MESHTAL)
    data = []
    while True:
        line = fin.readline()
        if line == '':
            raise ValueError(
                'Mesh Tally Number %s not found in the file, wrong file!',
                str(TALLY_NUMBER))
        if 'Mesh Tally Number' in line and str(
                TALLY_NUMBER) in line:  # find the the given tally part
            while True:
                line = fin.readline()
                if 'Energy' in line and 'Result' in line and 'Rel Error' in line:  # read
                    while True:
                        line = fin.readline()
                        line_ele = line.split()
                        if len(line_ele) == 0:
                            break
                        data.append(line_ele)  # put all the data into the
                    break
            break
    # initial a empty list to store the neutron flux and error data
    neutron_flux, neutron_flux_error = [], []
    for i in range(len(Meshes)):
        neutron_flux.append([])
        neutron_flux_error.append([])
        for j in range(N_GROUP_SIZE + 1):
            neutron_flux[i].append(-1.0)
            neutron_flux_error[i].append(-1.0)
    # put data of each line into nuetron flux and error
    for item in data:
        energy, x, y, z, result, error = item[0], float(
            item[1]), float(
            item[2]), float(
            item[3]), float(
                item[4]), float(
            item[5])
        e_index = get_energy_index(energy, get_energy_group(175))
        mesh_id = get_mesh_id([x, y, z], mesh_structure)
        neutron_flux[mesh_id][e_index] = result
        neutron_flux_error[mesh_id][e_index] = error
    # treat the total neutron flux in case of version 1.2
    for i in range(len(neutron_flux)):
        if neutron_flux[i][-1] < 0.0:
            neutron_flux[i][-1] = sum(neutron_flux[i][:-1])
            neutron_flux_error[i][-1] = sum(neutron_flux_error[i]
                                            [:-1]) / N_GROUP_SIZE
    # put the neutron flux and error data into Meshes
    for i in range(len(Meshes)):
        Meshes[i].neutron_flux = list(neutron_flux[i])
        Meshes[i].neutron_flux_error = list(neutron_flux_error[i])
    fin.close()
    return Meshes


def write_fispact_file(material, IRRADIATION_SCENARIO, MODEL_DEGREE,
                       neutron_flux, file_prefix, tab4flag, endf_lib_flag,
                       fispact_material_list, fispact_material_path, AIM=None):
    """write_fispact_file: write fispact file, input .i the flux .flx files
    input: material, a Material
    input: IRRADIATION_SCENARIO, the irradiation_scenario file
    input: MODEL_DEGREE, a float number of model, this used to multiply the total neutron flux
    input: neutron_flux, neutron flux of a mesh or a cell
    input: fispact_material_list, the list of the materials that defined by user to use another one
    input: fispact_material_path, the list of the materials pathes that need to use"""

    # write the input file
    file_name = ''.join([file_prefix, '.i'])
    fo = open(file_name, 'w')
    fo.write('<< ----get nuclear data---- >>\n')
    fo.write('NOHEADER\n')
    # endf lib used? ---------
    if endf_lib_flag:
        fo.write('EAFVERSION 8\n')
        fo.write('COVAR\n')
    # ------------------------
    fo.write(' '.join(['GETXS 1', str(len(neutron_flux) - 1), '\n']))
    fo.write('GETDECAY 1\n')
    fo.write('FISPACT\n')
    fo.write('* Irradiation start\n')
    fo.write('<< ----set initial conditions---- >>\n')
    # material part start
    if AIM in ['COOLANT_ACT_PRE']:
        if any(material in sublist for sublist in fispact_material_list):
            material_path = get_material_path(fispact_material_list,
                                              fispact_material_path, material)
            fo.write(
                '<< ----material info. defined by user in the separate file below ---->>\n')
            fo.write(''.join(['<< ----', material_path, '---->>\n']))
            # read the files in fispact_material_list and write it here
            fin = open(material_path)
            for line in fin:
                if line.strip().split() == []:
                    continue
                fo.write(line)
    elif any(material.id in sublist for sublist in fispact_material_list):
        material_path = get_material_path(fispact_material_list,
                                          fispact_material_path, material.id)
        fo.write(
            '<< ----material info. defined by user in the separate file below ---->>\n')
        fo.write(''.join(['<< ----', material_path, '---->>\n']))
        # read the files in fispact_material_list and write it here
        fin = open(material_path)
        for line in fin:
            if line.strip().split() == []:
                continue
            line = line.strip()
            fo.write(f"{line}\n")
    else:
        fo.write('<< ----material info. converted from MCNP output file ---->>\n')
        fo.write(
            ' '.join(['DENSITY', str(format(material.density, '.5e')), '\n']))
        fo.write(
            ' '.join(['FUEL', str(len(material.fispact_material_nuclide)), '\n']))
        for i in range(len(material.fispact_material_nuclide)
                       ):  # write nuclide and atoms information
            fo.write(' '.join([material.fispact_material_nuclide[i], str(
                format(material.fispact_material_atom_kilogram[i], '.5e')), '\n']))
    # material part end
    fo.write('MIND 1.E5\n')
    fo.write('HAZARDS\n')
    if (len(neutron_flux) in [70, 316]):  # fission mode
        fo.write('USEFISSION\n')
        fo.write("FISYIELD 4 Th233 U235 U238 Pu239\n")
    fo.write('CLEAR\n')
    if tab4flag:
        fo.write('TAB4 44\n')
    fo.write('ATWO\n')
    fo.write('HALF\n')
    fo.write('NOSTABLE\n')
    fo.write('UNCERT 2\n')
    fo.write('TOLERANCE 0 5.0E3 1.0E-4\n')
    fo.write('TOLERANCE 1 1.0E2 1.0E-4\n')
    # irradiation scenario part
    if AIM == 'COOLANT_ACT_PRE':
        fo.write(IRRADIATION_SCENARIO)
    else:
        fin = open(IRRADIATION_SCENARIO)
        for line in fin:
            line_ele = line.split()
            if len(line.strip()) == 0:  # end of the file
                # fo.write('\n')
                break
            if 'FLUX' in line:  # this is the irradiation part that defines flux
                try:
                    real_flux = float(
                        line_ele[1]) * MODEL_DEGREE / 360.0 * neutron_flux[len(neutron_flux) - 1]
                    fo.write(
                        ' '.join(['FLUX', str(format(real_flux, '.5e')), '\n']))
                except BaseException:
                    errormessage = ''.join(
                        [
                            'Neutron flux length inconsistance with the given Group number',
                            '\n',
                            'Please check the data'])
                    raise ValueError(errormessage)
            else:
                fo.write(line)
        fin.close()
    fo.write('END\n')
    fo.write('*END of RUN \n')
    fo.close()

    # write .flx file
    file_name = ''.join([file_prefix, '.flx'])
    fo = open(file_name, 'w')
    for i in range(len(neutron_flux) - 1):  # reverse the neutron flux
        fo.write(
            ''.join([format_single_output(neutron_flux[len(neutron_flux) - 2 - i]), '\n']))
    fo.write('1.0\n')
    fo.write(' '.join(['Neutron energy group', str(
        len(neutron_flux) - 1), 'G, TOT = ', format_single_output(neutron_flux[-1])]))
    fo.close()


@log
def mesh_fispact_cal_pre(
        AIM,
        WORK_DIR,
        Meshes_need_cal,
        MODEL_DEGREE,
        IRRADIATION_SCENARIO,
        fispact_material_list,
        fispact_material_path,
        FISPACT_FILES_DIR=''):
    """fispact_cal_pre, write .flx and .i files for fispact according to the AIM"""
    # check the input data
    if AIM not in ('MESH_PRE'):  # PRE mode
        raise RuntimeError(
            'mesh_fispact_cal_pre can only called in MESH_PRE mode')

    # when writing fispact input and flx file, material, irradiation scenario (inputed),
    # model_degree (inputed), neutron_flux and prefix are required
    tab4flag = True
    endf_lib_flag = False
    if AIM == 'MESH_PRE':
        for m in Meshes_need_cal:
            file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=m.id,
                                                  ele_type='m', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
            material = m.mat
            neutron_flux = m.neutron_flux
            write_fispact_file(
                material,
                IRRADIATION_SCENARIO,
                MODEL_DEGREE,
                neutron_flux,
                file_prefix,
                tab4flag,
                endf_lib_flag,
                fispact_material_list,
                fispact_material_path)


@log
def mesh_post_process(Meshes, WORK_DIR, AIM, cooling_times):
    """mesh_post_process: check the data of the meshes and then output the ptrans file."""
    # check the AIM
    if AIM not in ('MESH_POST',):
        raise ValueError(
            'mesh_post_process can only be called when AIM is MESH_POST')
    # check the gamma_emit_rate of meshes
    for m in Meshes:
        if m.gamma_emit_rate.shape != (len(cooling_time), 24):
            # this mesh is not calculated, set it's data to zero
            m.gamma_emit_rate = np.zeros((len(cooling_time), 24), dtype=float)
    # write the ptrans file of mesh
    # make a new director for the output files
    dirname = ''.join([WORK_DIR, '/', 'ptrans'])
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    # check the GEOM if the meshes
    GEOM = ''
    origin = []
    axs = []
    vec = []
    if Meshes[0].geom == 'xyz':
        GEOM = 'xyz'
    if Meshes[0].geom == 'cyl':
        GEOM = 'cyl'
        origin = Meshes[0].origin
        axs = Meshes[0].axs
        vec = Meshes[0].vec
    # write content
    for intv in range(len(cooling_times)):
        filename = os.path.join(dirname, ''.joine([str(intv), '.ptrans']))
        fo = open(filename, 'w')
        # section 1: mode CELL/MESH_XYZ/MESH_CYL
        if GEOM == 'xyz':
            fo.write('MESH_XYZ\n')
        if GEOM == 'cyl':
            fo.write('MESH_CYL\n')
            line = ' '.join([str(format(origin[0], '.5e')),
                             str(format(origin[1], '.5e')),
                             str(format(origin[2], '.5e')), '\n'])
            fo.write(line)
            line = ' '.join([str(axs[0]), str(axs[1]), str(axs[2]), '\n'])
            fo.write(line)
            line = ' '.join([str(vec[0]), str(vec[1]), str(vec[2]), '\n'])
            fo.write(line)
        # section 2: number of meshes
        line = ''.join([str(len(Meshes)), '\n'])
        fo.write(line)
        # section 3: mesh geometry, packing_factor and  total gamma emit rate
        if GEOM == 'xyz':
            for m in Meshes:
                line = ' '.join([str(format(m.xmin, '.5e')), str(format(m.xmax, '.5e')),
                                 str(format(m.ymin, '.5e')), str(
                                     format(m.ymax, '.5e')),
                                 str(format(m.zmin, '.5e')), str(
                                     format(m.zmax, '.5e')),
                                 str(format(m.packing_factor, '.5e')),
                                 str(format(sum(m.gamma_emit_rate[intv, :]), '.5e'))])
                line = ''.join([line, '\n'])
                fo.write(line)
        if GEOM == 'cyl':
            for m in Meshes:
                line = ' '.join([str(format(m.rmin, '.5e')), str(format(m.rmax, '.5e')),
                                 str(format(m.zmin, '.5e')), str(
                                     format(m.zmax, '.5e')),
                                 str(format(m.tmin, '.5e')), str(
                                     format(m.tmax, '.5e')),
                                 str(format(m.packing_factor, '.5e')),
                                 str(format(sum(m.gamma_emit_rate[intv, :]), '.5e'))])
                line = ''.join([line, '\n'])
                fo.write(line)
        # section 4: photon spectra of the meshes
        for m in Meshes:
            for j in range(24):
                if j == 0:
                    line = str(format(m.gamma_emit_rate[intv, 0], '.5e'))
                else:
                    line = ' '.join(
                        [line, str(format(m.gamma_emit_rate[intv, j], '.5e'))])
            line = ''.join([line, '\n'])
            fo.write(line)


def get_fispact_file_prefix(WORK_DIR, ele_id, ele_type='c',
                            FISPACT_FILES_DIR=''):
    """
    Get the fispact file prefix.
    """
    if FISPACT_FILES_DIR == '':
        file_prefix = os.path.join(WORK_DIR, f"{ele_type}{ele_id}")
    else:
        file_prefix = os.path.join(FISPACT_FILES_DIR, f"{ele_type}{ele_id}")
    return file_prefix


@log
def cell_fispact_cal_pre(
        AIM,
        WORK_DIR,
        cells_need_cal,
        MODEL_DEGREE,
        IRRADIATION_SCENARIO,
        fispact_material_list,
        fispact_material_path,
        FISPACT_FILES_DIR=''):
    """fispact_cal_pre, write .flx and .i files for fispact according to the AIM"""
    if AIM not in (
        'CELL_ACT_PRE',
        'CELL_ACT_POST',
        'CELL_DPA_PRE',
            'CELL_DPA_POST'):
        raise RuntimeError('cell_fispact_cal_pre can only called in CELL MODE')
    tab4flag = False
    # endf libaries used, then need keyword EAFVERSION 8
    if AIM in ('CELL_DPA_PRE', 'CELL_DPA_POST'):
        endf_lib_flag = True
    else:
        endf_lib_flag = False

    for c in cells_need_cal:
        file_prefix = get_fispact_file_prefix(WORK_DIR, c.id,
                                              FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        material = c.mat
        neutron_flux = c.neutron_flux
        try:
            write_fispact_file(
                material,
                IRRADIATION_SCENARIO,
                MODEL_DEGREE,
                neutron_flux,
                file_prefix,
                tab4flag,
                endf_lib_flag,
                fispact_material_list,
                fispact_material_path)
        except BaseException:
            errormessage = ' '.join(
                ['Encounter Error when writing fispact file of cell:', str(c.id), '\n'])
            raise ValueError(errormessage)


def get_irr_and_cooling_times(part_name, COOLANT_FLOW_PARAMETERS):
    """
    Get irradiation time and cooling times according to part name and
    coolant flow parameters.
    """
    df = pd.read_csv(COOLANT_FLOW_PARAMETERS)
    cols = df.columns
    part_info = np.array(df.loc[df['Parts'] == part_name]).flatten()
    irr_time = float(part_info[2])
    cooling_times_s = []
    for i in range(3, len(cols), 2):
        cooling_times_s.append(part_info[i])
    cooling_times = [float(x) for x in cooling_times_s]
    return irr_time, cooling_times


def construct_irradiation_scenario(irr_time, cooling_times, irr_total_flux):
    """
    Construct FISPACT-II format irradiation scenario.
    """
    irr_snr = '<<-----------Irradiation Scenario--------------->>\n'
    irr_snr += 'FLUX ' + format_single_output(irr_total_flux) + '\n'
    irr_snr += 'TIME ' + format_single_output(irr_time) + ' SECS ATOMS\n'
    irr_snr += 'ZERO\n'
    irr_snr += '<<-----------End of Irradiation --------------->>\n'
    irr_snr += '<<-----------Cooling Times--------------->>\n'
    for i, ct in enumerate(cooling_times):
        irr_snr += 'TIME ' + format_single_output(ct) + ' SECS ATOMS\n'
    return irr_snr


def calc_part_irradiation_scenario(part_name, COOLANT_FLOW_PARAMETERS,
                                   FLUX_MULTIPLIER, n_total_flux, MODEL_DEGREE=360.0):
    """
    Calculate the irradiation scenario according to the coolant flow parameters.

    Parameters:
    -----------
    part_name: str
        The name of the part.
    COOLANT_FLOW_PARAMETERS: str
        The file path of the coolant flow parameters.
    FLUX_MULTIPLIER: float
        The total neutron emitting rate of the fusion device.
        Eg: for CFETR 200 MW case, the value is 7.09e19.
    n_total_flux: float
        Total flux of the part.equal_cell.
    MODEL_DEGREE: float
        Default 360.

    Returns:
    --------
    irradiation_scenario: str
    """
    irr_time, cooling_times = get_irr_and_cooling_times(
        part_name, COOLANT_FLOW_PARAMETERS)
    irr_total_flux = MODEL_DEGREE / 360.0 * FLUX_MULTIPLIER * n_total_flux
    irradiation_scenario = construct_irradiation_scenario(
        irr_time, cooling_times, irr_total_flux)
    return irradiation_scenario


@log
def parts_fispact_cal_pre(AIM, WORK_DIR, parts, MODEL_DEGREE,
                          fispact_material_list, fispact_material_path, COOLANT_FLOW_PARAMETERS,
                          FLUX_MULTIPLIER, FISPACT_FILES_DIR=''):
    """fispact_cal_pre, write .flx and .i files for fispact according to the AIM"""
    tab4flag = False
    endf_lib_flag = False
    # endf libaries used, then need keyword EAFVERSION 8 for p in parts:
    for p in parts:
        file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=p.name,
                                              ele_type='p', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        neutron_flux = p.equal_cell.neutron_flux
        material = p.equal_cell.name
        IRRADIATION_SCENARIO = calc_part_irradiation_scenario(p.name,
                                                              COOLANT_FLOW_PARAMETERS, FLUX_MULTIPLIER, p.equal_cell.neutron_flux[-1], MODEL_DEGREE)
        try:
            write_fispact_file(material, IRRADIATION_SCENARIO, MODEL_DEGREE,
                               neutron_flux, file_prefix, tab4flag, endf_lib_flag,
                               fispact_material_list, fispact_material_path, AIM=AIM)
        except BaseException:
            errormessage = ' '.join(
                ['Encounter Error when writing fispact file of part: ', p.name, '\n'])
            raise ValueError(errormessage)


def get_cell_ids_sub(value):
    """get_cells_id_sub, used to interpret a string of cell list to int list of cell ids"""
    cell_ids_sub = []
    if '~' in value:  # this string need to expand
        cell_ele = value.split('~')
        pre_cell, post_cell = int(cell_ele[0]), int(cell_ele[-1])
        for i in range(pre_cell, post_cell + 1, 1):
            cell_ids_sub.append(i)
    else:
        cell_ids_sub.append(int(value))
    return cell_ids_sub


def get_cell_ids(value):
    """get_cell_ids, used to get cell ids from the context read from PART_CELL_LIST
    input: value, this is a list of string, that need to interpret to cell ids
    return: a list of int that represent the cell ids"""
    cell_ids = []
    for item in value:
        cell_ids_sub = get_cell_ids_sub(item)
        cell_ids.extend(cell_ids_sub)
    return cell_ids


def get_item_ids(value):
    """
    Used to get items (cells or parts or both) from NUC_TREATMENT.
    """
    items = []
    for item in value:
        if '~' in item: # it contains cell range
            cell_ids_sub = get_cell_ids_sub(item)
            items.extend(cell_ids_sub)
        elif is_item_cell(item):
            items.append(int(item))
        elif is_item_part(item):
            items.extend(item)
    return items

def get_subpart_cell_ids_sub(value):
    """get_subpart_cell_id_sub, used to interpret a string of subpart/cell list to int list of subpart/cell ids"""
    cell_ids_sub = []
    subpart_ids_sub = []
    if '~' in value:  # this string need to expand
        cell_ele = value.split('~')
        pre_cell, post_cell = int(cell_ele[0]), int(cell_ele[-1])
        for i in range(pre_cell, post_cell + 1, 1):
            cell_ids_sub.append(i)
    else:
        value.strip()
        try:
            cell_ids_sub.append(int(value))
        except:
            # not a string, it should be a part name
            subpart_ids_sub.append(value)
    return subpart_ids_sub, cell_ids_sub


def get_subpart_cell_ids(value):
    """get_cell_ids, used to get cell ids from the context read from PART_CELL_LIST
    input: value, this is a list of string, that need to interpret to cell ids
    return: a list of int that represent the cell ids"""
    subpart_ids = []
    cell_ids = []
    for item in value:
        subpart_ids_sub, cell_ids_sub = get_subpart_cell_ids_sub(item)
        subpart_ids.extend(subpart_ids_sub)
        cell_ids.extend(cell_ids_sub)
    return subpart_ids, cell_ids


def match_cell_part(part, cells, parts=[]):
    """ put the cells defined int the cell_ids to the part"""
    if len(part.part_cell_list) > 0:  # already matched
        return part
    for item in part.cell_ids:
        cidx = get_cell_index(cells, item)
        part.part_cell_list.append(cells[cidx])
    # if subpart provided
    for sp in part.subpart_ids:
        pidx = get_part_index_by_name(parts, sp)
        if len(parts[pidx].part_cell_list) == 0:  # this part not matched
            parts[pidx] = match_cell_part(parts[pidx], cells, parts)
        for c in parts[pidx].part_cell_list:
            if c in part.part_cell_list:
                raise ValueError(f"Duplicate cell {c.id} in part {part.name}")
            else:
                part.part_cell_list.append(c)
    return part


@log
def get_part(cells, PART_CELL_LIST, COOLANT_FLOW_PARAMETERS=None):
    """get_part, read PART_CELL_LIST and form the parts"""
    parts = []
    part_name = ''
    pid = -1
    if PART_CELL_LIST == '':  # PART_CELL_LIST not given
        return parts
    fin = open(PART_CELL_LIST, 'r')
    line = ' '
    while line != '':
        try:
            line = fin.readline()
        except:
            line = fin.readline().encode('ISO-8859-1')
        line_ele = line.split()
        if is_blank_line(line):  # this is a empty line
            continue
        if is_comment(line):  # this is a comment line
            continue
        # otherwise, this is a line that contains information
        if line[:5] == '     ':  # this is a continue line
            subpart_ids, cell_ids = get_subpart_cell_ids(line_ele)
            parts[pid].cell_ids.extend(cell_ids)
            parts[pid].subpart_ids.extend(subpart_ids)
        else:  # this line contains a part name
            part_name = line_ele[0]
            part = Part()
            part.name = part_name
            parts.append(part)
            subpart_ids, cell_ids = get_subpart_cell_ids(line_ele[1:])
            pid = get_part_index(parts, part)
            parts[pid].cell_ids.extend(cell_ids)
            parts[pid].subpart_ids.extend(subpart_ids)
    for p in parts:
        p = match_cell_part(p, cells, parts=parts)
    fin.close()
    # print all parts for user to check
    info_str = f"parts read from {PART_CELL_LIST} are:"
    for i, p in enumerate(parts):
        if i == 10:
            info_str = f"{info_str}\n      "
        info_str = f"{info_str} {p.name}"
    print(info_str)
    # init equal_cell for each part
    for i, p in enumerate(parts):
        p.init_equal_cell()
    # read part mass flow rate if COOLANT_FLOW_PARAMETERS is provided
    if COOLANT_FLOW_PARAMETERS is not None:
        df = pd.read_csv(COOLANT_FLOW_PARAMETERS)
        for i, p in enumerate(parts):
            part_info = np.array(df.loc[df['Parts'] == p.name]).flatten()
            p.mass_flow_rate = float(part_info[1])
    return parts


@log
def get_nodes(COOLANT_FLOW_PARAMETERS):
    """Get nodes, read COOLNAT_FLOW_PARAMETERS to define nodes"""
    nodes = []
    df = pd.read_csv(COOLANT_FLOW_PARAMETERS)
    cols = df.columns
    for i in range(3, len(cols), 2):
        node_name = cols[i].split('(s)')[0].strip()
        node = Part()
        node.name = node_name
        node.init_equal_cell()
        node.node_part_count = list(np.array(df[node_name + ' counts']))
        nodes.append(node)
    return nodes


@log
def get_cell_need_cal(AIM, parts, cells):
    """calculate the cell need to cal according to the AIM and parts
        input: AIM, the aim of the run
        input: parts, the parts that need to run
        input: cells, the lists of all the cells in the mcnp model
        return: cell_need_cal, a list of cells that need to perform FISPACt run
        CONDITION 1: if the AIM is 'CELL_DPA_PRE/POST' or the 'CELL_ACT_PRE/POST', then the parts must be given
               and then the cell_need_cal will be the cells listed in the parts."""
    # judge the condition
    cell_need_cal = []
    if AIM in ('CELL_DPA_PRE', 'CELL_DPA_POST', 'CELL_ACT_PRE',
               'CELL_ACT_POST'):  # parts should be given
        if len(parts) == 0:
            raise ValueError(
                "if the AIM is 'CELL_DPA_PRE/POST' or the 'CELL_ACT_PRE/POST', then the parts must be given")
        else:
            for p in parts:
                for c in p.part_cell_list:
                    if c not in cell_need_cal:
                        cell_need_cal.append(c)
    return cell_need_cal


@log
def get_mesh_need_cal(Meshes):
    """get_mesh_need_cal: get meshes that need to do the fispact calculate
    input:Meshes, the list of all the meshes
    return: Meshes_need_cal, the list of meshes that need calculate
    GUIDE: meshes that satisfy two condition need cal
    1. non-void material, use mat.density to judge
    2. non-zero total neutron flux, use neutron_flux to judge"""
    Meshes_need_cal = []
    for m in Meshes:
        if m.mat.density > 0 and m.neutron_flux[len(m.neutron_flux) - 1] > 0:
            Meshes_need_cal.append(m)
    return Meshes_need_cal


def check_fispact_output_files(itemlist, WORK_DIR, AIM, FISPACT_FILES_DIR=''):
    """check_fispact_output_files, check whether all the output files needed are available
    input: itemlist, a list of cells/meshes that contains all the items needed to calculate
    WORK_DIR, the working directory
    content, what files are checked, a tuple of '.out','.tab4'
    raise a error when some file are missing, return nothing if all the files are OK."""
    if AIM not in ['CELL_ACT_POST', 'CELL_DPA_POST', 'COOLANT_ACT_POST']:
        raise RuntimeError(
            'check_fispact_output_files not support AIM: {0}'.format(AIM))
    if AIM in ['CELL_ACT_POST', 'CELL_DPA_POST', 'COOLANT_ACT_POST']:
        content = ('.out',)
    for item in itemlist:
        for cnt in content:
            if isinstance(item, Cell):
                file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=item.id,
                                                      ele_type='c', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
            if isinstance(item, Part):
                file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=item.name,
                                                      ele_type='p', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
            check_file_name = f"{file_prefix}{cnt}"
            try:
                f = open(check_file_name)
                f.close()
            except IOError:
                raise RuntimeError(f"File {check_file_name} not accessible")


def check_interval_list(item_list, WORK_DIR, FISPACT_FILES_DIR=''):
    """
    Check the interval lists in the different output files.
    Parameters:
    item_list: list of cells or meshes
    """
    # check the mode CELL/PART
    mode = ''
    if (len(item_list) == 0):
        raise ValueError(
            'numbers of files to check is zero, there must be error, check!')
    if isinstance(item_list[0], Cell):
        mode = 'CELL'
        cooling = True
    if isinstance(item_list[0], Part):
        mode = 'PART'
        cooling = False
    if (mode == ''):
        raise ValueError('item_list to be checked not belong to Cell or Part')

    ref_interval_list = []
    # read the interval list for each item
    for i, item in enumerate(item_list):
        if mode == 'CELL':
            file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=item.id,
                                                  ele_type='c', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        if mode == 'PART':
            file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=item.name,
                                                  ele_type='p', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        filename = f"{file_prefix}.out"
        if i == 0:
            ref_interval_list = get_interval_list(filename)
            ref_filename = filename
        interval_list = get_interval_list(filename)
        if interval_list != ref_interval_list:
            raise ValueError("File {0} has different interval list from the {1}".format(
                filename, ref_filename))
    # no different found, get cooling interval
    interval_list = get_interval_list(filename, cooling=cooling)
    return interval_list


@log
def read_fispact_output_cell(cells_need_cal, WORK_DIR, AIM, cooling_times_cul,
                             FISPACT_FILES_DIR=''):
    """read_fispact_output_act: read the fispact output file to get activation information of cells
    input: cells_need_cal, list a cells that need to calculate and analysis
    input: WORK_DIR, the working director
    return: cells_need_cal, changed list of cells"""
    interval_list = check_interval_list(
        cells_need_cal, WORK_DIR, FISPACT_FILES_DIR=FISPACT_FILES_DIR)
    print('     the intervals need to read are {0}'.format(interval_list))
    for c in cells_need_cal:
        print('       reading cell {0} start'.format(c.id))
        file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=c.id,
                                              ele_type='c', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        filename = f"{file_prefix}.out"
        if AIM == 'CELL_ACT_POST':  # read output information
            read_fispact_out_act(c, filename, interval_list)
        if AIM == 'CELL_DPA_POST':  # read DPA information
            read_fispact_out_dpa(c, filename, interval_list)


@log
def read_fispact_output_part(parts, WORK_DIR, AIM, FISPACT_FILES_DIR=''):
    """read_fispact_output_part: read the fispact output file to get
    activation information of parts in PHTS.

    Parameters:
    -----------
    parts:  list of parts
        parts that need to calculate and analysis
    WORK_DIR: string
        The working director

    Returns:
    --------
    parts:
        Changed list of parts
    """
    interval_list = check_interval_list(
        parts, WORK_DIR, FISPACT_FILES_DIR=FISPACT_FILES_DIR)
    print('     the intervals need to read are {0}'.format(interval_list))
    for i, p in enumerate(parts):
        print('       reading part {0} start'.format(p.name))
        if AIM == 'COOLANT_ACT_POST':  # read output information
            file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=p.name,
                                                  ele_type='p', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
            filename = f"{file_prefix}.out"
            read_fispact_out_act(p.equal_cell, filename, interval_list)
            read_fispact_out_sdr(p.equal_cell, filename, interval_list)


@log
def read_fispact_output_mesh(Meshes_need_cal, WORK_DIR, AIM, cooling_times, FISPACT_FILES_DIR=''):
    """read_fispact_output_mesh: read the tab4 files of meshes to get the gamma emit rate of the meshes
    input: Meshes_need_cal, a list of meshes that need to calculate and analysis
    input: WORK_DIR, the working director
    input: AIM, it must be MESH_POST
    input: cooling time, the cooling interval times
    return: Meshes_need_cal, changed list of meshes"""
    # check the AIM
    if AIM not in ('MESH_POST',):
        raise ValueError(
            'read_fispact_output_mesh can only be called when AIM is MESH_POST')

    interval_list = get_interval_list(Meshes_need_cal, WORK_DIR, cooling_times)
    print('     the interval need read is {0}'.format(interval_list))
    for m in Meshes_need_cal:
        print('       reading mesh {0} start'.format(m.id))
        file_prefix = get_fispact_file_prefix(WORK_DIR, ele_id=m.id,
                                              ele_type='m', FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        m = read_fispact_out_sdr(m, filename, interval_list)
    return Meshes_need_cal


def cell_act_post_process(parts, WORK_DIR, MODEL_DEGREE, AIM,
                          cooling_times_cul, rwss=[]):
    """
    cell_act_post_process: treat the parts, analysis the data and output results

    Parameters:
    -----------
    ...
    rwss: list of RadwasteStandard, optional
        Radwsate standards used.
    """
    # first, merge the cells in the part to get the euqal_cell
    if AIM in ('CELL_ACT_POST', 'CELL_DPA_POST'):
        for p in parts:
            p.merge_cell(AIM)

    # if the AIM is CELL_ACT_POST, then there should perform analysis
    if AIM == 'CELL_ACT_POST':
        for p in parts:
            p.part_act_analysis(AIM, rwss=rwss)
    # if the AIM is CELL_DPA_POST, don't do anything
    # output the data
    for p in parts:
        p.output_data(WORK_DIR, MODEL_DEGREE, AIM,
                      cooling_times_cul=cooling_times_cul, rwss=rwss)


def coolant_act_post_process(parts, nodes, WORK_DIR, MODEL_DEGREE, AIM):
    """
    coolant_act_post_process: treat the parts and coolant, analysis the data
    and output results
    """
    # merge nodes data
    for i, node in enumerate(nodes):
        merge_node_parts(node, parts, i)

    # output the data
    for p in parts:
        p.output_data(WORK_DIR, MODEL_DEGREE, AIM)
    for node in nodes:
        node.output_data(WORK_DIR, MODEL_DEGREE, AIM)


def is_short_live(half_life):
    """
    Check whether the nuclide is short live (half live <= 30 years) nuclide.
    """
    # input check
    if not isinstance(half_life, float):
        raise ValueError("half_life must be a float")
    if half_life < 0:
        raise ValueError("half_life < 0, invalide")
    # 30 year
    threshold = 60.0 * 60 * 24 * 365.25 * 30
    if half_life <= threshold:
        return True
    else:
        return False


def get_material_path(mat_chain_list, path_list, mid):
    """
    Find the material path to replace.
    """
    for i, item in enumerate(mat_chain_list):
        if mid in item:
            return path_list[i]
    raise ValueError("Material path not found")


def check_material_list(mat_chain_list, AIM=None):
    """
    Check material list.
    Raise ValueError when these happens:
    - mid is not int.
    - mid is negtive. (mid could be 0, enable He to replace it)
    - mid is shown in more than one sublist of mat_chain_list.
    """

    extend_list = []
    # check type
    for i, sublist in enumerate(mat_chain_list):
        for j, item in enumerate(sublist):
            if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
                if not isinstance(item, str):
                    raise ValueError(
                        "part name {0} has wrong type or value.".format(str(item)))
            else:
                if not isinstance(item, int) or item < 0:
                    raise ValueError(
                        "mid {0} has wrong type or value.".format(str(item)))
        extend_list.extend(sublist)

    # check repeat
    extend_set = set(extend_list)
    if len(extend_set) != len(extend_list):
        # there is duplicate in the list
        for i, item in enumerate(extend_list):
            count = extend_list.count(item)
            if count > 1:
                raise ValueError(
                    "mid {0} defined more than once.".format(str(item)))
    return True


def merge_node_parts(node, parts, node_index):
    """
    Merge the data of different parts to node according to cooling interval.
    The merged data are stored in node.equal_cell.
    """
    # get the total mass flow rate
    for i, p in enumerate(parts):
        node.mass_flow_rate += p.mass_flow_rate * node.node_part_count[i]
    # treat the nuclide and half-life
    for i, p in enumerate(parts):
        for j, nuc in enumerate(p.equal_cell.nuclide):
            if nuc in node.equal_cell.nuclide:
                pass
            else:
                # add the nuc into node
                node.equal_cell.nuclide.append(nuc)
                node.equal_cell.half_life.append(p.equal_cell.half_life[j])
    # treat the act, decay heat, contact_dose and ci
    NUC = len(node.equal_cell.nuclide)
    INTV = len(parts[0].equal_cell.act)
    node.equal_cell.act = np.resize(node.equal_cell.act, (1, NUC))
    node.equal_cell.total_alpha_act = np.resize(
        node.equal_cell.total_alpha_act, (INTV-1))
    node.equal_cell.decay_heat = np.resize(
        node.equal_cell.decay_heat, (1, NUC))
    node.equal_cell.contact_dose = np.resize(
        node.equal_cell.contact_dose, (1, NUC))
    node.equal_cell.ci = np.resize(node.equal_cell.ci, (1, NUC))
    node.equal_cell.gamma_emit_rate = np.resize(
        node.equal_cell.gamma_emit_rate, (1, 24))
    # merge the data
    for i, p in enumerate(parts):
        for j, nuc in enumerate(p.equal_cell.nuclide):
            nidx = node.equal_cell.nuclide.index(nuc)
            node.equal_cell.act[0][nidx] += p.equal_cell.act[node_index+1][j] * (
                p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate)  # unit: Bq/kg
            node.equal_cell.decay_heat[0][nidx] += p.equal_cell.decay_heat[node_index+1][j] * (
                p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate)  # kW/kg
            node.equal_cell.contact_dose[0][nidx] += p.equal_cell.contact_dose[node_index+1][j] * (
                p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate)  # Sv/h
            node.equal_cell.ci[0][nidx] += p.equal_cell.ci[node_index+1][j] * \
                (p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate)
        for intv in range(INTV-1):
            node.equal_cell.total_alpha_act[intv] += p.equal_cell.total_alpha_act[node_index+1] * (
                p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate)  # kW/kg
        for eb in range(24):
            node.equal_cell.gamma_emit_rate[0][eb] += p.equal_cell.gamma_emit_rate[node_index+1][eb] * (
                p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate)


def get_nuc_treatments(value):
    """
    Get list of the [nuc, treatment].
    """
    nuc_treatments = []
    for i, item in enumerate(value):
        nuc = item.split()[0]
        treatment = float(item.split()[1])
        nuc_treatments.append([nuc, treatment])
    return nuc_treatments


def get_item_nuc_treatments(NUC_TREATMENT):
    """
    Read the file NUC_TREATMENT and get information.

    Parameters:
    -----------
    NUC_TREATMENT: str
        The filename of NUC_TREATMENT.

    Returns:
    --------
    item_list: list
        List of the items (could be Parts or Cells) need to treat.
    treatments: list of list
        List of treatments. Eg.: [['H3', 0.001], ['C14', 0.01']]
    """

    item_nuc_treatments = []
    fin = open(NUC_TREATMENT, 'r')
    line = ' '
    while line != '':
        try:
            line = fin.readline()
        except:
            line = fin.readline().encode('ISO-8859-1')
        if is_blank_line(line):  # this is a empty line
            continue
        if is_comment(line):  # this is a comment line
            continue
        line_ele = line.split(',')
        # otherwise, this is a line that contains information
        item_ids = get_item_ids(line_ele[0].split())
        #cell_ids = get_cell_ids(line_ele[0].split())
        nuc_treatments = get_nuc_treatments(line_ele[1:])
        # put the pair: item, nuc, treatment to list
        for i, c in enumerate(item_ids):
            for j, n_t in enumerate(nuc_treatments):
                item_nuc_treatments.append([c, n_t[0], n_t[1]])
    fin.close()
    return item_nuc_treatments


def expand_item_nuc_treatments(item_nuc_treatments, cells, parts):
    """
    Expand the item_nuc_treatments. The item_nuc_treatments contains list of Cell and Part.
    This funciton expand the Part into cells.
    Noting:
        - The same treatment to a cell will be combined, only perform once.
          For example, A contains cell 1 and 2. The treatment [[1, H3, 0.01], [A, H3, 0.01]]
          will be expanded to [[1, H3, 0.01], [2, H3, 0.01]]
        - Different level of extraction will be combined, only perform the one
          with lower retain. For example, [[1, H3, 0.01], [A, H3, 0.001]] will
          be expanded to [[1, H3, 0.001], [2, H3, 0.001]]
    """
    cell_nuc_treatments = []
    # put all pairs together
    for i, cnt in enumerate(item_nuc_treatments):
        if is_item_cell(cnt[0], cells):
           cell_nuc_treatments.append(cnt)
        elif is_item_part(cnt[0], parts):
            pidx = get_part_index_by_name(parts, cnt[0])
            for c in parts[pidx].cell_ids:
                cell_nuc_treatments.append([c, cnt[1], cnt[2]])
    # sort
    cell_nuc_treatments.sort()
    # combine treatments
    unique_cnts = []
    c_tmp = 0
    l_idx = 0
    for i, cnt in enumerate(cell_nuc_treatments):
        if cnt not in unique_cnts:
            merge_flag = False
            for i in range(l_idx, len(unique_cnts)):
                # check whether there is the same cell, nuc pair
                if cnt[:-1] == unique_cnts[i][:-1]:
                    # use the minimum value of the treatment
                    unique_cnts[i][2] = min(cnt[2], unique_cnts[i][2])
                    merge_flag = True
                    break
            if not merge_flag: # cnt not merged, append it
                unique_cnts.append(cnt)
                if c_tmp < cnt[0]: # update combine progress
                    c_tmp = cnt[0]
                    l_idx = len(unique_cnts) - 1
    return unique_cnts

def treat_nuc(cells, parts, NUC_TREATMENT):
    """
    Treat the nuclide in cells. Such as extract the H3 by a factor of 99.9%.
    """
    if NUC_TREATMENT == '':
        return cells
    item_nuc_treatments = get_item_nuc_treatments(NUC_TREATMENT)
    item_nuc_treatments = expand_item_nuc_treatments(item_nuc_treatments, cells, parts)
    for i, cnt in enumerate(item_nuc_treatments):
        cidx = get_cell_index(cells, cnt[0])  # find cell index
        nidx = cells[cidx].nuclide.index(cnt[1])  # find nuc index
        for intv in range(len(cells[cidx].act)):
            cells[cidx].act[intv, nidx] = cells[cidx].act[intv, nidx] * cnt[2]
            cells[cidx].decay_heat[intv,
                                   nidx] = cells[cidx].decay_heat[intv, nidx] * cnt[2]
            cells[cidx].contact_dose[intv,
                                     nidx] = cells[cidx].contact_dose[intv, nidx] * cnt[2]
            cells[cidx].ci[intv, nidx] = cells[cidx].ci[intv, nidx] * cnt[2]
    return cells


def get_tally_number(config):
    """Get the tally number from config file"""
    TALLY_NUMBER = config.get('mcnp', 'TALLY_NUMBER').split(',')
    for i, tn in enumerate(TALLY_NUMBER):
        try:
            TALLY_NUMBER[i] = int(TALLY_NUMBER[i])
        except:
            raise ValueError(f"TALLY_NUMBER must be integer")
    for tn in TALLY_NUMBER:
        if tn < 0 or (tn % 10) != 4:
            raise ValueError(
                f'Wrong TALLY_NUMBER {tn}, must great than 0 and ended with 4')
    return TALLY_NUMBER


def natf_cell_rwc_vis(config):
    """
    Modify the MCNP_INPUT for visulization.
    """
    # ------ READ input -------
    AIM = 'CELL_RWC_VIS'
    WORK_DIR = config.get('general', 'WORK_DIR')
    # [mcnp]
    MCNP_INPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_INPUT'))
    MCNP_OUTPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_OUTPUT'))
    CONTINUE_OUTPUT = None
    try:
        CONTINUE_OUTPUT = config.get('mcnp', 'CONTINUE_OUTPUT')
        if CONTINUE_OUTPUT != '':
            CONTINUE_OUTPUT = os.path.join(
                WORK_DIR, config.get('mcnp', 'CONTINUE_OUTPUT'))
    except:
        pass
    # mcnp.tally_number
    TALLY_NUMBER = get_tally_number(config)
    # mcnp.n_group_size
    N_GROUP_SIZE = config.getint('mcnp', 'N_GROUP_SIZE')
    cells = get_cell_basic_info(MCNP_OUTPUT)
    cells = get_cell_tally_info(MCNP_OUTPUT, cells, TALLY_NUMBER, N_GROUP_SIZE,
                                CONTINUE_OUTPUT=CONTINUE_OUTPUT)
    # [model], required
    PART_CELL_LIST = os.path.join(
        WORK_DIR, config.get('model', 'PART_CELL_LIST'))
    parts = get_part(cells, PART_CELL_LIST)
    # [fispact]
    IRRADIATION_SCENARIO = os.path.join(WORK_DIR,
                                        config.get('fispact', 'IRRADIATION_SCENARIO'))
    cooling_times = get_cooling_times(IRRADIATION_SCENARIO, AIM)
    cooling_times_cul = get_cooling_times_cul(cooling_times)
    # [radwaste] standard
    RADWASTE_STANDARDS = config.get(
        'radwaste', 'RADWASTE_STANDARDS').split(',')
    rwss = []
    for item in RADWASTE_STANDARDS:
        rws = RadwasteStandard(item.strip())
        rwss.append(rws)

    # get RWC CHN2018 for each cooling_time
    names = []
    for p in parts:
        names.append(p.name)
    # rewrite MCNP_INPUT for each cooling_time
    for rws in rwss:
        key = f'rwc_{rws.standard.lower()}'
        rwcs = get_rwcs_by_cooling_times(names, cooling_times=cooling_times_cul,
                                         key=key, work_dir=WORK_DIR)
        if rws.standard in ['CHN2018']:
            classes = ['LLW', 'Clearance']
        else:
            classes = ['LLW']

        ctrs = calc_rwc_cooling_requirement(names, key=key,
                                            classes=classes, standard=rws.standard, work_dir=WORK_DIR,
                                            out_unit='a', ofname=None)
        for i, ct in enumerate(cooling_times_cul):
            filename = f"{MCNP_INPUT}_{rws.standard.lower()}_ct{i}.txt"
            fo = open(filename, 'w')
            # rewite cell card
            with open(MCNP_INPUT, 'r') as fin:
                cell_start, surf_start = False, False
                cell_end, surf_end = False, False
                while True:
                    line = fin.readline()
                    if line == '':
                        break
                    # end of cell card
                    if is_blank_line(line) and cell_start and not surf_start:
                        cell_end = True
                        surf_start = True
                        fo.write(line)
                        continue
                    if is_comment(line):
                        fo.write(line)
                        continue
                    if is_cell_title(line):
                        cell_start = True
                        cid, mid, den = get_cell_cid_mid_den(line)
                        if is_cell_id_in_parts(parts, cid):
                            pidx = get_part_index_by_cell_id(
                                parts, cid, find_last=True)
                            rwc = rwcs[pidx][i]
                            rwci = rwc_to_int(rwc, standard=rws.standard)
                            new_line = cell_title_change_mat(
                                line, new_mid=rwci, new_den=1.0)
                            fo.write(new_line+'\n')
                        else:  # this cell do not belong to activated parts, set to void
                            new_line = cell_title_change_mat(
                                line, new_mid=0, new_den=None)
                            fo.write(new_line+'\n')
                        continue
                    if is_blank_line(line) and surf_start and not surf_end:
                        surf_end = True
                        fo.write(line)
                        # append pseudo-mat here
                        fo.write(f"C ---- pseudo-mat for RWC VIS--------\n")
                        fo.write(create_pseudo_mat(mid=1).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=2).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=3).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=4).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=5).__str__()+'\n')
                        continue
                    fo.write(line)  # other lines
            fo.write('\n')  # new line at the end
            fo.close()
        # rewrite MCNP_INPUT for Time-to-Clearance and Time-to-LLW
        for i, cls in enumerate(classes):
            filename = f"{MCNP_INPUT}_{rws.standard.lower()}_to_{cls}.txt"
            fo = open(filename, 'w')
            # rewite cell card
            with open(MCNP_INPUT, 'r') as fin:
                cell_start, surf_start = False, False
                cell_end, surf_end = False, False
                while True:
                    line = fin.readline()
                    if line == '':
                        break
                    # end of cell card
                    if is_blank_line(line) and cell_start and not surf_start:
                        cell_end = True
                        surf_start = True
                        fo.write(line)
                        continue
                    if is_comment(line):
                        fo.write(line)
                        continue
                    if is_cell_title(line):
                        cell_start = True
                        cid, mid, den = get_cell_cid_mid_den(line)
                        if is_cell_id_in_parts(parts, cid):
                            pidx = get_part_index_by_cell_id(
                                parts, cid, find_last=True)
                            ctr = ctrs[pidx][i]
                            ctri = ctr_to_int(ctr)
                            new_line = cell_title_change_mat(
                                line, new_mid=ctri, new_den=1.0)
                            fo.write(new_line+'\n')
                            continue
                        else:  # this cell do not belong to activated parts, set to void
                            new_line = cell_title_change_mat(
                                line, new_mid=0, new_den=None)
                            fo.write(new_line+'\n')
                            continue
                    if is_blank_line(line) and surf_start and not surf_end:
                        surf_end = True
                        fo.write(line)
                        # append pseudo-mat here
                        fo.write(f"C ---- pseudo-mat for RWC VIS--------\n")
                        fo.write(create_pseudo_mat(mid=1).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=2).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=3).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=4).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=5).__str__()+'\n')
                        continue
                    fo.write(line)  # other lines
            fo.write('\n')  # new line at the end
            fo.close()
    # rewrite MCNP_INPUT for Recycling
    ctrs = [[], []]  # CRH, ARH
    ctrs[0] = calc_recycle_cooling_requirement(
        names, key='cdt', rh='CRH', work_dir=WORK_DIR, out_unit='a')
    ctrs[1] = calc_recycle_cooling_requirement(
        names, key='cdt', rh='ARH', work_dir=WORK_DIR, out_unit='a')
    for i in range(0, 2):
        if i == 0:
            filename = f"{MCNP_INPUT}_to_recycle_crh.txt"
        else:
            filename = f"{MCNP_INPUT}_to_recycle_arh.txt"
        fo = open(filename, 'w')
        # rewite cell card
        with open(MCNP_INPUT, 'r') as fin:
            cell_start, surf_start = False, False
            cell_end, surf_end = False, False
            while True:
                line = fin.readline()
                if line == '':
                    break
                if is_blank_line(line) and cell_start and not surf_start:  # end of cell card
                    cell_end = True
                    surf_start = True
                    fo.write(line)
                    continue
                if is_comment(line):
                    fo.write(line)
                    continue
                if is_cell_title(line):
                    cell_start = True
                    cid, mid, den = get_cell_cid_mid_den(line)
                    if is_cell_id_in_parts(parts, cid):
                        pidx = get_part_index_by_cell_id(
                            parts, cid, find_last=True)
                        ctrs
                        ctr = ctrs[i][pidx]
                        ctri = ctr_to_int(ctr)
                        new_line = cell_title_change_mat(
                            line, new_mid=ctri, new_den=1.0)
                        fo.write(new_line+'\n')
                        continue
                    else:  # this cell do not belong to activated parts, set to void
                        new_line = cell_title_change_mat(
                            line, new_mid=0, new_den=None)
                        fo.write(new_line+'\n')
                        continue
                if is_blank_line(line) and surf_start and not surf_end:
                    surf_end = True
                    fo.write(line)
                    # append pseudo-mat here
                    fo.write(f"C ---- pseudo-mat for RWC VIS--------\n")
                    fo.write(create_pseudo_mat(mid=1).__str__()+'\n')
                    fo.write(create_pseudo_mat(mid=2).__str__()+'\n')
                    fo.write(create_pseudo_mat(mid=3).__str__()+'\n')
                    fo.write(create_pseudo_mat(mid=4).__str__()+'\n')
                    fo.write(create_pseudo_mat(mid=5).__str__()+'\n')
                    continue
                fo.write(line)  # other lines
        fo.write('\n')  # new line at the end
        fo.close()


def natf_cell_act_pre(config):
    # general
    WORK_DIR = config.get('general', 'WORK_DIR')
    AIM = config.get('general', 'AIM')
    # [mcnp]
    MCNP_INPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_INPUT'))
    MCNP_OUTPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_OUTPUT'))
    CONTINUE_OUTPUT = None
    try:
        CONTINUE_OUTPUT = config.get('mcnp', 'CONTINUE_OUTPUT')
        if CONTINUE_OUTPUT != '':
            CONTINUE_OUTPUT = os.path.join(
                WORK_DIR, config.get('mcnp', 'CONTINUE_OUTPUT'))
    except:
        pass
    # mcnp.tally_number
    TALLY_NUMBER = get_tally_number(config)
    # mcnp.n_group_size
    N_GROUP_SIZE = config.getint('mcnp', 'N_GROUP_SIZE')

    # [fispact]
    # fispact.fispact_material_list, optional
    try:
        FISPACT_MATERIAL_LIST = config.get('fispact', 'FISPACT_MATERIAL_LIST')
        if FISPACT_MATERIAL_LIST != '':
            FISACT_MATERIAL_LIST = os.path.join(
                WORK_DIR, FISPACT_MATERIAL_LIST)
    except:
        FISPACT_MATERIAL_LIST = ''
    # fispact.irradiation_scenario
    IRRADIATION_SCENARIO = os.path.join(
        WORK_DIR, config.get('fispact', 'IRRADIATION_SCENARIO'))
    # fispact.fispact_files_dir, optional
    FISPACT_FILES_DIR = ''
    try:
        FISPACT_FILES_DIR = config.get('fispact', 'FISPACT_FILES_DIR')
        if FISPACT_FILES_DIR != '':
            FISPACT_FILES_DIR = os.path.join(WORK_DIR, FISPACT_FILES_DIR)
    except:
        pass

    # [model], required
    PART_CELL_LIST = os.path.join(
        WORK_DIR, config.get('model', 'PART_CELL_LIST'))
    # model.model_degree, optional
    try:
        MODEL_DEGREE = float(config.get('model', 'MODEL_DEGREE'))
    except:
        MODEL_DEGREE = 360.0

    # read the fispact material list
    fispact_material_list, fispact_material_path = get_fispact_material_list(
        FISPACT_MATERIAL_LIST, AIM)
    cooling_times = get_cooling_times(IRRADIATION_SCENARIO, AIM)
    cooling_times_cul = get_cooling_times_cul(cooling_times)
    # read mcnp output file, get cell information:
    # icl, cid, mid, vol (cm3), mass (g)
    cells = get_cell_basic_info(MCNP_OUTPUT)
    cells = get_cell_tally_info(MCNP_OUTPUT, cells, TALLY_NUMBER, N_GROUP_SIZE,
                                CONTINUE_OUTPUT=CONTINUE_OUTPUT)
    materials = get_material_info(MCNP_OUTPUT)
    materials = convert_material_mcnp_to_fispact(materials)
    cells = match_cells_materials(cells, materials)
    parts = get_part(cells, PART_CELL_LIST)
    cells_need_cal = get_cell_need_cal(AIM, parts, cells)
    cell_fispact_cal_pre(AIM, WORK_DIR, cells_need_cal, MODEL_DEGREE,
                         IRRADIATION_SCENARIO, fispact_material_list,
                         fispact_material_path,
                         FISPACT_FILES_DIR=FISPACT_FILES_DIR)
    print('End of NATF: {0}'.format(AIM))


def natf_run():
    # first check the input file to get running information
    input_filename = "input"
    config = ConfigParser.ConfigParser()
    config.read(input_filename)
    # general
    WORK_DIR = config.get('general', 'WORK_DIR')
    AIM = config.get('general', 'AIM')
    if AIM == 'CELL_RWC_VIS':
        natf_cell_rwc_vis(config)
        return
    if AIM == 'CELL_ACT_PRE':
        natf_cell_act_pre(config)
        return
    check_input(filename=input_filename)
    # [mcnp]
    MCNP_INPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_INPUT'))
    MCNP_OUTPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_OUTPUT'))
    CONTINUE_OUTPUT = None
    try:
        CONTINUE_OUTPUT = config.get('mcnp', 'CONTINUE_OUTPUT')
        if CONTINUE_OUTPUT != '':
            CONTINUE_OUTPUT = os.path.join(
                WORK_DIR, config.get('mcnp', 'CONTINUE_OUTPUT'))
    except:
        pass

    # mcnp.tally_number
    TALLY_NUMBER = get_tally_number(config)
    # mcnp.n_group_size
    N_GROUP_SIZE = config.getint('mcnp', 'N_GROUP_SIZE')

    # [coolant_flow]
    if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
        COOLANT_FLOW_PARAMETERS = os.path.join(WORK_DIR,
                                               config.get('coolant_flow', 'COOLANT_FLOW_PARAMETERS'))
        FLUX_MULTIPLIER = float(config.get('coolant_flow', 'FLUX_MULTIPLIER'))

    # [fispact]
    # fispact.fispact_material_list, optional
    try:
        FISPACT_MATERIAL_LIST = config.get('fispact', 'FISPACT_MATERIAL_LIST')
        if FISPACT_MATERIAL_LIST != '':
            FISACT_MATERIAL_LIST = os.path.join(
                WORK_DIR, FISPACT_MATERIAL_LIST)
    except:
        FISPACT_MATERIAL_LIST = ''

    try:
        NUC_TREATMENT = config.get('fispact', 'NUC_TREATMENT')
    except:
        NUC_TREATMENT = ''
    # fispact.irradiation_scenario, required in CELL_ACT and CELL_DPA mode
    if AIM in ['CELL_ACT_PRE', 'CELL_ACT_POST', 'CELL_DPA_PRE', 'CELL_DPA_POST']:
        IRRADIATION_SCENARIO = os.path.join(WORK_DIR,
                                            config.get('fispact', 'IRRADIATION_SCENARIO'))
    # fispact.fispact_files_dir, optional
    FISPACT_FILES_DIR = ''
    try:
        FISPACT_FILES_DIR = config.get('fispact', 'FISPACT_FILES_DIR')
        if FISPACT_FILES_DIR != '':
            FISPACT_FILES_DIR = os.path.join(WORK_DIR, FISPACT_FILES_DIR)
    except:
        pass

    # [model], required
    PART_CELL_LIST = os.path.join(WORK_DIR,
                                  config.get('model', 'PART_CELL_LIST'))
    # model.model_degree, optional
    try:
        MODEL_DEGREE = float(config.get('model', 'MODEL_DEGREE'))
    except:
        MODEL_DEGREE = 360.0

    # [radwaste] standard
    try:
        RADWASTE_STANDARDS = config.get(
            'radwaste', 'RADWASTE_STANDARDS').split(',')
    except:
        RADWASTE_STANDARDS = []

    # read the fispact material list
    fispact_material_list, fispact_material_path = get_fispact_material_list(
        FISPACT_MATERIAL_LIST, AIM)

    # ---------------------ACT and DPA calculation----------------------
    # read the irradiation scenario. If the AIM is CELL_DPA,then only
    if AIM in ['CELL_ACT_PRE', 'CELL_DPA_PRE', 'CELL_ACT_POST', 'CELL_DPA_POST']:
        # one irradiation pulse allowed, the pulse must be a FULL POWER YEAR.
        cooling_times = get_cooling_times(IRRADIATION_SCENARIO, AIM)
        cooling_times_cul = get_cooling_times_cul(cooling_times)

    if AIM in ['CELL_ACT_PRE', 'CELL_DPA_PRE', 'CELL_ACT_POST', 'CELL_DPA_POST']:
        # read mcnp output file, get cell information:
        # icl, cid, mid, vol (cm3), mass (g)
        cells = get_cell_basic_info(MCNP_OUTPUT)
        cells = get_cell_tally_info(MCNP_OUTPUT, cells, TALLY_NUMBER, N_GROUP_SIZE,
                                    CONTINUE_OUTPUT=CONTINUE_OUTPUT)
        materials = get_material_info(MCNP_OUTPUT)
        materials = convert_material_mcnp_to_fispact(materials)
        cells = match_cells_materials(cells, materials)
        parts = get_part(cells, PART_CELL_LIST)
        cells_need_cal = get_cell_need_cal(AIM, parts, cells)
    if AIM in ('CELL_ACT_PRE', 'CELL_DPA_PRE'):
        cell_fispact_cal_pre(AIM, WORK_DIR, cells_need_cal, MODEL_DEGREE,
                             IRRADIATION_SCENARIO, fispact_material_list,
                             fispact_material_path,
                             FISPACT_FILES_DIR=FISPACT_FILES_DIR)
    if AIM in ('CELL_ACT_POST', 'CELL_DPA_POST'):
        # first, check whether all the fispact output files are available
        check_fispact_output_files(
            cells_need_cal, WORK_DIR, AIM, FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        # then read the output information
        read_fispact_output_cell(cells_need_cal, WORK_DIR, AIM,
                                 cooling_times_cul, FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        treat_nuc(cells_need_cal, parts, NUC_TREATMENT)
        rwss = []
        for item in RADWASTE_STANDARDS:
            rws = RadwasteStandard(item.strip())
            rwss.append(rws)
        cell_act_post_process(parts, WORK_DIR, MODEL_DEGREE,
                              AIM, cooling_times_cul, rwss=rwss)

    if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
        cells = get_cell_basic_info(MCNP_OUTPUT)
        cells = get_cell_tally_info(
            MCNP_OUTPUT, cells, TALLY_NUMBER, N_GROUP_SIZE)
        parts = get_part(cells, PART_CELL_LIST, COOLANT_FLOW_PARAMETERS)
        nodes = get_nodes(COOLANT_FLOW_PARAMETERS)
    if AIM == 'COOLANT_ACT_PRE':
        parts_fispact_cal_pre(AIM, WORK_DIR, parts, MODEL_DEGREE,
                              fispact_material_list, fispact_material_path,
                              COOLANT_FLOW_PARAMETERS, FLUX_MULTIPLIER)
    if AIM == 'COOLANT_ACT_POST':
        # first, check whether all the fispact output files are available
        check_fispact_output_files(
            parts, WORK_DIR, AIM, FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        read_fispact_output_part(parts, WORK_DIR, AIM,
                                 FISPACT_FILES_DIR=FISPACT_FILES_DIR)
        coolant_act_post_process(parts, nodes, WORK_DIR, MODEL_DEGREE, AIM)

    print('End of NATF: {0}'.format(AIM))


# codes for test functions
if __name__ == '__main__':
    pass
