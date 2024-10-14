# helper/interaction_handler.py

from helper.openai_api import text_completion, generate_image
from helper.telegram_api import sendMessage, sendPhoto
from helper.memory import add_to_memory, get_memory
from helper.memory import clear_memory  # cleanup_memory
import logging
import asyncio


persona_prompt = {
        "You are SaadatAI,"
        "a friendly and approachable assistant fluent in Farsi. "
        "Your knowledge level is"
        "expert in product information of Poyandegane Rahe Saadat Company. "
        "Respond to the user in a helpful and slightly humorous manner.\n"
}


async def handle_api_call(prompt: str, persona_prompt: str):
    """Handles the API calls asynchronously."""
    response = await asyncio.to_thread(text_completion, prompt, persona_prompt)
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


async def handle_ask_command(
        sender_id: int, words: list, interaction_count: dict, messages: dict):
    """
    Handles the /ask command for user queries.

    Parameters:
        - sender_id: ID of the user sending the message (int)
        - words: List of words in the user's message (list)
        - interaction_count: Dictionary tracking user interactions (dict)
        - messages: Dictionary containing predefined messages (dict)
    """
    logging.info(f"Handling /ask command for user {sender_id} with words: {words}")

    if len(words) < 2:  # No query provided after /ask
        sendMessage(sender_id, messages["ASK_PROMPT"])
        return

    current_query = ' '.join(words[1:])  # Join the user's query
    logging.info(f"Current Query: {current_query}")

    # Add the current query to memory
    add_to_memory(sender_id, current_query)

    # Construct the prompt for OpenAI API
    persona_prompt = (
        "You are SaadatAI, a friendly and approachable assistant fluent in Farsi. "
        "Your knowledge level is expert in product information of Poyandegane Rahe Saadat Company. "
        "Respond to the user in a helpful and slightly humorous manner.\n"
    )
    full_prompt = f"User's question: {current_query}"

    try:
        # Get response from OpenAI API
        response = await asyncio.to_thread(
            text_completion, full_prompt, persona_prompt)

        # Log the response before sending
        logging.info(f"Response from OpenAI: {response['response']}")

        # Send the response to the user
        sendMessage(sender_id, response['response'])

    except Exception as e:
        logging.error(f"Error while handling /ask command: {e}")
        sendMessage(sender_id, messages["ERROR_PROCESSING"])


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