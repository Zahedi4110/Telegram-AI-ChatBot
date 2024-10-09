# helper/interaction_handler.py

from helper.openai_api import text_completion, generate_image
from helper.telegram_api import sendMessage, sendPhoto
from helper.memory import add_to_memory, get_memory
from helper.memory import clear_memory  # cleanup_memory
import logging

import asyncio


async def handle_api_call(prompt: str):
    """Handles the API calls asynchronously."""
    response = await asyncio.to_thread(text_completion, prompt)
    return response


async def summarize_memory(user_id: int):
    """Summarizes the user's memory using OpenAI API."""
    memory_content = get_memory(user_id)
    if memory_content:
        summary_prompt = (
            f"Summarize the conversation, highlighting key information. "
            f"Limit to 1-10 points for future reference, focusing on "
            f"essential details, user preferences, and specific requests "
            f"discussed.- No additional details\n{memory_content}"
        )
        summary_response = await handle_api_call(summary_prompt)
        return summary_response['response']
    return ""


def handle_ask_command(
        sender_id: int, words: list, interaction_count: dict, messages: dict):
    """Handles the /ask command for text completion."""
    if len(words) < 2:  # No query provided after /ask
        sendMessage(sender_id, messages["ASK_PROMPT"])
        return

    # Get previous memory
    previous_memory = get_memory(sender_id)
    current_query = ' '.join(words[1:])
    # Log memory status
    logging.info(f"Memory Status: {get_memory(sender_id)}")

    # Add context to the memory and the current question
    if previous_memory:
        memory_prompt = f"previous interactions:\n{previous_memory}\n"
    else:
        memory_prompt = "No previous interactions found.\n"

    memory_prompt += f"new input of user: {current_query}"
    add_to_memory(sender_id, current_query)

    # Summarize memory every 5 interactions
    if interaction_count[sender_id] % 5 == 0:
        summary = asyncio.run(summarize_memory(sender_id))
        if summary:
            clear_memory(sender_id)  # Clear the user's memory
            add_to_memory(sender_id, summary)  # Add summarized memory
            sendMessage(sender_id, "Updating Memory...")
            logging.info(f"\n\n************************\nUpdated Memory:"
                         f"\n{summary}\n************************\n\n")

        else:
            sendMessage(sender_id, "Can't Summarize!")
            # Log AI response

    # Get response from OpenAI API
    response = asyncio.run(handle_api_call(memory_prompt))
    sendMessage(sender_id, response['response'])


def handle_img_command(sender_id: int, words: list, messages: dict):
    """Handles the /img command for image generation."""
    if len(words) < 2:  # No query provided after /img
        sendMessage(sender_id, messages["ASK_PROMPT"])
        return

    query = ' '.join(words[1:])
    add_to_memory(sender_id, query)

    formatted_prompt = get_memory(sender_id) + f"User's Image Request: {query}"
    response = generate_image(formatted_prompt)

    if response['status'] == 1:
        sendPhoto(sender_id, response['url'], 'Generated Image!')
    else:
        sendMessage(sender_id, response['url'])

    sendMessage(sender_id, messages["DEFAULT_IMAGE_RESPONSE"])


def handle_clean_command(sender_id: int, messages: dict):
    """Handles the /clean command to clear user memory."""
    previous_memory = get_memory(sender_id)
    if previous_memory:
        sendMessage(
            sender_id, f"Summary of cleared memory:\n{previous_memory}")
        clear_memory(sender_id)
        sendMessage(sender_id, messages["MEMORY_CLEARED"])
    else:
        sendMessage(sender_id, messages["NO_CONVERSATION"])
    sendMessage(sender_id, messages["CLEAN_START"])
