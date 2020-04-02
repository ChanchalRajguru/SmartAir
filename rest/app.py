from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
# from flask.ext.pymongo import PyMongo


app = Flask(__name__)

@app.route('/status', methods=['GET'])
def hello_world():
    return 'OK running!'


# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)
# print(mongo)

if __name__ == '__main__':
    app.run()
