# helper/memory.py

import time

# Global memory buffer to store user messages with timestamps
memory_buffer = {}
MESSAGE_EXPIRATION = 3600  # 1 hour expiration time


def add_to_memory(user_id: int, message: str) -> None:
    """Adds a message to the user's memory buffer with a timestamp."""
    if user_id not in memory_buffer:
        memory_buffer[user_id] = []
    memory_buffer[user_id].append((message, time.time()))


def clear_memory(user_id: int) -> None:
    """Clears the user's memory buffer."""
    memory_buffer.pop(user_id, None)


def get_memory(user_id: int) -> str:
    """Retrieves the user's memory as a concatenated string."""
    cleanup_memory(user_id)
    return "\n".join([msg[0] for msg in memory_buffer.get(user_id, [])])


def cleanup_memory(user_id: int) -> None:
    """Removes messages older than MESSAGE_EXPIRATION seconds."""
    if user_id in memory_buffer:
        current_time = time.time()
        memory_buffer[user_id] = [
            (msg, timestamp) for msg, timestamp in memory_buffer[user_id]
            if current_time - timestamp < MESSAGE_EXPIRATION
        ]
        if not memory_buffer[user_id]:
            clear_memory(user_id)
