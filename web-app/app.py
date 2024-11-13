from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import uuid
import datetime
import os

app = Flask(__name__)

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)  # Adjust the connection string if necessary
db = client['sentiment']  # Database name
collection = db['texts']  # Collection name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkSentiment', methods=['POST'])
def submit_sentence():
    data = request.get_json()
    sentence = data.get('sentence')

    # Generate a unique request_id
    request_id = str(uuid.uuid4())

    # Create the data structure with status "pending" and analysis as null
    document = {
        "request_id": request_id,
        "sentences": [
            {
                "sentence": sentence,
                "status": "pending",
                "analysis": None
            }
        ],
        "overall_status": "pending",
        "timestamp": datetime.datetime.utcnow()
    }

    # Insert into MongoDB
    collection.insert_one(document)

    # Return the user's input sentence
    return jsonify({'analysis': sentence})

if __name__ == '__main__':
    app.run(debug=True)
