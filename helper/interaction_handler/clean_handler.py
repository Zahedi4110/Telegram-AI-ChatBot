# Helper/interaction_handler/clean_handler.py

from helper.telegram_api import send_message
from helper.memory import clear_temp_memory, get_temp_memory


def handle_clean_command(sender_id: int, messages: dict):
    previous_memory = get_temp_memory(sender_id)
    
    if previous_memory:
        send_message(
            sender_id, f"Summary of cleared memory:\n{previous_memory}")
        clear_temp_memory(sender_id)
        send_message(sender_id, messages["MEMORY_CLEARED"])
    else:
        send_message(sender_id, messages["NO_CONVERSATION"])
    send_message(sender_id, messages["CLEAN_START"])
