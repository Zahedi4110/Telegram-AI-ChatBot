from helper.openai_api import text_completion, create_prompt
from helper.telegram_api import send_message
from helper.memory import add_temp_memory, get_perm_memory
from helper.memory import get_temp_memory, summarize_memory, clear_temp_memory
import logging

persona_prompt = (
    "Your name is *AI CHATBOT (DEMO),"
    "a friendly and approachable assistant"
    "َAlways translate the answer into farsi!\n\n"
)


def handle_ask_command(
        sender_id: int, words: list, interaction_count: dict, messages: dict):
    if len(words) < 2:
        send_message(sender_id, messages["Len<2"])
        return

    current_query = ' '.join(words[1:])
    user_info = get_perm_memory(sender_id)
    user_history = get_temp_memory(sender_id)

    # ساخت پرامپت کامل برای OpenAI
    full_prompt = create_prompt(
        persona_prompt, user_info, user_history, current_query)

    # ارسال پرامپت به OpenAI
    response = text_completion(full_prompt)
    send_message(sender_id, response['response'])

    # ذخیره ورودی و پاسخ در temp_memory
    add_temp_memory(
        sender_id, {'question': current_query, 'response': response['response']})

    # افزایش شمارش تعاملات
    interaction_count[sender_id] += 1
    # بررسی تعداد تعاملات
    if interaction_count[sender_id] % 5 == 0:
        update_message = summarize_memory(sender_id)
        send_message(sender_id, update_message)
        send_message(sender_id, "حافظه با خلاصه به‌روزرسانی شد.")
        logging.info(f"Updated Memory:\n{update_message}\n")
