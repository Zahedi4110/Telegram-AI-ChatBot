# src/main.py

import logging
import json
import time
from flask import Flask, request
from helper.interaction_handler import handle_ask_command, handle_img_command
from helper.interaction_handler import handle_clean_command
from helper.telegram_api import sendMessage

# Load messages from JSON file
with open('messages.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Initialize logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask application
app = Flask(__name__)

# Global variables for interaction tracking
interaction_count = {}
user_last_interaction_time = {}
processing_flags = {}  # To track if a user is currently being processed


@app.route('/telegram', methods=['POST', 'GET'])
def telegram():
    """Handles incoming messages from Telegram and responds accordingly."""
    try:
        data = request.get_json()
        message = data['message']
        query = message['text'].strip()  # Strip leading/trailing whitespace
        sender_id = message['from']['id']

        # Initialize interaction count and processing flag if not present
        if sender_id not in interaction_count:
            interaction_count[sender_id] = 0
            user_last_interaction_time[sender_id] = time.time()
            processing_flags[sender_id] = False  # Initialize processing flag

        # Check if the user is already being processed
        if processing_flags[sender_id]:
            logging.info(f"User {sender_id} is already being processed.")
            return "Processing", 200  # Prevent re-processing

        # Set the processing flag
        processing_flags[sender_id] = True

        interaction_count[sender_id] += 1
        user_last_interaction_time[sender_id] = time.time()

        # Log user input
        logging.info(f"User Input: {query}")
        logging.info(f"Num OF Interaction: {interaction_count}")

        # Command processing logic
        if query.startswith('/img'):
            words = query.split(' ')
            handle_img_command(sender_id, words, messages)
        elif query.startswith('/clean'):
            words = query.split(' ')
            handle_clean_command(sender_id, messages)
        else:
            # Treat any other input as a question for handle_ask_command
            words = query.split(' ')
            handle_ask_command(sender_id, words, interaction_count, messages)

    except Exception as e:
        logging.error(f"Error in processing: {e}")
        sendMessage(sender_id, messages["ERROR_PROCESSING"])

    finally:
        # Reset the processing flag
        processing_flags[sender_id] = False
        return "Welcome to the Telegram Bot API!", 200


if __name__ == '__main__':
    app.run(debug=True)