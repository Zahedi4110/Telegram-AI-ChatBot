# Helper/interaction_handler/img_handler.py

from helper.openai_api import generate_image
from helper.telegram_api import send_message, send_photo
from helper.memory import add_temp_memory, get_perm_memory, get_temp_memory


def handle_img_command(sender_id: int, words: list, messages: dict):
    if len(words) < 2:
        send_message(sender_id, messages["ASK_PROMPT"])
        return

    query = ' '.join(words[1:])
    add_temp_memory(sender_id, query)

    user_info = get_perm_memory(sender_id)
    user_history = get_temp_memory(sender_id)

    formatted_prompt = f"{user_info}\n{user_history}\nUser's Image Request: {query}"
    response = generate_image(formatted_prompt)

    if response['status'] == 1:
        send_photo(sender_id, response['url'], 'Generated Image!')
    else:
        send_message(sender_id, response['url'])

    send_message(sender_id, messages["DEFAULT_IMAGE_RESPONSE"])

