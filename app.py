import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from flask import jsonify, Flask, request
import csv

app = Flask(__name__)
data = pd.DataFrame()

def load_data(filename):
	try:
		global data
		data = pd.read_csv(filename);
	except FileNotFoundError:
		print("Error: File not found")
	print(data)

def lin_reg_train(data, target, features):
	x = data[features]
	y = data[target]
	model = LinearRegression()
	model.fit(x,y)
	r_sq = model.score(x,y)

	print("R Squared: "+str(r_sq))

	return model

def lin_reg_test(trained_model, target, features):
	x = data[features]
	y = data[target]
	model = trained_model
	y_pred = model.predict(x)
	print(y_pred)

load_data("test.csv")
target = "price"
features=["area", "bedrooms", "bathrooms", "stories"]

model = lin_reg_train(data, target, features)
lin_reg_test(model, target, features)
