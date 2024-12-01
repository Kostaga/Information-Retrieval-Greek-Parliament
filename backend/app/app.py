
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from scripts.stopwords import STOPWORDS
from scripts.dataCleaning import to_lowercase, remove_punctuation_and_numbers, stem_words

# Create a Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parliament.db'
db = SQLAlchemy(app)

CORS(app)  # Enable CORS for connecting with React

@app.route('/api', methods=['GET'])
def get_data():
    return jsonify({"message": "API is working!"})

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    if not data:
        return jsonify({"Error": "Invalid JSON"}), 400
    
    name = data.get('name', '')
    date = data.get('date', '')
    political_party = data.get('politicalParty', '')
    keywords = data.get('keywords', '')

    # Apply preprocessing functions
    keywords = to_lowercase(keywords)
    keywords = ' '.join([remove_punctuation_and_numbers(word) for word in keywords.split()])
    keywords = ' '.join([stem_words(word) for word in keywords.split()])
    
    print(name, date, political_party, keywords)

    return jsonify({
        "name": name,
        "date": date,
        "political_party": political_party,
        "keywords": keywords
    })


if __name__ == '__main__':
    app.run(debug=True)
