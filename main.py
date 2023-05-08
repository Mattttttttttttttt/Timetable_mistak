#TODO: Найти накладки в расписании лектора
"""1. Очистить файл от мусора
2. Свести одного лектора в один файл
3. найти накладки по принципу:
    а) нет пересечения потоков (3 группы на лекции, 1 группа на пр, 1 на лр
    б) нет пересечения типов пар (одновременно лр и пр и тп)"""
import os

import pandas as pd
import numpy as np
from glob import glob as glob
import openpyxl



"""base_path = 'D:\Desktop\Программы Питон\ИТИП ошибки расписания\main'
in_files = sorted(glob(base_path + '/*.xls*'))
#print(in_files)
df_list = []
for f in in_files:
    df_list.append(pd.read_excel(f))
    print(f)
for i in range(len(df_list)):
    col_names = [
        'day',
        'l_num',
        'l_time',
        'l_room_1',
        'l_type_1',
        'lector_1',
        'discipline_1',
        'discipline_2',
        'lector_2',
        'l_type_2',
        'l_room_2'
    ]
    df_list[i].columns = col_names
    # print(df)
    indexes = list(df_list[i].columns)
    indexes[:len(col_names)] = col_names
    df_list[i].columns = indexes
    norm_t_table = df_list[i][df_list[i]['l_time'].notna()].copy()
    norm_t_table.dropna(
        axis=1,
        how='all',
        inplace=True
    )
    norm_t_table['day'] = norm_t_table['day'].ffill()
    col_to_drop = [col for col in norm_t_table.columns if col not in col_names]
    norm_t_table.drop(
        columns=col_to_drop,
        inplace=True
    )
    norm_t_table.drop(
        norm_t_table[norm_t_table['day'] == 'День недели'].index,
        inplace=True
    )
    rows = norm_t_table[norm_t_table['l_room_1'].isnull() == True]
    rows = rows[norm_t_table['l_room_2'].isnull() == True]
    norm_t_table.drop(
        index=rows.index,
        inplace=True
    )
    df_list[i]=norm_t_table

master_df = df_list[0]
for i in range(1, len(df_list)):
    master_df = pd.concat([master_df, df_list[i]])
print(master_df)"""
exel_file = pd.ExcelFile('D:\Desktop\Программы Питон\ИТИП ошибки расписания\main\BIK2102.xlsx')
df = pd.read_excel(exel_file)
#print(df)
col_names = [
    'day',
    'l_num',
    'l_time',
    'l_room_1',
    'l_type_1',
    'lector_1',
    'discipline_1',
    'discipline_2',
    'lector_2',
    'l_type_2',
    'l_room_2'
]
df.columns = col_names
#print(df)
indexes = list(df.columns)
indexes[:len(col_names)] = col_names
df.columns = indexes
norm_t_table = df[df['l_time'].notna()].copy()
norm_t_table.dropna(
    axis=1,
    how='all',
    inplace=True
)
norm_t_table['day'] = norm_t_table['day'].ffill()
col_to_drop = [col for col in norm_t_table.columns if col not in col_names]
norm_t_table.drop(
    columns=col_to_drop,
    inplace=True
)
norm_t_table.drop(
    norm_t_table[norm_t_table['day'] == 'День недели'].index,
    inplace=True
)
rows = norm_t_table[norm_t_table['l_room_1'].isnull() == True]
rows = rows[norm_t_table['l_room_2'].isnull() == True]
norm_t_table.drop(
    index = rows.index,
    inplace = True
)
print(norm_t_table)
norm_t_table=norm_t_table[(norm_t_table['lector_1'] == 'Егоров Д.А.') | (norm_t_table['lector_2'] == 'Егоров Д.А.')]


#master_df.to_excel('D:\Desktop\Программы Питон\ИТИП ошибки расписания\output.xlsx')