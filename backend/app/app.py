
from flask import Flask, jsonify, request, send_file
from scripts.lsi_model import create_lsi_model, get_lsi_vectors
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from scripts.stopwords import STOPWORDS
from scripts import clustering 
from scripts.similarity import get_top_similar_members
from scripts.search import search
from scripts.group import group_by_speech, group_by_party, group_by_member_name, group_by_date
import json
import os


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

@app.route('/groupedData', methods=['POST'])
def getGroupedData():
    grouped_by = request.json.get('grouped_by', '')
    switcher = {
        "member_name": group_by_member_name() if grouped_by == "member_name" else None,
        "speech": group_by_speech() if grouped_by == "speech" else None,
        "party": group_by_party() if grouped_by == "party" else None,
        "date": group_by_date() if grouped_by == "date" else None
    }

    return jsonify(switcher.get(grouped_by).to_json(orient='records'))


@app.route('/similarity', methods=['GET'])
def compute_similarity():
    top_similar = get_top_similar_members()
    print(top_similar)
    return jsonify(top_similar)

@app.route('/lsi')
def lsi():
    # Build the LSI model
    lsi_model, dictionary, doc_term_matrix = create_lsi_model(num_topics=7)

    # Transform speeches into LSI vectors
    lsi_vectors = get_lsi_vectors(lsi_model, doc_term_matrix)

    # Convert LSI vectors to JSON serializable format
    lsi_vectors_serializable = []
    for vec in lsi_vectors:
        vec_serializable = [(int(topic), float(weight)) for topic, weight in vec]
        lsi_vectors_serializable.append(vec_serializable)
    
    return jsonify(lsi_vectors_serializable)

@app.route('/clustering')
def Clustering():
    plot_path = clustering.kmeans()
    if not os.path.exists(plot_path):
        return "Error: Cluster plot was not generated.", 500  # Return HTTP 500 error
    return send_file(plot_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

