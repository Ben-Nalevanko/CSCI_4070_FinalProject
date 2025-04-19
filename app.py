import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from flask import jsonify, Flask, request
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

data = pd.DataFrame()
UPLOAD_FOLDER = "data_files"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/load_data", methods=["GET", "POST"])
def load_data():
	# downloads the file locally so the app can open it
	if 'file' not in request.files:
		return jsonify({'message': 'No file part'}), 400
	file = request.files['file']
	if file.filename == '':
		return jsonify({'message': 'No selected file'}), 400
	if file:
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		file.save(filepath)


	# loads contents into data
	try:
		print("try")
		global data
		data = pd.read_csv(filepath)
		print(data)
	except FileNotFoundError:
		print("Error");

	return jsonify({'message': 'File uploaded successfully'}), 200

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

# After loading the data
# Runs training and testing
# Called by script.js
@app.route("/run", methods=["GET", "POST"])
def run():
	if data is None:
		return jsonify({"error": "No data Loaded"}), 404
	#dummy values for testing, call training and testing algorithms
	match request.json.get("algorithm"):
		case "linreg":
			print("linreg")
		case "cluster":
			print("cluster")

#load_data("test.csv")
#target = "price"
#features=["area", "bedrooms", "bathrooms", "stories"]

#model = lin_reg_train(data, target, features)
#lin_reg_test(model, target, features)

#Essentially a main method to run the app
if __name__ == "__main__":
	app.run(debug=True)
