import pandas as pd

""" Наша задача - написать гео-классификатор, который каждой строке
сможет выставить географическую принадлежность определенному региону.
Т. е. если поисковый запрос содержит название города региона,
то в столбце 'region' пишется название этого региона.
Если поисковый запрос не содержит названия города, то ставим
'undefined'. Какое количество строк пришлось на Дальний Восток?"""

geo_data = {
    'Центр': ['москва', 'тула', 'ярославль'],
    'Северо-Запад': ['петербург', 'псков', 'мурманск'],
    'Дальник Восток': ['владивосток', 'сахалин', 'хабаровск']
}

def geo_classification(row):
    parsed = row['keyword']
    for region, city_list in geo_data.items():
        for city in city_list:
            if parsed.find(city) != -1:
                return region
    return "undefined"

data = pd.read_csv('datasets/keywords.csv')
#print (data.head())
data['region'] = data.apply(geo_classification, axis = 1)
data = data.groupby('region').sum()
print (data.sort_values(by = 'shows'))
