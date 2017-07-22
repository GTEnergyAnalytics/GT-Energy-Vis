from flask import Flask, render_template, request, jsonify
import pickle
from sklearn.externals import joblib
import ast

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'