import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import executor
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("QUEST_TRACKER_BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create bot instance
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Create dispatcher
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Execute SQL queries
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, event_id INTEGER)")
cursor.execute("INSERT INTO users (username, event_id) VALUES ('JohnDoe', 1)")

# Retrieve data from the database
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the database connection
conn.close()



# Command to register for an event
@dp.message_handler(Command("register"))
async def register_event(message: types.Message):
    # Extract registration details from the message
    username = message.from_user.username
    event_id = ...  # Extract event ID from the message or use other means to identify the event

    # Store registration details in the database
    cursor.execute("INSERT INTO users (username, event_id) VALUES (?, ?)", (username, event_id))
    conn.commit()

    await message.reply(f"Registered for event {event_id}")


# Command to start an event
@dp.message_handler(Command("start_event"))
async def start_event(message: types.Message):
    # Get the list of registered users from the database
    cursor.execute("SELECT username FROM users")
    registered_users = [row[0] for row in cursor.fetchall()]

    # Send a message to all registered users
    for user in registered_users:
        await bot.send_message(user, "The event has started! Here are the details: ...")


# Command to complete an objective
@dp.message_handler(Command("complete_objective"))
async def complete_objective(message: types.Message, state: FSMContext):
    # Check if the user is registered for the event
    cursor.execute("SELECT * FROM users WHERE username=?", (message.from_user.username,))
    user_data = cursor.fetchone()
    if user_data is None:
        await message.reply("You are not registered for the current event.")
        return

    # Process objective completion
    try:
        # Assuming the message format is '/complete_objective <objective_id>'
        command_parts = message.get_args().split()
        objective_id = int(command_parts[0])
    except (IndexError, ValueError):
        await message.reply("Invalid objective ID format. Please use the correct format.")
        return

    # Update player's progress and provide feedback
    player_id = user_data[0]  # Assuming the player's ID is stored in the first column of the 'users' table
    player_progress = track_progress(player_id, objective_id)
    feedback_message = f"Objective {objective_id} completed!\nYour progress: {player_progress}"
    await message.reply(feedback_message)


def track_progress(player_id, objective_id):
    # Update player's progress in the database
    cursor.execute("INSERT INTO progress (player_id, objective_id) VALUES (?, ?)", (player_id, objective_id))
    conn.commit()

    # Retrieve updated player's progress from the database
    cursor.execute("SELECT COUNT(*) FROM progress WHERE player_id=?", (player_id,))
    player_progress = cursor.fetchone()[0]

    return player_progress


# Command to display player's coin balance
@dp.message_handler(Command("coins"))
async def show_coin_balance(message: types.Message):
    # Check if the user is registered for the event
    cursor.execute("SELECT * FROM users WHERE username=?", (message.from_user.username,))
    user_data = cursor.fetchone()
    if user_data is None:
        await message.reply("You are not registered for the current event.")
        return

    # Retrieve user's coin balance from the database
    player_id = user_data[0]  # Assuming the player's ID is stored in the first column of the 'users' table
    cursor.execute("SELECT coin_balance FROM players WHERE id=?", (player_id,))
    coin_balance = cursor.fetchone()[0]

    await message.reply(f"Your coin balance: {coin_balance}")


# Command to complete an objective
@dp.message_handler(Command("complete_objective"))
async def complete_objective(message: types.Message, state: FSMContext):
    # Check if the user is registered for the event
    cursor.execute("SELECT * FROM users WHERE username=?", (message.from_user.username,))
    user_data = cursor.fetchone()
    if user_data is None:
        await message.reply("You are not registered for the current event.")
        return

    # Process objective completion
    try:
        # Assuming the message format is '/complete_objective <objective_id>'
        command_parts = message.get_args().split()
        objective_id = int(command_parts[0])
    except (IndexError, ValueError):
        await message.reply("Invalid objective ID format. Please use the correct format.")
        return

    # Update player's progress and provide feedback
    player_id = user_data[0]  # Assuming the player's ID is stored in the first column of the 'users' table
    player_progress = track_progress(player_id, objective_id)
    feedback_message = f"Objective {objective_id} completed!\nYour progress: {player_progress}"
    await message.reply(feedback_message)


def track_progress(player_id, objective_id):
    # Update player's progress in the database
    cursor.execute("INSERT INTO progress (player_id, objective_id) VALUES (?, ?)", (player_id, objective_id))
    conn.commit()

    # Retrieve updated player's progress from the database
    cursor.execute("SELECT COUNT(*) FROM progress WHERE player_id=?", (player_id,))
    player_progress = cursor.fetchone()[0]

    return player_progress

# Other command handlers, error handlers, and additional functionality can be added as needed.


if __name__ == "__main__":
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
