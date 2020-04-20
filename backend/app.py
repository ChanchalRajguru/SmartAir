from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from usDataCleaning import dataCleaning
import json
from bson import json_util, ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'averageCarbonPollution'
app.config['MONGO_URI']= 'mongodb://localhost:27017/averageCarbonPollution'
mongo = PyMongo(app)

@app.route('/status', methods=['GET'])
def hello_world():
    return 'OK running!'

@app.route('/map', methods=['GET'])
def carbonPollution():
    carbonData = mongo.db.carbonFeatureJsonList
    result = []
    finalResult = []
    for field in carbonData.find():
        # result.append({"type":field['type'],"features":field['features']})
        result.append(field)
    results = json.loads(json_util.dumps(result))
    finalResult = {"type":"FeatureCollection","features":results}
    return jsonify(finalResult), 200

@app.route('/forest', methods=['GET'])
def forestData():
    forestData = mongo.db.forestList
    result = []
    finalResult = []
    data = forestData.find_one()
    result.append(data)
    results = json.loads(json_util.dumps(result))
    finalResult = {"type":"FeatureCollection","features":results}
    return jsonify(finalResult), 200


###Setups the Initial Workflow for the app
# def setup_app(app):
#    dataCleaning()

# setup_app(app)

if __name__ == '__main__':
    app.run()
