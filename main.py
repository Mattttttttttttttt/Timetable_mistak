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



base_path = 'D:\Desktop\Программы Питон\ИТИП ошибки расписания\main'
in_files = sorted(glob(base_path + '/*.xls*'))
print(in_files)
#file_list = ['BIK2101', 'BIK2102','BIK2103','BIK2104','BIK2105', 'BIK2106', 'BIK2107', 'BIK2108', 'BIK2109','BIK2201', 'BIK2202','BIK2203','BIK2204','BIK2205', 'BIK2206', 'BIK2207', 'BIK2208', 'BIK2209']
df_list = []
"""for i in range(1,len(file_list)):
    df_list.append(pd.read_excel(f'D:\Desktop\Программы Питон\ИТИП ошибки расписания\main\{file_list[i]}.xlsx'))
    print(f'D:\Desktop\Программы Питон\ИТИП ошибки расписания\main\{file_list[i]}.xlsx')"""
for f in in_files:
    df_list.append(pd.read_excel(f))
    #print(f)
for i in range(len(df_list)):
    print(in_files[i])
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
#print(master_df)
"""exel_file = pd.ExcelFile('D:\Desktop\Программы Питон\ИТИП ошибки расписания\main\BIK2102.xlsx')
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
"""
lector = master_df['lector_1' or 'lector_2'].unique()
for i in range(1,len(lector)+1):
    print(f"{i}.  {lector[i-1]}")
n = 0
while (n<=0 or n>len(lector)):
    n = int(input("Введите номер преподавателя из списка:"))
    if n<0 or n>len(lector): print("Повторите ввод, ошибка")
lec = lector[n-1]
print(lec)
master_df_1 = master_df[master_df['lector_1'] == lec]
master_df_1 = master_df_1.iloc[:,0:7]
master_df_2 = master_df[master_df['lector_2'] == lec]
#master_df_2 = master_df_2.iloc[:,[0,1,2,7,8,9,10,11]]
final_df = pd.concat([master_df_1, master_df_2])
#print(master_df_1)
#print(master_df_2)
dict = {
    1: 'понедельник',
    2: 'вторник',
    3: 'среда',
    4: 'четверг',
    5: 'пятница',
    6: 'суббота'
}
err = 0
df_err = pd.DataFrame()

for i in range(1,7):
    df = final_df[final_df['day'] == dict[i]]
    #print(f'{i}:')
    #print(df)
    for j in range(1,5):
        df_1 = df[df['l_num'] == j]
        master_df_1 = df_1[df_1['lector_1'] == lec]
        if (master_df_1.shape[0] > 1 and master_df_1.shape[0] <4):
            df_l1 = master_df_1[master_df_1['l_type_1'] != 'л.']
            df_l1 = df_l1[df_l1['l_type_1'] != ' л.']
            if df_l1.shape[0] > 1:
                err = err + 1
                print(f"Найдена ошибка номер {err}: ")
                print(df_l1)
                df_err = pd.concat([df_err, df_l1])
        elif(master_df_1.shape[0] >=4):
            err = err + 1
            print(f"Найдена ошибка номер {err}: ")
            print(master_df_1.shape)
            df_err = pd.concat([df_err, master_df_1])
        master_df_2 = df_1[df_1['lector_2'] == lec]
        if (master_df_2.shape[0] > 1 and master_df_2.shape[0] < 4):
            df_l2 = master_df_2[master_df_2['l_type_2'] != 'л.']
            df_l2 = df_l2[df_l2['l_type_2'] != ' л.']
            if df_l2.shape[0] > 1:
                err = err + 1
                print(f"Найдена ошибка номер {err}: ")
                print(df_l2)
                df_err = pd.concat([df_err, df_l2])
        elif(master_df_2.shape[0] >=4):
            err = err + 1
            print(f"Найдена ошибка номер {err}: ")
            print(master_df_2)
            df_err = pd.concat([df_err, master_df_2])

if err == 0:
    print("Ошибок нет")
    final_df.to_excel('D:\Desktop\Программы Питон\ИТИП ошибки расписания\output.xlsx')
else:
    print("Все ошибки выведены в: D:\Desktop\Программы Питон\ИТИП ошибки расписания\output.xlsx")
    df_err.to_excel('D:\Desktop\Программы Питон\ИТИП ошибки расписания\output.xlsx')