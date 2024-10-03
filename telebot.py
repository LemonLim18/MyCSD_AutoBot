import os
import re
from dotenv import load_dotenv
from telethon import TelegramClient

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Create a new Telegram client
client = TelegramClient('autoCSD_Log', api_id, api_hash)

async def get_group_id(group_name):
    await client.start()
    async for dialog in client.iter_dialogs():
        if dialog.name == group_name:
            return dialog.id

# Function to extract Google Form URLs from the message text
def extract_google_form_urls(message_text):
    # Define the regex patterns for Google Form URLs
    patterns = [
        r'https?://docs\.google\.com/forms/d/e/\S+',  # Full URL format for Google Forms
        r'https?://forms\.gle/\S+'                    # Shortened URL format
    ]

    # Create a list to hold found URLs
    found_urls = []

    # Check each pattern against the message text
    for pattern in patterns:
        matches = re.findall(pattern, message_text)
        found_urls.extend(matches)

    return found_urls

async def monitor_group_messages(target_group_name):
    group_id = await get_group_id(target_group_name)

    if group_id:
        async for message in client.iter_messages(group_id):
            message_text = message.text or ""  # Ensure message_text is a string

            # Extract Google Form URLs
            gform_urls = extract_google_form_urls(message_text)

            if gform_urls:
                print("\n\nGoogle form detected!!!")
                for url in gform_urls:
                    print(f"Google Form URL: {url}")  # Print the extracted URL
            else:
                print("No Google Form URLs found in this message.")

    else:
        print(f"Group '{target_group_name}' not found")

# Run the client
with client:
    client.loop.run_until_complete(monitor_group_messages('AAA. Test MyCSD Bot Group'))
