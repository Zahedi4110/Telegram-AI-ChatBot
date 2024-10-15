from helper.openai_api import text_completion, create_prompt
from helper.telegram_api import send_message
from helper.memory import add_temp_memory, get_perm_memory
from helper.memory import get_temp_memory, summarize_memory, clear_temp_memory
import logging

persona_prompt = (
    "Your name is *AI CHATBOT TELEGRAM (DEMO),"
    "a friendly and approachable assistant"
    "َAlways translate the answer into farsi!\n\n"
)


def handle_ask_command(
        sender_id: int,
        words: list,
        interaction_count: dict,
        messages: dict):

    if len(words) < 2:
        send_message(sender_id, messages["Len<2"])
        return

    current_query = ' '.join(words[1:])
    user_info = get_perm_memory(sender_id)
    user_history = get_temp_memory(sender_id)

    # افزودن ورودی کاربر به temp_memory
    add_temp_memory(sender_id, current_query)

    # ساخت پرامپت کامل برای OpenAI
    full_prompt = create_prompt(
        persona_prompt,
        user_info,
        user_history,
        current_query)

    # ارسال پرامپت به OpenAI
    response = text_completion(full_prompt)
    send_message(sender_id, response['response'])

    # بررسی تعداد تعاملات
    if interaction_count[sender_id] % 5 == 0:
        # اضافه کردن پرامپت برای خلاصه‌سازی
        summary_prompt = f"Summarize the following and store key points as memory: {user_history}"
        summary = text_completion(summary_prompt)

        if summary:
            clear_temp_memory(sender_id)
            add_temp_memory(sender_id, summary)
            send_message(sender_id, "Memory Updated.")
            logging.info(f"Updated Memory:\n{summary}\n")
        else:
            send_message(sender_id, "Can't Summarize!!")
