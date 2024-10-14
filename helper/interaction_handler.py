# helper/interaction_handler.py

from helper.openai_api import text_completion, generate_image
from helper.telegram_api import sendMessage, sendPhoto
from helper.memory import add_to_memory, get_memory, clear_memory
import logging

# State management for user info mode
user_info_mode = {}  # Dictionary to track user states

# Persona prompt for the AI
persona_prompt = (
    "You are SaadatAI, a friendly and approachable assistant fluent in Farsi. "
    "Your knowledge level is expert in product information of Poyandegane Rahe "
    "Saadat Company. Respond to the user in a helpful and slightly humorous "
    "manner.\n"
)

def set_user_info_mode(sender_id: int, mode: bool):
    """Sets the user info mode for the given sender_id."""
    user_info_mode[sender_id] = mode

def is_user_info_mode(sender_id: int) -> bool:
    """Checks if the user info mode is active for the given sender_id."""
    return user_info_mode.get(sender_id, False)

def handle_info_command(sender_id: int, words: list, messages: dict):
    """Handles the /info command for collecting user information."""
    sendMessage(sender_id, "Please insert the information about yourself "
                           "for better understanding of the AI and better responses.")
    set_user_info_mode(sender_id, True)  # Enable info mode

def handle_user_message(sender_id: int, message: str, messages: dict):
    """Handles user messages and stores user info if in info mode."""
    if is_user_info_mode(sender_id):  # Check if the user is in info mode
        add_to_memory(sender_id, message)  # Store the user's message
        sendMessage(sender_id, "Thank you! Your information has been recorded.")
        set_user_info_mode(sender_id, False)  # Exit info mode
    else:
        handle_other_commands(sender_id, message, messages)

def handle_ask_command(sender_id: int, words: list, interaction_count: dict, messages: dict):
    """Handles the /ask command for user queries."""
    
    if len(words) < 2:  # No query provided after /ask
        sendMessage(sender_id, messages["ASK_PROMPT"])
        return

    current_query = ' '.join(words[1:])  # Join the user's query

    # Build the context for the prompt
    memory_prompt = (f"User Info:\n{get_memory(sender_id)}\n"
                     if get_memory(sender_id) else "No user information found.\n")

    # Combine the persona prompt with the user's query
    full_prompt = (
        f"{persona_prompt}{memory_prompt}"
        f"User's question: {current_query}\n"
        "Please respond in a helpful and slightly humorous manner."
    )

    # Add the current query to memory
    add_to_memory(sender_id, current_query)

    # Get response from OpenAI API with the improved prompt
    response = text_completion(full_prompt, persona_prompt)
    sendMessage(sender_id, response['response'])  # Send the response

    # Summarize memory every 5 interactions
    if interaction_count[sender_id] % 5 == 0:
        summary = summarize_memory(sender_id)
        if summary:
            clear_memory(sender_id)  # Clear the user's memory
            add_to_memory(sender_id, summary)  # Add summarized memory
            sendMessage(sender_id, "Memory updated with summary.")
            logging.info(f"Updated Memory:\n{summary}\n")
        else:
            sendMessage(sender_id, "Can't summarize memory!")

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