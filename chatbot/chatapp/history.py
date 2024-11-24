import sqlite3
from typing import List, Tuple

def get_last_two_messages(db_path: str) -> List[Tuple[str, str]]:
    """
    Connect to the SQLite database and retrieve the last two entries as pairs of user messages and bot responses.

    Args:
    - db_path: Path to the SQLite database file.

    Returns:
    - A list of tuples, each containing a user message and bot response.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Define your query for the last two entries based on a column like 'id'
        query = "SELECT user_message, bot_response FROM chatapp_chatmessage ORDER BY id DESC LIMIT 2"

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        rows = cursor.fetchall()

        # Create a list of (user_message, bot_response) tuples
        message_pairs = [(row[0], row[1]) for row in rows]

    finally:
        # Ensure the connection is closed even if an error occurs
        conn.close()

    return message_pairs

# Example usage:
# db_path = r'C:\Users\Mukesh\Desktop\numhack_2024\chatbot\db.sqlite3'
# message_pairs = get_last_two_messages(db_path)
# for user_message, bot_response in message_pairs:
#     print(f"User Message: {user_message}, Bot Response: {bot_response}")