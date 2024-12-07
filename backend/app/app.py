
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from scripts.stopwords import STOPWORDS
from scripts.search import search
import json
# Create a Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parliament.db'
db = SQLAlchemy(app)

CORS(app)  # Enable CORS for connecting with React

@app.route('/api', methods=['GET'])
def get_data():
    return jsonify({"message": "API is working!"})

@app.route('/search', methods=['POST'])
def searchEngine():
    data = request.json
    if not data:
        return jsonify({"Error": "Invalid JSON"}), 400
    
    name = data.get('name', '')
    date = data.get('date', '')
    political_party = data.get('politicalParty', '')
    keywords = data.get('keywords', '')

    
    print(name, date, political_party, keywords)
    search_results = search(name, date, political_party, keywords)
    search_results_json = json.loads(search_results.to_json(orient='records'))
    return jsonify(search_results_json)



if __name__ == '__main__':
    app.run(debug=True)
