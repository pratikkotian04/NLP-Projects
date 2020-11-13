from flask import Flask, jsonify, request
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import pandas as pd

user_data = pd.read_excel("Travel_Destination.xlsx")
import datefinder
from pymongo import MongoClient

nlp = spacy.load("en_core_web_sm")
filename = "final_model.sav"  ## Logistic Regression Binary Saved Model
load_model = pickle.load(open(filename, "rb"))
client = MongoClient("mongodb://localhost:27017/?readPreference=primary")
db = client["travel_data"]
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(binary=True)
X = cv.fit_transform(user_data["Text"])

app = Flask(__name__)


@app.route("/get_info", methods=["POST"])
def get_info():
    data = request.get_json()
    text = data["text"]
    msg = cv.transform([text])
    travel_predict = load_model.predict(msg)[0]
    data["Journey_Type"] = travel_predict
    data = extract_info(text, data)
    print(data)
    return (
        jsonify({"response_data": data, "success": True}),
        200,
    )


def extract_info(text, data):

    doc = nlp(text)
    db_data = db.info_data.find_one({}, {"_id": 0})
    places = db_data["places"]
    for token in doc:
        if token.text in places:
            index = text.split().index(token.text)
            data[str(doc[index].nbor(-1))] = token.text

    if "to" in data.keys() and "from" in data.keys():
        pass
    elif "to" in data.keys():
        data["from"] = "Where do you want to board your flight from?"
    elif "from" in data.keys():
        data["to"] = "Where do you want to go ?"
    else:
        pass

    data["Onward_Time"] = [i for i in datefinder.find_dates(text)]
    data["WeekDays"] = [i for i in db_data["weekDays"] if i in text.split()]
    data["Events"] = [i for i in db_data["events"] if i in text.split()]
    data["Departure_Time"] = [
        j for i, j in db_data["time"].items() if i in text.split()
    ]

    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

