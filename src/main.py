# src/main.py

import logging
import json
import time
from flask import Flask, request
from helper.interaction_handler import (handle_ask_command,
                                         handle_img_command,
                                         handle_clean_command,
                                         handle_info_command)
from helper.telegram_api import send_message

# Load messages from JSON file
with open('messages.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask application
app = Flask(__name__)

# Global variables for interaction tracking
interaction_count = {}
user_last_interaction_time = {}

@app.route('/telegram', methods=['POST', 'GET'])
def telegram():
    """Handles incoming messages from Telegram and responds accordingly."""
    try:
        data = request.get_json()
        message = data['message']
        query = message['text']
        sender_id = message['from']['id']

        # Initialize interaction count if not present
        if sender_id not in interaction_count:
            interaction_count[sender_id] = 0
            user_last_interaction_time[sender_id] = time.time()

        interaction_count[sender_id] += 1
        user_last_interaction_time[sender_id] = time.time()

        # Split the message into words for command processing
        words = query.split(' ')
        logging.info(f"User Input: {query}")
        logging.info(f"Num OF Interaction: {interaction_count}")

        if words[0] == '/ask':
            handle_ask_command(sender_id, words, interaction_count, messages)

        elif words[0] == '/img':
            handle_img_command(sender_id, words, messages)

        elif words[0] == '/clean':
            handle_clean_command(sender_id, messages)

        elif words[0] == '/info':
            handle_info_command(sender_id, words, messages)

        else:
            send_message(sender_id, messages["UNRECOGNIZED_COMMAND"])

    except Exception as e:
        logging.error(f"Error in processing: {e}")
        send_message(sender_id, messages["ERROR_PROCESSING"])

    return "Welcome to the Telegram Bot API!", 200

if __name__ == '__main__':
    app.run(debug=True)