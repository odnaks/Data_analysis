import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_excel("x.xlsx")
data2 = data.drop_duplicates('Куратор ИП')
name_curator = list(data2['Куратор ИП'])
for name in name_curator:
    if name == 0:
        name_curator.remove(0)
new = data.columns[1:]
#print (new)
#print (data.drop_duplicates('Статус акцепта куратора')['Статус акцепта куратора'])
data['date'] = pd.to_datetime(data["Дата документа"])
mask = (data['date'] >= '2019-01-01') & (data['date'] < '2019-02-01')
data = data.loc[mask]

result = pd.DataFrame(columns=['куратор', 'кол-во операций', 'кол-во ИП', 'валюта платежа', 'акцепт куратора'])
for i in range(len(name_curator)):
    tmp = data.loc[data['Куратор ИП'] == name_curator[i]]
    tmp2 = tmp.drop_duplicates('GUID объекта')
    tmp3 = data.loc[(data['Валюта платежа'] != 'RUR') &
                    (data['Куратор ИП'] == name_curator[i])].drop_duplicates('GUID объекта')
    tmp4 = data.loc[(data['Статус акцепта куратора'] == 'Акцептован') & (data['Куратор ИП'] == name_curator[i])]
    result.loc[i] = [name_curator[i], len(tmp), len(tmp2), len(tmp3), len(tmp4)]
sum_one = result['кол-во операций'].sum()
sum_two = result['кол-во ИП'].sum()
sum_three = result['валюта платежа'].sum()
sum_four = result['акцепт куратора'].sum()

result['кол-во операций(%)'] = result['кол-во операций'] / sum_one
result['кол-во ИП(%)'] = result['кол-во ИП'] / sum_two
result['валюта платежа(%)'] = result['валюта платежа'] / sum_three
result['акцепт куратора(%)'] = result['акцепт куратора'] / sum_four
#print(result)

writer = pd.ExcelWriter('jan19_table.xlsx', engine='xlsxwriter')
result.to_excel(writer, 'Sheet1')

worksheet = writer.sheets['Sheet1']
workbook = writer.book
worksheet.conditional_format('G2:J18', {'type': 'data_bar',
                                        'bar_solid': True,
                                        'bar_color':'#acf4a4'})
header_format = workbook.add_format({
    'bold':True,
    'text_wrap':True,
    'valign':'top',
    'fg_color':'#4575d4',
    'border':1})
for col_num, value in enumerate(result.columns.values):
    worksheet.write(0, col_num + 1, value, header_format)

cellColor = workbook.add_format({'fg_color':'#ff9340'})
worksheet.set_column(1, 1, 10, cellColor)
cellColor2 = workbook.add_format({'fg_color':'#acf4a4'})
worksheet.set_column(2, 5, 10, cellColor2)
worksheet.set_column(0,10,20)
writer.save()

x = result['куратор']
z1 = result['кол-во операций(%)']
z2 = result['кол-во ИП(%)']
z3 = result['валюта платежа(%)']
z4 = result['акцепт куратора(%)']
eps = 0.2

fig = plt.figure()
rect1 = plt.barh(x, z1, height=0.2)
rect2 = plt.barh(np.arange(-eps, len(name_curator) - eps), z2, height=0.2)
rect3 = plt.barh(np.arange(-eps*2, len(name_curator) - eps*2), z3, height=0.2)
rect4 = plt.barh(np.arange(eps, len(name_curator) + eps), z4, height=0.2)
plt.title('январь 2019')
#plt.grid(True)
plt.legend((rect1[0], rect2[0], rect3[0], rect4[0]), ('кол-во операций', 'кол-во ИП', 'нерезиденты', 'акцепт куратора'))

fig = plt.gcf()
fig.set_size_inches((15, 11))
fig.savefig("jan19.png", dpi=500)
#plt.show()
