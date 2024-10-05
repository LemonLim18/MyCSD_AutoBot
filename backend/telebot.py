import os
import re
import json
import signal   # Import the signal module to handle signals
from dotenv import load_dotenv
from telethon import TelegramClient, events 
from autoForm import fill_google_form   # Import the function to fill Google Forms

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Variable to control the running state of the bot
should_run = True

# Create a new Telegram client
client = TelegramClient('autoCSD_Log', api_id, api_hash)

async def get_group_id(group_name):
    await client.start()  # Ensure the client is started
    async for dialog in client.iter_dialogs():
        if dialog.name == group_name:
            return dialog.id
    return None

# Function to extract Google Form URLs from the message text
def extract_google_form_urls(message_text):
    # Define the regex patterns for Google Form URLs
    patterns = [
        r'https?://docs\.google\.com/forms/d/e/\S+',  # Full URL format for Google Forms
        r'https?://forms\.gle/\S+'                    # Shortened URL format
    ]

    # Create a list to hold found URLs
    found_urls = []
    for pattern in patterns:
        matches = re.findall(pattern, message_text)
        found_urls.extend(matches)

    return found_urls


@client.on(events.NewMessage)
async def new_message_listener(event):
    # Get the message text
    message_text = event.message.message or ""  # Ensure message_text is a string
    target_group_name = 'AAA. Test MyCSD Bot Group'

    # Check if the message is from the target group
    if event.chat.title == target_group_name:
        # Extract Google Form URLs
        gform_urls = extract_google_form_urls(message_text)

        if gform_urls:
            print("\n\nGoogle form detected!!!")
            for url in gform_urls:
                print(f"Google Form URL: {url}")  # Print the extracted URL
                #TO-DO: Later will change the info.json to the data sent fro the Form.jsx
                with open("info.json", "r") as file:
                    json_data = json.load(file)
                fill_google_form(url, json_data)  # Fill the Google Form
                print("\Google Form filled successfully! Waiting for the next form...")
        else:
            print("No Google Form URLs found in this message.")

# Graceful shutdown handler
def stop_bot(_signal_received, _frame):
    global should_run
    print("Signal received to stop bot...")
    should_run = False
    client.disconnect()  # Gracefully disconnect the Telegram client

# Signal handling for exit
signal.signal(signal.SIGTERM, stop_bot)
signal.signal(signal.SIGINT, stop_bot)


async def main():
    target_group_name = 'AAA. Test MyCSD Bot Group'
    group_id = await get_group_id(target_group_name)

    if group_id:
        print(f"Monitoring messages in {target_group_name}...")
    else:
        print(f"Group '{target_group_name}' not found")
        return  # Exit if the group is not found

# Run the client
async def run_client():
    async with client:
        await main()  # Start monitoring messages
        await client.run_until_disconnected()  # Keep the client running until disconnected

if __name__ == '__main__':
    import asyncio
    asyncio.run(run_client())  # Start the client loop
