# Helper/interaction_handler/ask_handler.py

from helper.openai_api import text_completion
from helper.telegram_api import send_message
from helper.memory import add_temp_memory, get_perm_memory
from helper.memory import get_temp_memory, summarize_memory, clear_temp_memory
import logging

persona_prompt = (
    "Your name is *Soulsupport*,"
    "a friendly and approachable assistant"
    "specializing in psychology and mental health."
    "You possess expert-level knowledge in psychology.\n\n"
    "Rules:\n1- Tailor your responses based on the user’s information\n"
    "2- Focusing exclusively on their mental health.\n"
    "3- Respond in a helpful and lightly humorous manner"
    "to Create a supportive atmosphere.\n"
    "4- If user asked something unrelated lead him back on the track\n"
    "5- Always answer in farsi\n"
    "6- Just answer the *User's New Question:*"
    "and use the data before that as the memory\n"
    "7- No need to title the answer\n"
    "8-Try to answer short and optimize with"
    "no additional details unless the question asks for it."


)


def handle_ask_command(
        sender_id: int, words: list, interaction_count: dict, messages: dict):
    if len(words) < 2:
        send_message(sender_id, messages["ASK_PROMPT"])
        return

    current_query = ' '.join(words[1:])
    user_info = get_perm_memory(sender_id)
    user_history = get_temp_memory(sender_id)

    full_prompt = f"{persona_prompt}\n{user_info}\n{user_history}\n*User's New Question:* {current_query}\n"

    add_temp_memory(sender_id, current_query)
    response = text_completion(full_prompt, persona_prompt)
    send_message(sender_id, response['response'])

    if interaction_count[sender_id] % 5 == 0:
        summary = summarize_memory(sender_id)
        if summary:
            clear_temp_memory(sender_id)
            add_temp_memory(sender_id, summary)
            send_message(sender_id, "Memory updated with summary.")
            logging.info(f"Updated Memory:\n{summary}\n")
        else:
            send_message(sender_id, "Can't summarize memory!")
