# Helper/interaction_handler/info_handler.py

from helper.telegram_api import send_message
from helper.memory import clear_temp_memory, add_perm_memory
from helper.openai_api import text_completion

info_mode = {}


def set_info_mode(sender_id: int, mode: bool):
    info_mode[sender_id] = mode


def is_info_mode(sender_id: int) -> bool:
    return info_mode.get(sender_id, False)


def handle_info_command(sender_id: int, words: list, messages: dict):
    if len(words) < 2:
        send_message(sender_id, "Please insert your info after /info")
        return

    user_info = ' '.join(words[1:])
    clear_temp_memory(sender_id)

    prompt = f"Summarize and store key points: {user_info}"

    summary_response = text_completion(prompt)
    add_perm_memory(sender_id, summary_response['response'])

    send_message(sender_id, "Info Recorded!")
    send_message(sender_id, "Summary Of Your Info:")
    send_message(sender_id, summary_response['response'])


def handle_user_message(sender_id: int, message: str, messages: dict):
    if is_info_mode(sender_id):
        handle_info_command(sender_id, message.split(), messages)
        set_info_mode(sender_id, False)
    else:
        send_message(sender_id, "Info not req")
