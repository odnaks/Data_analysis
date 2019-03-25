import pandas as pd
import os
from os.path import join, getsize

files = os.listdir('datasets')
for file in files:
    if file.find('ratings_') == -1:
        files.remove(file)
data = pd.DataFrame(columns = ['one', 'two', 'tree', 'four'])
for filename in files:
    temp = pd.read_csv(os.path.join('datasets', filename), sep = ',',  names =['one', 'two', 'tree', 'four'])
    data = pd.concat([data, temp], axis = 0)
print (data)
