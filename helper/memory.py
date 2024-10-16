import time
import logging
from helper.openai_api import text_completion

# Global memory buffers
temp_memory = {}
perm_memory = {}
MSG_EXPIRATION = 3600  # 1 hour expiration time for temporary memory

def add_temp_memory(user_id: int, message: str) -> None:
    if user_id not in temp_memory:
        temp_memory[user_id] = []
    temp_memory[user_id].append((message, time.time()))

def clear_temp_memory(user_id: int) -> None:
    temp_memory.pop(user_id, None)

def get_temp_memory(user_id: int) -> str:
    cleanup_temp_memory(user_id)
    return "\n".join([msg[0] for msg in temp_memory.get(user_id, [])])

def cleanup_temp_memory(user_id: int) -> None:
    if user_id in temp_memory:
        current_time = time.time()
        temp_memory[user_id] = [
            (msg, timestamp) for msg, timestamp in temp_memory[user_id]
            if current_time - timestamp < MSG_EXPIRATION
        ]
        if not temp_memory[user_id]:
            clear_temp_memory(user_id)

def add_perm_memory(user_id: int, info: str) -> None:
    perm_memory[user_id] = info

def get_perm_memory(user_id: int) -> str:
    return perm_memory.get(user_id, "")


def summarize_memory(user_id: int) -> str:
    """خلاصه‌سازی حافظه کاربر با استفاده از API OpenAI."""
    # دریافت محتوای حافظه موقتی کاربر
    memory_content = get_temp_memory(user_id)
    
    if memory_content:
        # ساخت پرامپت خلاصه‌سازی
        summary_prompt = (
            f"Summarize the conversation, highlighting key information. "
            f"Limit to 1-10 points for future reference, focusing on "
            f"essential details, user preferences, and specific requests "
            f"discussed.- No additional details\n{memory_content}"
        )
        
        # فراخوانی API OpenAI برای دریافت خلاصه
        summary_response = text_completion(summary_prompt)  # Ensure this call is correct
        
        # بررسی پاسخ API و جایگزینی حافظه موقتی
        if 'response' in summary_response:
            # جایگزینی حافظه موقتی با خلاصه
            clear_temp_memory(user_id)  # پاک کردن حافظه موقتی قبلی
            add_temp_memory(user_id, {'question': "Summary", 'response': summary_response['response']})  # اضافه کردن خلاصه به حافظه موقتی
            return "Memory Updating..."
    
    return "Can't Update Memory"


'''

def summarize_memory(user_id: int) -> str:
    if user_id in temp_memory:
        interactions = temp_memory[user_id]
        logging.info(f"Current interactions for user {user_id}: {interactions}")

        summary = []
        for index, interaction in enumerate(interactions):
            question = interaction['question']
            response = interaction['response']
            summary.append(f"{index + 1}- User's question: {question}\nAI's response: {response}")
        return "\n".join(summary)
    return ""
'''
