from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from usDataCleaning import dataCleaning

app = Flask(__name__)

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["carbonPollution"]
# mycol = mydb["carbonFeatureJson"]

app.config['MONGO_DBNAME'] = 'carbonPollution'
app.config['MONGO_URI']= 'mongodb://localhost:27017/carbonPollution'
mongo = PyMongo(app)

@app.route('/status', methods=['GET'])
def hello_world():
    return 'OK running!'

@app.route('/map', methods=['GET'])
def carbonPollution():
    carbonData = mongo.db.carbonFeatureJson
    result = []
    for field in carbonData.find():
        result.append({"type":field['type'],"features":field['features']})
    return jsonify(result), 200


#Setups the Initial Workflow for the app
# def setup_app(app):
#     pass
# #    dataCleaning()

# setup_app(app)

if __name__ == '__main__':
    app.run()
