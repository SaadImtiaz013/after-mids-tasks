#ai lab task 10
import pandas as pd
import numpy as np
data = pd.read_csv('data.csv', sep=None, engine='python', on_bad_lines='skip')
print('We have {} rows.'.format(data.shape[0]))
print('We have {} columns'.format(data.shape[1]))
print(np.sum(pd.isnull(data)))
for col in data.columns:
    if data[col].isnull().any():
        num = data[col].mode()[0]
        data[col] = data[col].fillna(num)
if 'show_id' in data.columns:
    data.drop('show_id', axis=1, inplace=True)
print(data.dtypes)
cat_columns = data.select_dtypes(['object']).columns
data[cat_columns] = data[cat_columns].apply(lambda x: pd.factorize(x)[0])
print(data.dtypes)
x = data.iloc[:, 0:-1]
print(x.shape)
y = data.iloc[:, -1]
print(y.shape)