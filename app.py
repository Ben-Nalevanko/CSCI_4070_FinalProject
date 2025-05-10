import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from flask import jsonify, Flask, request, render_template
from flask_cors import CORS
import csv
import os
import uuid

app = Flask(__name__, static_url_path='/static/')
CORS(app)

data = pd.DataFrame()
UPLOAD_FOLDER = "data_files"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/load_data", methods=["POST"])
def load_data():
	# downloads the file locally so the app can open it, not strictly necessary.
	if 'file' not in request.files:
		return jsonify({'message': 'No file part'}), 400
	file = request.files['file']
	if file.filename == '':
		return jsonify({'message': 'No selected file'}), 400
	if file:
		filename=file.filename
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(filepath)


	# loads contents into data, probably not a good idea. Should remove.
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
	requestData = request.get_json()
	print(requestData)
	filename = requestData["file"]
	print(filename)
	filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	data = pd.read_csv(filepath)

	#Tempory for testing
	features = ["area", "bedrooms", "bathrooms", "stories"]
	target = "price"

	if data is None:
		return jsonify({"error": "No data Loaded"}), 404
	#dummy values for testing, call training and testing algorithms
	match request.json.get("algorithm"):
		case "linreg":
			lin_reg_train(data, target, features)
		case "cluster":
			print("cluster")
	return jsonify({"text": "Finished"})
#load_data("test.csv")
#target = "price"
#features=["area", "bedrooms", "bathrooms", "stories"]

#model = lin_reg_train(data, target, features)
#lin_reg_test(model, target, features)

#Essentially a main method to run the app
if __name__ == "__main__":
	app.run(debug=True)
