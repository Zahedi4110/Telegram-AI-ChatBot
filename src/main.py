# src/main.py

import logging
import json
import time
from quart import Quart, request  # Import Quart instead of Flask
from helper.interaction_handler import handle_ask_command, handle_img_command
from helper.interaction_handler import handle_clean_command
from helper.telegram_api import sendMessage

# Load messages from JSON file
with open('messages.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Initialize logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Quart application
app = Quart(__name__)

# Global variables for interaction tracking
interaction_count = {}
user_last_interaction_time = {}
processing_flags = {}  # To track if a user is currently being processed


@app.route('/telegram', methods=['POST', 'GET'])
async def telegram():
    """Handles incoming messages from Telegram and responds accordingly."""
    try:
        data = await request.get_json()  # Use await to get JSON data
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
        words = query.split(' ')
        if query.startswith('/img'):
            await handle_img_command(
                sender_id, words, messages)  # Await async function
        elif query.startswith('/clean'):
            await handle_clean_command(
                sender_id, messages)  # Await async function
        else:
            # Treat any other input as a question for handle_ask_command
            await handle_ask_command(
                sender_id, words, interaction_count, messages)
                    # Await async function

    except Exception as e:
        logging.error(f"Error in processing: {e}")
        sendMessage(sender_id, messages["ERROR_PROCESSING"])

    finally:
        # Reset the processing flag
        processing_flags[sender_id] = False
        return "Welcome to the Telegram Bot API!", 200


if __name__ == '__main__':
    app.run(debug=True)