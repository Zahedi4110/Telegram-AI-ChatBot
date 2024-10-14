# helper/interaction_handler.py

from helper.openai_api import text_completion, generate_image
from helper.telegram_api import send_message, send_photo
from helper.memory import (add_temp_memory, get_temp_memory,
                            clear_temp_memory, add_perm_memory,
                            get_perm_memory, summarize_memory)
import logging

# State management for user info mode
info_mode = {}

# Persona prompt for the AI
persona_prompt = (
    "Your name is *Soulsupport*,"
    "a friendly and approachable assistant"
    "specializing in psychology and mental health."
    "You possess expert-level knowledge in psychology."
    "Tailor your responses based on the user’s information,"
    "focusing exclusively on their mental health."
    "Respond in a helpful and lightly humorous manner"
    "to create a supportive atmosphere.\n"


)

def set_info_mode(sender_id: int, mode: bool):
    """Sets the user info mode for the given sender_id."""
    info_mode[sender_id] = mode

def is_info_mode(sender_id: int) -> bool:
    """Checks if the user info mode is active for the given sender_id."""
    return info_mode.get(sender_id, False)

def handle_info_command(sender_id: int, words: list, messages: dict):
    """Handles the /info command for collecting user information."""
    send_message(sender_id, "Please insert the information about yourself "
                           "for better understanding of the AI and better responses.")
    set_info_mode(sender_id, True)  # Enable info mode

def handle_user_message(sender_id: int, message: str, messages: dict):
    """Handles user messages and stores user info if in info mode."""
    if is_info_mode(sender_id):  # Check if the user is in info mode
        add_perm_memory(sender_id, message)  # Store the user's message as permanent info
        send_message(sender_id, "Thank you! Your information has been recorded.")
        set_info_mode(sender_id, False)  # Exit info mode
    else:
        add_temp_memory(sender_id, message)  # Store temporary messages
        send_message(sender_id, "Command not recognized. Please use /ask, /img, /info, or /clean.")

def handle_ask_command(sender_id: int, words: list, interaction_count: dict, messages: dict):
    """Handles the /ask command for user queries."""
    
    if len(words) < 2:  # No query provided after /ask
        send_message(sender_id, messages["ASK_PROMPT"])
        return

    current_query = ' '.join(words[1:])  # Join the user's query

    # Build the context for the prompt
    user_info = get_perm_memory(sender_id)
    user_history = get_temp_memory(sender_id)

    # Combine the persona prompt with the user's query
    full_prompt = (
        f"{persona_prompt}\n{user_info}\n{user_history}\n"
        f"User's question: {current_query}\n"
        "Please respond in a helpful and slightly humorous manner."
    )

    # Add the current query to temporary memory
    add_temp_memory(sender_id, current_query)

    # Get response from OpenAI API with the improved prompt
    response = text_completion(full_prompt, persona_prompt)
    send_message(sender_id, response['response'])  # Send the response

    # Summarize temporary memory every 5 interactions
    if interaction_count[sender_id] % 5 == 0:
        summary = summarize_memory(sender_id)  # Ensure this function is defined
        if summary:
            clear_temp_memory(sender_id)  # Clear the user's temporary memory
            add_temp_memory(sender_id, summary)  # Add summarized memory
            send_message(sender_id, "Memory updated with summary.")
            logging.info(f"Updated Memory:\n{summary}\n")
        else:
            send_message(sender_id, "Can't summarize memory!")

def handle_img_command(sender_id: int, words: list, messages: dict):
    """Handles the /img command for image generation."""
    if len(words) < 2:  # No query provided after /img
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

def handle_clean_command(sender_id: int, messages: dict):
    """Handles the /clean command to clear user memory."""
    previous_memory = get_temp_memory(sender_id)
    if previous_memory:
        send_message(sender_id, f"Summary of cleared memory:\n{previous_memory}")
        clear_temp_memory(sender_id)
        send_message(sender_id, messages["MEMORY_CLEARED"])
    else:
        send_message(sender_id, messages["NO_CONVERSATION"])
    send_message(sender_id, messages["CLEAN_START"])