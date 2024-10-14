# Helper/interaction_handler/info_handler.py

from helper.telegram_api import send_message
from helper.memory import add_perm_memory

info_mode = {}


def set_info_mode(sender_id: int, mode: bool):
    info_mode[sender_id] = mode


def is_info_mode(sender_id: int) -> bool:
    return info_mode.get(sender_id, False)


def handle_info_command(sender_id: int, words: list, messages: dict):
    send_message(
        sender_id, "Please insert your info for better understanding")
    set_info_mode(sender_id, True)


def handle_user_message(sender_id: int, message: str, messages: dict):
    if is_info_mode(sender_id):
        add_perm_memory(sender_id, message)
        send_message(
            sender_id, "Thank you! Your information has been recorded.")
        set_info_mode(sender_id, False)
    else:
        send_message(
            sender_id, "Error!\nYour info did not recorded!")

