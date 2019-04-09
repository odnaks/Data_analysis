import pandas as pd
import time
import numpy as np
import sys

########################################################################

file1 = "datasets/feb.xlsx" # входной
file2 = "datasets/proj.xlsx" # список всех проектов

file3 = "out_credit_stat/table.xlsx" # выходная сводка (основная)
file4 = "out_credit_stat/data.xlsx" # выходная таблица (общая)

################################### Строки

########### Причины заключения договора на БС
str1_1 = "214-ФЗ + Кредит"
str1_2 = "963+БГ"
str1_3 = "Банковская гарантия"
str1_4 = "Контрактное кредитование"
str1_5 = "Кредитование + Банковская гарантия"

##########
str2_1 = "Акцептован"
str2_2 = "Отказан"

#########
T0 = "T"
T1 = "T+1"
T2 = "T+2"
T3 = "T+3"
T4 = "T+4"
T5 = "T+5"
T6 = "T+6"

#########
str3_1 = "Операция не соответствует режиму (целевому назначению) счета"
str3_2 = "Не предоставлены обосновывающие документы"
str3_3 = "Предоставлен не полный комплект обосновывающих документов"

#########
str4_1 = "Нецелевое назначение"
str4_2 = "Замечания к об.док"
str4_3 = "Прочее"

######### Для нового файла
str5_1 = "T"
str5_2 = "T+1"
str5_3 = "T+2..6"
str5_4 = "Акцептовано"
str5_5 = " "
str5_6 = "Всего"
str5_7 = "Отказано"
str5_9 = "Обработано"

#################################### Колонки

col1 = "Причина заключения договора на БС"
col2 = "Состояние контроля"
col3 = "hour"
col4 = "bussDays"
col5 = "hour_b"
col6 = "T"
col7 = "Причина отказа"
col8 = "GUID объекта"
col9 = "Начало контроля"
col10 = "Завершение контроля"
col11 = "Причина (обобщ.)"
col12 = "Сумма"

######### Для нового файла
col1_1 = "Период"
col1_2 = "Сумма"
col1_3 = "Кол-во"
col1_4 = " "
col1_5 = "Причина отказа"

###################################################################

def hour_bin(row):
    if (row[col3] > 18):
        return 1
    else:
        return 0
def var_t(row):
    if ((row[col1] == str1_1  or row[col1] == str1_2 or row[col1] == str1_3 or row[col1] == str1_4 or row[col1] == str1_5)
            and (row[col2] == str2_1 or row[col2] == str2_2)):
        if (row[col4] == 0):
            return (T0)
        elif (row[col4] == 1):
            if (row[col5] == 1):
                return (T0)
            else:
                return (T1)
        elif (row[col4] == 2):
            if (row[col5] == 1):
                return (T1)
            else:
                return (T2)
        elif (row[col4] == 3):
            if (row[col5] == 1):
                return (T2)
            else:
                return (T3)
        elif (row[col4] == 4):
            if (row[col5] == 1):
                return (T3)
            else:
                return (T4)
        elif (row[col4] == 5):
            if (row[col5] == 1):
                return (T4)
            else:
                return (T5)
        elif (row[col4] == 6):
            if (row[col5] == 1):
                return (T5)
            else:
                return (T6)
        else:
            return (T6)

def prich_o(row):
    if (row[col2] == str2_2 and (row[col6] == T0 or row[col6] == T1 or row[col6] == T2 or row[col6] == T3 or row[col6] == T4 or row[col6] == T5 or row[col6] == T6)):
        if (row[col7] == str3_1):
            return (str4_1)
        elif (row[col7] == str3_2 or row[col7] == str3_3):
            return (str4_2)
        else:
            return (str4_3)

################################################################

if len(sys.argv) > 1:
    data = pd.read_excel(sys.argv[1])
else:
    data = pd.read_excel(file1)
proj = pd.read_excel(file2)

data = pd.merge(data, proj[[col8, col1]], on = col8, how='left')

######################

data[col4] = np.busday_count( data[col9].values.astype('datetime64[D]'), data[col10].values.astype('datetime64[D]'))
data[col3] = data[col9].dt.hour
data[col5] = data.apply(hour_bin, axis = 1)
data[col6] = data.apply(var_t, axis = 1)
data[col11] = data.apply(prich_o, axis = 1)

#####################

data_ak = data[data[col2] == str2_1]
count_t = len(data_ak[data_ak[col6] == T0])
count_t_one = len(data_ak[data_ak[col6] == T1])
count_t_two = len(data_ak[data_ak[col6] == T2]) + len(data_ak[data_ak[col6] == T3]) + len(data_ak[data_ak[col6] == T4]) + len(data_ak[data_ak[col6] == T5]) + len(data_ak[data_ak[col6] == T6])

sum_t = data_ak[data_ak[col6] == T0][col12].sum()
sum_t_one = data_ak[data_ak[col6] == T1][col12].sum()
sum_t_two = data_ak[data_ak[col6] == T2][col12].sum() + data_ak[data_ak[col6] == T3][col12].sum() + data_ak[data_ak[col6] == T4][col12].sum() + data_ak[data_ak[col6] == T5][col12].sum() + data_ak[data_ak[col6] == T6][col12].sum()

new_data = pd.DataFrame([[str5_1, sum_t, count_t]], columns = [col1_1, col1_2, col1_3])
col = [col1_1, col1_2, col1_3]
new_data = new_data.append(pd.DataFrame([[str5_2, sum_t_one, count_t_one]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_3, sum_t_two, count_t_two]], columns = [col1_1, col1_2, col1_3]), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_6, sum_t + sum_t_one + sum_t_two, count_t + count_t_one + count_t_two]], columns = [col1_1, col1_2, col1_3]), ignore_index=True)

