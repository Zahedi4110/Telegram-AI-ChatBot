# src/main.py

import logging
import json
from flask import Flask, request
from helper.telegram_api import send_message
from helper.interaction_handler.ask_handler import handle_ask_command
from helper.interaction_handler.img_handler import handle_img_command
from helper.interaction_handler.clean_handler import handle_clean_command
from helper.interaction_handler.info_handler import handle_info_command
from helper.interaction_handler.show_handler import handle_show_command



# Load messages from JSON file
with open('messages.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask application
app = Flask(__name__)

# Global variables for interaction tracking
interaction_count = {}


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

        interaction_count[sender_id] += 1

        logging.info(f"User Input: {query}")

        if query.startswith('/ask'):
            handle_ask_command(
                sender_id, query.split(),
                interaction_count, messages)
        elif query.startswith('/img'):
            handle_img_command(sender_id, query.split(), messages)
        elif query.startswith('/clean'):
            handle_clean_command(sender_id, messages)
        elif query.startswith('/info'):
            handle_info_command(sender_id, query.split(), messages)
        elif query.startswith('/show'):  # Check for the /show command
            handle_show_command(sender_id)  # Call the show handler
        else:
            send_message(sender_id, messages["UNRECOGNIZED_COMMAND"])

    except Exception as e:
        logging.error(f"Error in processing: {e}")
        send_message(sender_id, messages["ERROR_PROCESSING"])

    return "Welcome to the Telegram Bot API!", 200


if __name__ == '__main__':
    app.run(debug=True)