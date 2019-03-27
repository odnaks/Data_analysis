import pandas as pd
import numpy as np

result = pd.DataFrame(columns=['Файл', 'ИНН'])

xls = pd.ExcelFile("perech.xlsx")
sheet_to_df_map = {}
k = 0
flag = 0
for sheet_name in xls.sheet_names:
    if (flag == 0):
        data_ref = xls.parse(sheet_name)
        col_inn = data_ref['ИНН']
        list_inn = col_inn.tolist()
        #print (list_inn)
        flag += 1
    else:
        data = xls.parse(sheet_name)
        if (sheet_name != 'error'):
            for i, row in data.iterrows():
                for j, column in row.iteritems():
                    if (type(column) == str):
                        if ((column.find("INN") != -1) or (column.find("ИНН") != -1)):
                            words = column.split(" ")
                            for word in words:
                                if ((word.isdigit()) and (len(word) > 8) and (len(word) < 13)):
                                    int_word = int(word)
                                    result.loc[k] = [sheet_name, int_word]
                                    k += 1
                    elif (type(column) == int):
                        if ((column > 99999999) and (column < 9999999999999)):
                            result.loc[k] = [sheet_name, column]
                            k += 1
result = result.drop_duplicates('ИНН')
col_inn_match = result['ИНН']
list_inn_match = col_inn_match.tolist()
result_1 = pd.DataFrame(columns=['Файл', 'ИНН'])
l = 0
for num1 in list_inn_match:
    for num2 in list_inn:
        if (num1 == num2):
            temp = result.loc[result['ИНН'] == num1]
            file_name = temp.iloc[0]['Файл']
            result_1.loc[l] = [file_name, num1]
            l += 1
#data_ref.style.apply(lambda x: ["background: red" if v == 7703744408 else "" for v in x], axis = 1)

result_1['Ссылка'] = result_1['Файл']

writer = pd.ExcelWriter("output/result.xlsx", engine = 'xlsxwriter')
writer1 = pd.ExcelWriter("output/all.xlsx", engine = 'xlsxwriter')
#writer2 = pd.ExcelWriter("refffff.xlsx", engine = 'xlsxwriter')
#data_ref.to_excel(writer2, 'Sheet1')
#writer2.save()
result_1.to_excel(writer, 'Sheet1')
result.to_excel(writer1, 'Sheet1')
#worksheet = writer2.sheets['Sheet1']
#worksheet.write_url('D2', r'internal:Sheet1!A1')
writer.save()
writer1.save()
#writer2.save()

def style_specific_cell(x):
    color = 'backgrond_color: lightgreen'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    df1.iloc[2, 2] = color
    return df1

def color(x):
    c1 = 'color: #fffff; background-color: #ba3018'
    m = 1
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    df1.loc[m, ['config_size_x', 'config_size_y']] = c1
    return df1

#writer2 = pd.ExcelWriter("refref.xlsx", engine = 'xlsxwriter')
#data_ref.to_excel(writer2, 'Sheet1')
#data_ref.style.apply(style_specific_cell, axis=None)
#data_ref.to_excel(writer2, 'Sheet1')
#worksheet = writer2.sheets['Sheet1']
#worksheet.conditional_format('A1', {'type': 'cell',
#                                    'criteria': 'equal to',
#                                    'value': 5,
#                                    'format': red })
#writer2.save()

