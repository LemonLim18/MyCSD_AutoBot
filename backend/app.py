from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for the app

# Route for the root URL
@app.route('/')
def index():
    return "Welcome to the Flask API!"  # Add a welcome message for the root URL

# Route for handling form submissions
@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.json  # Get the JSON data from the request from the frontend
    user_file = f"{data['name'].lower().replace(' ', '')}.json"  # Create a filename based on the lowercase name with no spaces

    # Save the user data in a JSON file
    with open(user_file, 'w') as f:  # Open the file in write mode (**Or Create**)
        json.dump(data, f)  # Write the JSON data to the file

    return jsonify({"message": "User data saved successfully"}), 200  # Return a JSON response with a status of 200 to the frontend

# Route for starting the Telegram bot [Receive a POST request at http://127.0.0.1:5000/start-bot]
@app.route('/start-bot', methods=['POST'])
def start_bot():
    # Start the telebot.py logic here
    os.system("python telebot.py")  # Run the telebot.py script
    return jsonify({"message": "Bot started successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
