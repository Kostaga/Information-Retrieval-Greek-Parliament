from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parliament.db'
db = SQLAlchemy(app)

CORS(app)  # Enable CORS for connecting with React

@app.route('/api', methods=['GET'])
def get_data():
    return jsonify({"message": "API is working!"})


# @app.route('/search', methods=['POST'])
# def search():
#     data = request.json
#     name = data.get('name', '')
#     date = data.get('date', '')
#     political_party = data.get('politicalParty', '')
#     keywords = data.get('keywords', '')

#     results = df.copy()
#     if name:
#         results = results[results['name'].str.contains(name, na=False)]
#     if date:
#         results = results[results['date'] == date]
#     if political_party:
#         results = results[results['political_party'].str.contains(political_party, na=False)]
#     if keywords:
#         results = results[results['speech'].str.contains(keywords, na=False)]

#     # Return the filtered results
#     return results.head(10).to_json(orient='records')



if __name__ == '__main__':
    app.run(debug=True)
