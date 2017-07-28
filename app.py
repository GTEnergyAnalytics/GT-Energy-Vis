#Import libraries

from flask import Flask, render_template, request, jsonify
import pickle
import sys
from sklearn.externals import joblib
import sklearn
import ast
import pandas as pd
import xgboost

model = pickle.load(open('static/data/culc.xgb2.pickle.dat', 'rb'))
model1 = pickle.load(open('static/data/culc.xgb.pickle.dat', 'rb'))


# print contents
app = Flask(__name__)


data = pd.read_csv('static/data/energy_weather_schedule_dummies.csv')
labels_df = pd.read_csv('static/data/labels.csv')
# print(data.describe())

x = data.iloc[:, 6:]
y = labels_df['power']

x_train = x.iloc[:17515, ]
x_test = x.iloc[17515: ]
y_train = y[:17515]
y_test = y[17515:]


# Basic route for displaying webpage
@app.route('/')
def index():
    return render_template('index.html')

# Route that will process the AJAX request, sum up two
# integer numbers (defaulted to zero) and return the
# result as a proper JSON response (Content-Type, etc.)
# @app.route('/_add_numbers', methods=['GET'])
# def add_numbers():
#     #creating the features vector

#     index = 0
#     PCAOne = 0
#     PCANine = 0
#     PCAEight = 0
#     PCAFour = 0
#     if request.method == 'GET':
#         data = request.json    
#         temp = request.args.get('dictionary')
#         tempOne = ast.literal_eval(temp)
#         print(tempOne)
#         for k in tempOne:
#             if k == 'PCAOne':
#                 PCAOne = tempOne[k]
#             elif k == 'PCANine':
#                 PCANine = tempOne[k]
#             elif k == 'PCAFour':
#                 PCAFour = tempOne[k]
#             elif k == 'PCAEightVal':
#                 PCAEight = tempOne[k]
#             elif k == "ID":
#                 index = int(tempOne[k])
#     # predictMe = content[index]
#     predictMe[0] = PCANine
#     predictMe[1] = PCAEight
#     predictMe[2] = PCAFour
#     predictMe[3] = PCAOne
#     print(predictMe)


#     # prediction = model.predict_proba(predictMe)
#     # print(prediction)
#     return jsonify(result=prediction[0][0])

#route to calculate historical values
@app.route('/_calculate_hist', methods=['GET'])
def calculate_hist():
    if request.method == 'GET':
        datetime = request.args.get('datetime', 'whoops', type=str)
        num_classes = request.args.get('num_classes', 0, type=int)
        temp = request.args.get('temp', 0, type=float)
        num_students = request.args.get('num_students', 0, type=int)

        # format datetime
        datetime = list(datetime)
        datetime[-6] = ' '
        datetime[-2:] = '00'
        datetime = datetime + [':00']
        datetime = ''.join(datetime)

        # get historical data
        print datetime
        row = data.loc[data['date.time']==datetime].copy()
        print row
        power = labels_df.loc[labels_df['date.time']==datetime].copy()
        print power
        # update values with deltas
        row['num.classes'] += int(num_classes)
        row['Temperature'] += int(temp)
        row['num.students'] += int(num_students)

        # getting maximum power
        # maxPower = data['power'].max()
        # print maxPower
        if (row.shape[0] == 1):
            cols = row.iloc[:, 5:]
            actual = int(power['power'])
            expected = int(model1.predict(cols)[0])
            return jsonify(success=True, truth=actual, prediction=expected)
            # return jsonify(success=True, prediction=expected)
        else:
            print 'Not successful'
            return jsonify(success=False)

@app.route('/_time_series', methods=['GET'])
def time_series():
    if request.method == 'GET':
        num_classes = request.args.get('num_classes', 'whoops', type=int)
        temp = request.args.get('temp', 'whoops', type=int)
        num_students = request.args.get('num_students', 'whoops', type=int)

        data2 = data.copy()
        data2['num.classes'].astype(int)
        data2.loc[(data2['num.classes']!=0), 'num.classes'] += num_classes
        data2['Temperature'] = data2['Temperature'].astype(int) + temp
        data2.loc[(data2['num.students']!=0), 'num.students'] += num_students

        # predict power usage for all time points
        data2['predictPower'] = model1.predict(data2.iloc[:, 5:])
        power = []
        powerPredict = []
        months = []
        x = 0
        for i in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December']:
            monthData = data2.loc[data2['month{}'.format(i)] == 1, ['power', 'predictPower']]
            power.append(monthData['power'].sum())
            powerPredict.append(int(monthData['predictPower'].sum()))
            months.append(i)
            x += 1

            # time = request.args.get('time', 'whoops', type=str)
        #process data
        return jsonify({'success':True, 'prediction':powerPredict, 'months':months})
        


if __name__ == '__main__':
    app.run()
