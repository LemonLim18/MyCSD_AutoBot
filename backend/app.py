import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import subprocess

# Setup the Flask Application for the backend server, which it will handle the API requests
app = Flask(__name__)
CORS(app)  # Enable CORS for the app

# Variable to keep track of the bot process
bot_process = None

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
        json.dump(data, f, indent=4)  # Write the JSON data to the file with an indentation of 4 spaces

    return jsonify({"message": "User data saved successfully"}), 200  # Return a JSON response with a status of 200 to the frontend

# Route for starting the Telegram bot [Receive a POST request at http://127.0.0.1:5000/start-bot]
@app.route('/start-bot', methods=['POST'])
def start_bot():
    global bot_process

    print("START")
    print("Checking the bot process: ", bot_process)
    
    # Check if bot_process is not None before calling poll()
    if bot_process is not None:
        if bot_process.poll() is None:
            return jsonify({"message": "Bot is already running"}), 400  # Bot is still running

    try:
        # Start the telebot.py logic here
        # subprocess can capture the output or error message from the script
        bot_process = subprocess.Popen(["python", "telebot.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # If the Telebot.py script runs successfully, return a success message
        return jsonify({"message": "Bot started successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error starting bot: {str(e)}"}), 500


# Route for stopping the Telegram bot
@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global bot_process

    print("STOP")
    print("Checking the bot process: ", bot_process)

    # Check if bot_process is not None before calling poll()
    if bot_process is not None:
        print("Checking the bot process poll: ", bot_process.poll())  # This line will be safe now
        if bot_process.poll() is None:  # Check if the bot process is running
            bot_process.terminate()  # Terminate the bot process
            bot_process.wait()  # Wait for the process to finish
            return jsonify({"message": "Bot stopped successfully"}), 200
        else:
            return jsonify({"message": "Bot is not running"}), 400  # Bot has already stopped
    else:
        return jsonify({"message": "Bot is not running"}), 400  # Bot process was never started

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode


# -------------- HOW TO START THE FLASK SERVER-----------------------------

# To start the Flask server, run the following command in the terminal:
# 1. \venv\Scripts\activate: to start the virtual environment
# 2. echo %FLASK_APP%: to check if the FLASK_APP is set
# 3. set FLASK_APP=app.py: to set the FLASK_APP environment variable to our main app
# 4. flask run: to start the Flask server
# 5. OR python app.py: to start the Flask server
# ------------------------------------------------------------------------