new_data = new_data.append(pd.DataFrame([[str5_4, str5_5, str5_5]], columns = col), ignore_index=True)

####################

new_data = new_data.append(pd.DataFrame([[str5_5, str5_5, str5_5]], columns = col), ignore_index=True)

data_ak = data[data[col2] == str2_2]
count_t = len(data_ak[data_ak[col6] == T0])
count_t_one = len(data_ak[data_ak[col6] == T1])
count_t_two = len(data_ak[data_ak[col6] == T2]) + len(data_ak[data_ak[col6] == T3]) + len(data_ak[data_ak[col6] == T4]) + len(data_ak[data_ak[col6] == T5]) + len(data_ak[data_ak[col6] == T6])

sum_t = data_ak[data_ak[col6] == T0][col12].sum()
sum_t_one = data_ak[data_ak[col6] == T1][col12].sum()
sum_t_two = data_ak[data_ak[col6] == T2][col12].sum() + data_ak[data_ak[col6] == T3][col12].sum() + data_ak[data_ak[col6] == T4][col12].sum() + data_ak[data_ak[col6] == T5][col12].sum() + data_ak[data_ak[col6] == T6][col12].sum()

new_data = new_data.append(pd.DataFrame([[str5_1, sum_t, count_t]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_2, sum_t_one, count_t_one]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_3, sum_t_two, count_t_two]], columns = [col1_1, col1_2, col1_3]), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_6, sum_t + sum_t_one + sum_t_two, count_t + count_t_one + count_t_two]], columns = [col1_1, col1_2, col1_3]), ignore_index=True)

new_data = new_data.append(pd.DataFrame([[str5_7, str5_5, str5_5]], columns = col), ignore_index=True)

###################

new_data = new_data.append(pd.DataFrame([[str5_5, str5_5, str5_5]], columns = col), ignore_index=True)

data_ak = data[(data[col1] == str1_1) | (data[col1] == str1_2) | (data[col1] == str1_3) | (data[col1] == str1_4) | (data[col1] == str1_5)]
data_ak = data_ak[data_ak[col2] == str2_2]
sum_pr = len(data_ak) # all
nec_naz = len(data_ak[data_ak[col7] == str3_1])
zamech = len(data_ak[(data_ak[col7] == str3_2) | (data_ak[col7] == str3_3)])
proch = sum_pr - nec_naz - zamech

new_data = new_data.append(pd.DataFrame([[col1_4, col1_5, col1_3]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_5, str4_1, nec_naz]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_5, str4_2, zamech]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_5, str4_3, proch]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_5, str5_5, sum_pr]], columns = col), ignore_index=True)

###################

new_data = new_data.append(pd.DataFrame([[str5_5, str5_5, str5_5]], columns = col), ignore_index=True)

data_ak = data[(data[col2] == str2_2) | (data[col2] == str2_1)]
count_t = len(data_ak[data_ak[col6] == T0])
count_t_one = len(data_ak[data_ak[col6] == T1])
count_t_two = len(data_ak[data_ak[col6] == T2]) + len(data_ak[data_ak[col6] == T3]) + len(data_ak[data_ak[col6] == T4]) + len(data_ak[data_ak[col6] == T5]) + len(data_ak[data_ak[col6] == T6])

sum_t = data_ak[data_ak[col6] == T0][col12].sum()
sum_t_one = data_ak[data_ak[col6] == T1][col12].sum()
sum_t_two = data_ak[data_ak[col6] == T2][col12].sum() + data_ak[data_ak[col6] == T3][col12].sum() + data_ak[data_ak[col6] == T4][col12].sum() + data_ak[data_ak[col6] == T5][col12].sum() + data_ak[data_ak[col6] == T6][col12].sum()

new_data = new_data.append(pd.DataFrame([[str5_1, sum_t, count_t]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_2, sum_t_one, count_t_one]], columns = col), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_3, sum_t_two, count_t_two]], columns = [col1_1, col1_2, col1_3]), ignore_index=True)
new_data = new_data.append(pd.DataFrame([[str5_6, sum_t + sum_t_one + sum_t_two, count_t + count_t_one + count_t_two]], columns = [col1_1, col1_2, col1_3]), ignore_index=True)

new_data = new_data.append(pd.DataFrame([[str5_9, str5_5, str5_5]], columns = col), ignore_index=True)

##################

new_data.set_index(col1_1, inplace=True)
writer = pd.ExcelWriter(file3, engine='xlsxwriter')
new_data.to_excel(writer, 'Sheet1')

workbook = writer.book
worksheet = writer.sheets['Sheet1']

######

yellow = workbook.add_format({'bg_color': '#ffff00'})
worksheet.conditional_format("A2:C5", {'type': 'unique',
                                    'format': yellow})
worksheet.conditional_format("A8:C11", {'type': 'unique',
                                        'format': yellow})
worksheet.conditional_format("A15:C18", {'type': 'unique',
                                        'format': yellow})
worksheet.conditional_format("A20:C23", {'type': 'unique',
                                        'format': yellow})

######

akc = workbook.add_format({'bg_color': '#f4c542'})
worksheet.conditional_format("A6", {'type': 'unique',
                                    'format': akc})
worksheet.conditional_format("A12", {'type': 'unique',
                                    'format': akc})
worksheet.conditional_format("A24", {'type': 'unique',
                                    'format': akc})
worksheet.conditional_format("B14:C14", {'type': 'unique',
                                    'format': akc})

######

worksheet.set_column(1, 1, 25)
worksheet.set_column(0, 0, 20)
writer.save()

####################

writer_test = pd.ExcelWriter(file4, engine='xlsxwriter')
data.to_excel(writer_test, 'Sheet1')
writer_test.save()
