# Helper/interaction_handler/show_handler.py

from helper.telegram_api import send_message
from helper.memory import get_temp_memory, get_perm_memory


def handle_show_command(sender_id: int):
    """Handles the /show command to display user memory."""
    # Retrieve temporary and permanent memory for the user
    temp_memory = get_temp_memory(sender_id)
    perm_memory = get_perm_memory(sender_id)

    # Prepare messages to send to the user
    if temp_memory:
        temp_memory_message = f"*Temporary Memory:*\n{temp_memory}"
    else:
        temp_memory_message = "*Temporary Memory:*\nNo temporary memory recorded."

    if perm_memory:
        perm_memory_message = f"*Permanent Memory:*\n{perm_memory}"
    else:
        perm_memory_message = "*Permanent Memory:*\nNo permanent memory recorded."

    # Send the memory information to the user
    send_message(sender_id, temp_memory_message)
    send_message(sender_id, perm_memory_message)