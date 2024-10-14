# helper/memory.py

import time

# Global memory buffers
temp_memory = {}  # Temporary memory for user interactions
perm_memory = {}  # Permanent memory for user information
MSG_EXPIRATION = 3600  # 1 hour expiration time for temporary memory


def add_temp_memory(user_id: int, message: str) -> None:
    """Adds a message to the user's temporary memory."""
    if user_id not in temp_memory:
        temp_memory[user_id] = []
    temp_memory[user_id].append((message, time.time()))


def clear_temp_memory(user_id: int) -> None:
    """Clears the user's temporary memory."""
    temp_memory.pop(user_id, None)


def get_temp_memory(user_id: int) -> str:
    """Retrieves the user's temporary memory as a concatenated string."""
    cleanup_temp_memory(user_id)
    return "\n".join([msg[0] for msg in temp_memory.get(user_id, [])])


def cleanup_temp_memory(user_id: int) -> None:
    """Removes messages older than MSG_EXPIRATION."""
    if user_id in temp_memory:
        current_time = time.time()
        temp_memory[user_id] = [
            (msg, timestamp) for msg, timestamp in temp_memory[user_id]
            if current_time - timestamp < MSG_EXPIRATION
        ]
        if not temp_memory[user_id]:
            clear_temp_memory(user_id)


def add_perm_memory(user_id: int, info: str) -> None:
    """Stores permanent user information."""
    perm_memory[user_id] = info


def get_perm_memory(user_id: int) -> str:
    """Retrieves the user's permanent memory."""
    return perm_memory.get(user_id, "")


def summarize_memory(user_id: int) -> str:
    """Summarizes the user's temporary memory."""
    if user_id in temp_memory:
        # Create a simple summary of the last 5 interactions
        recent_messages = [msg[0] for msg in temp_memory[user_id][-5:]]
        return "\n".join(recent_messages)
    return ""
