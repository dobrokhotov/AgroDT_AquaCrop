import os
import pandas as pd
from datetime import datetime

def format_aquacrop_meteo(project_name, meteocsvfile_path, data_path='aquacrop/aquacrop_fortran/project/DATA'):
    '''
    Function to create AquaCrop Climate files
    :param project_name:
    :param meteocsvfile_path:
    :param data_path:
    :return:
    '''
    df = pd.read_csv(meteocsvfile_path, index_col=0)
    df.index = pd.to_datetime(df.index, format='%Y%m%d')

    start_day = df.index[0].day
    start_month = df.index[0].month
    start_year = df.index[0].year

    # ET0
    eto_path = os.path.join(data_path, f'{project_name}.ETo')
    df['ET0_str'] = df['ET0'].apply(lambda x: str(round(x, 1)) + '\n')
    with open(eto_path, 'w') as f:
        f.write(f'{project_name}\n')
        f.write(f'     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n')
        f.write(f'     {start_day}  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n')
        f.write(f'     {start_month}  : First month of record\n')
        f.write(f'  {start_year}  : First year of record (1901 if not linked to a specific year))\n')
        f.write('\n')
        f.write('  Average ETo (mm/day) \n')
        f.write('======================= \n')
        f.writelines(df['ET0_str'])

    # PRECIPITATION
    plu_path = os.path.join(data_path, f'{project_name}.PLU')
    df['Pr_str'] = df['Pr'].apply(lambda x: str(round(x, 1)) + '\n')
    with open(plu_path, 'w') as f:
        f.write(f'{project_name}\n')
        f.write(f'     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n')
        f.write(f'     {start_day}  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n')
        f.write(f'     {start_month}  : First month of record\n')
        f.write(f'  {start_year}  : First year of record (1901 if not linked to a specific year))\n')
        f.write('\n')
        f.write('  Total Rain (mm) \n')
        f.write('======================= \n')
        f.writelines(df['Pr_str'])

    # TEMPERATURES
    tnx_path = os.path.join(data_path, f'{project_name}.Tnx')
    df['Tn_str'] = df['Tn'].apply(lambda x: str(round(x, 1)))
    df['Tx_str'] = df['Tx'].apply(lambda x: str(round(x, 1)))
    df['Tnx_str'] = df['Tn_str'] + '\t' + df['Tx_str'] + '\n'
    with open(tnx_path, 'w') as f:
        f.write(f'{project_name}\n')
        f.write(f'     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n')
        f.write(f'     {start_day}  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n')
        f.write(f'     {start_month}  : First month of record\n')
        f.write(f'  {start_year}  : First year of record (1901 if not linked to a specific year))\n')
        f.write('\n')
        f.write('  Tmin (C)   TMax (C)\n')
        f.write('=======================\n')
        f.writelines(df['Tnx_str'])

    # CLIMATE
    cli_path = os.path.join(data_path, f'{project_name}.CLI')
    with open(cli_path, 'w') as f:
        f.write(f'{project_name}\n')
        f.write(' 7.1   : AquaCrop Version (August 2023)\n')
        f.write(f'{project_name}.Tnx\n')
        f.write(f'{project_name}.ETo\n')
        f.write(f'{project_name}.PLU\n')
        f.write(f'MaunaLoa.CO2')


def format_aquacrop_calendar(project_name, growing_season_start, data_path='aquacrop/aquacrop_fortran/project/DATA'):
    '''
    Fucntion to create AquaCrop calendar file
    :param project_name:
    :param growing_season_start:
    :param data_path:
    :return:
    '''
    growing_season_start_dt = datetime.strptime(str(growing_season_start), '%Y%m%d')
    growing_season_start_doy = growing_season_start_dt.strftime('%j')

    cal_path = os.path.join(data_path, f'{project_name}.CAL')
    with open(cal_path, 'w') as f:
        f.write(f'{project_name}\n')
        f.write('         7.1  : AquaCrop Version (August 2023)\n')
        f.write('         0    : The onset of the growing period is fixed on a specific date\n')
        f.write('        -9    : Day-number (1 ... 366) of the Start of the time window for the onset criterion: Not applicable\n')
        f.write('        -9    : Length (days) of the time window for the onset criterion: Not applicable\n')
        f.write(f'       {growing_season_start_doy}    : Day-number (1 ... 366) for the onset of the growing period\n')
        f.write('        -9    : Number of successive days: Not applicable\n')
        f.write('        -9    : Number of occurrences: Not applicable')

def get_crop_parameters_dict(cropfile_path='WheatGDD.CRO'):

    with open(cropfile_path) as f:
        lines = f.readlines()

    values = [i.strip().split(':', 1)[0].strip() for i in lines[1:]]
    parameters = [i.strip().split(':', 1)[1].strip() for i in lines[1:]]
    ser = pd.Series(data=values, index=parameters)

    return ser

def modify_aquacrop_crop(project_name, parameters_dict_modify, cropfile_folder, cropfile='WheatGDD.CRO'):

    cropfile_path = os.path.join(cropfile_folder, cropfile)
    with open(cropfile_path) as f:
        lines = f.readlines()

    values = [i.strip().split(':', 1)[0].strip() for i in lines[1:]]
    parameters = [i.strip().split(':', 1)[1].strip() for i in lines[1:]]

    ser = pd.Series(data=values, index=parameters)
    ser.update(parameters_dict_modify)

    out_cropfile = project_name + '_' + cropfile
    out_cropfile_path = os.path.join(cropfile_folder, out_cropfile)

    with open(out_cropfile_path, 'w') as f:
        f.write(f'{project_name}\n')
        for k, v in ser.items():
            v_modify = '  ' + str(v)
            v_modify = v_modify + ' ' * (15 - len(v_modify))
            f.write(f'{v_modify}: {k}\n')

    return out_cropfile



