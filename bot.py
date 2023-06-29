import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import executor
import sqlite3
import os
from dotenv import load_dotenv
from .adminApp.QuestTrackerAdmin.models import User, Progress, Player

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
    registered_users = User.objects.all()

    # Send a message to all registered users
    for user in registered_users:
        await bot.send_message(user.username, "The event has started! Here are the details: ...")


# Command to complete an objective
@dp.message_handler(Command("complete_objective"))
async def complete_objective(message: types.Message, state: FSMContext):
    # Check if the user is registered for the event
    user = Player.objects.filter(username=message.from_user.username).first()
    if user is None:
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
    player_id = user.id  # Assuming the player's ID is stored in the first column of the 'users' table
    player_progress = track_progress(player_id, objective_id)
    feedback_message = f"Objective {objective_id} completed!\nYour progress: {player_progress}"
    await message.reply(feedback_message)


def track_progress(player_id, objective_id):
    # Retrieve player's progress from the database
    # use djnago model
    player_progress = Progress.objects.filter(player_id=player_id, objective_id=objective_id).first()
    return player_progress


# Command to display player's coin balance
@dp.message_handler(Command("coins"))
async def show_coin_balance(message: types.Message):
    # Check if the user is registered for the event
    # use django
    user = Player.objects.filter(username=message.from_user.username).first()
    if user is None:
        return await message.reply("You are not registered for the current event.")

    # Retrieve user's coin balance from the database
    player_id = user.id
    coin_balance = get_coin_balance(player_id)
    await message.reply(f"Your coin balance: {coin_balance}")


def get_coin_balance(player_id):
    # Retrieve player's coin balance from the database
    # use django
    player = Player.objects.filter(id=player_id).first()
    return player.coin_balance

# Command to complete an objective
@dp.message_handler(Command("complete_objective"))
async def complete_objective(message: types.Message, state: FSMContext):
    # use djnaog
    user = Player.objects.filter(username=message.from_user.username).first()
    if user is None:
        return await message.reply("You are not registered for the current event.")

    player_id = user.id


    # Process objective completion
    try:
        # Assuming the message format is '/complete_objective <objective_id>'
        command_parts = message.get_args().split()
        objective_id = int(command_parts[0])
    except (IndexError, ValueError):
        await message.reply("Invalid objective ID format. Please use the correct format.")
        return

    player_progress = track_progress(player_id, objective_id)
    feedback_message = f"Objective {objective_id} completed!\nYour progress: {player_progress}"
    await message.reply(feedback_message)


def track_progress(player_id, objective_id):
    # Retrieve player's progress from the database
    player = Player.objects.filter(id=player_id).first()
    progress = Progress.objects.filter(player=player, objective_id=objective_id).first()
    return progress.current_progress

# Other command handlers, error handlers, and additional functionality can be added as needed.


if __name__ == "__main__":
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
