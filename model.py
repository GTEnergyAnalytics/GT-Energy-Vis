import pickle
import pandas as pd

data = pd.read_csv('Data/en.csv')
print(data.describe())

x = data.iloc[:, 6:]
y = data['power']

x_train = x.iloc[:17515, ]
x_test = x.iloc[17515: ]
y_train = y[:17515]
y_test = y[17515:]



pred_y = model.predict(x_test)