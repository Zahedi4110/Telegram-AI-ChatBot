# Helper/interaction_handler/info_handler.py

from helper.telegram_api import send_message
from helper.memory import add_temp_memory, clear_temp_memory
# from helper.memory import get_temp_memory, summarize_memory, add_perm_memory

info_mode = {}


def set_info_mode(sender_id: int, mode: bool):
    """Sets the user info mode for the given sender_id."""
    info_mode[sender_id] = mode


def is_info_mode(sender_id: int) -> bool:
    """Checks if the user info mode is active for the given sender_id."""
    return info_mode.get(sender_id, False)


def handle_info_command(sender_id: int, words: list, messages: dict):
    """Handles the /info command for collecting user information."""
    if len(words) < 2:
        send_message(sender_id, "Please provide information after /info.")
        return

    # Join the user input after the command into a single string
    user_info = ' '.join(words[1:])

    # Save the new user info into temporary memory (replace old info)
    clear_temp_memory(sender_id)  # Clear old info if exists
    add_temp_memory(sender_id, user_info)

    # Send confirmation messages
    send_message(
        sender_id, "Your info has been recorded.")
    send_message(sender_id, "Here is a brief of your info:")

    # Create a summary from the user info
    summarized_info = summarize_user_info(user_info)
    send_message(sender_id, summarized_info)

    send_message(
        sender_id, "If you want to change the info, use /info.")


def summarize_user_info(user_info: str) -> str:
    """Summarizes user info into a formatted string."""
    # For simplicity, we can split the user info into key points
    # In a real scenario, you might want to extract more meaningful key points
    points = user_info.split(',')

    # Create a formatted summary
    summary_lines = ["*User's Info*"]
    for i, point in enumerate(points, 1):
        summary_lines.append(f"{i}- {point.strip()}")

    return "\n".join(summary_lines)


def handle_user_message(sender_id: int, message: str, messages: dict):
    """Handles user messages and stores user info if in info mode."""
    if is_info_mode(sender_id):
        # Store the user's message as temporary info
        handle_info_command(sender_id, message.split(), messages)
        set_info_mode(sender_id, False)  # Exit info mode
    else:
        send_message(
            sender_id, "Command not recognized.")
