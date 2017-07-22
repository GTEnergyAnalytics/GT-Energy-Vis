# We'll render HTML templates and access data sent by GET
# using the request object from flask. jsonigy is required
# to send JSON as a response of a request
from flask import Flask, render_template, request, jsonify
import pickle
import sys
from sklearn.externals import joblib
import sklearn
import ast
import pandas as pd
import xgboost

model = pickle.load(open('static/data/culc.xgb.pickle.dat', 'rb'))
# content = 0
# with open('serializedpandas/dataArr.pkl', 'rb') as pickle_file:
#     content = pickle.load(pickle_file)
#from FinalAlgo import *
# Initialize the Flask application

# print contents
app = Flask(__name__)


data = pd.read_csv('static/data/energy_weather_schedule_dummies.csv')
# print(data.describe())

x = data.iloc[:, 6:]
y = data['power']

x_train = x.iloc[:17515, ]
x_test = x.iloc[17515: ]
y_train = y[:17515]
y_test = y[17515:]


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
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

@app.route('/_calculate_hist', methods=['GET'])
def calculate_hist():
    if request.method == 'GET':
        datetime = request.args.get('datetime', 'whoops', type=str)
        num_classes = request.args.get('num_classes', 'whoops', type=str)
        temp = request.args.get('temp', 'whoops', type=str)
        num_students = request.args.get('num_students', 'whoops', type=str)

        # time = request.args.get('time', 'whoops', type=str)
        #process data
        datetime = list(datetime)
        datetime[-6] = ' '
        datetime[-2:] = '00'
        datetime = datetime + [':00']
        datetime = ''.join(datetime)
        row = data.loc[data['date.time']==datetime]
        row['num.classes'] = int(num_classes)
        maxPower = data['power'].max()
        print maxPower
        if (row.shape[0] == 1):
            cols = row.iloc[:, 5:]
            actual = int(row['power'])
            expected = int(model.predict(cols)[0])
            return jsonify(success=True, truth=actual, prediction=expected)
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
        print data2.loc[(data2['num.classes']!=0), 'num.classes'].head()
        data2['num.classes'].astype(int)
        data2.loc[(data2['num.classes']!=0), 'num.classes'] += num_classes
        #data2.loc[(data2['num.classes']!=0), 'num.classes'] + num_classes
        data2['Temperature'] = data2['Temperature'].astype(int) + temp
        data2.loc[(data2['num.students']!=0), 'num.students'] += num_students
        # data2['Temperature'] += temp

        data2['predictPower'] = model()


        # time = request.args.get('time', 'whoops', type=str)
        #process data
        


if __name__ == '__main__':
    app.run()
