from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
import logging
import re
import asyncio
import nest_asyncio
import psutil
import os
import sys

# Enable logging for debugging
logging.basicConfig(filename='bot.log', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Patch asyncio to allow nested use
nest_asyncio.apply()

# Function to check for existing bot instances
def check_for_existing_bot():
    current_process = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python.exe' and proc.info['pid'] != current_process:
            if 'telebot.py' in proc.info['cmdline']:
                print(f"Found running bot instance with PID: {proc.info['pid']}. Terminating it...")
                proc.terminate()  # Terminate the existing bot instance
                proc.wait()       # Wait for the process to terminate

# Create function to handle incoming messages from the group chat, not from the bot itself
async def handle_message(update: Update, context: CallbackContext) -> None:
    # Check if the message is from a group chat
    if update.message.chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        message_text = update.message.text      # Get the text of the message
        chat_id = update.message.chat        # Get the chat object

        # Log the message for debugging
        logger.info(f"Received message from group {chat_id}: {message_text}")

        # Example: Look for messages containing URLs
        url_match = re.search(r'(https?://[^\s]+)', message_text)

        if url_match:
            url = url_match.group(0)
            await context.bot.send_message(chat_id=chat_id, text=f"Found a URL: {url}")
            print(f"Found a URL: {url}")

# Error handler
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

# Main function to start the bot
async def main():
    bot_token = '7541098480:AAFRhypcZhRZBASXe30BRDjO3NXUJTvoc8o'

    # Create the Application
    application = ApplicationBuilder().token(bot_token).build()

    # Register the message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register the error handler
    application.add_error_handler(error)

    # Start the Bot
    print("Bot starting...")
    await application.run_polling()  # Use await here instead of application.start_polling()
    logger.info("Bot started successfully and is now polling for updates")

if __name__ == '__main__':
    check_for_existing_bot()  # Check and terminate any existing bot instances
    try: 
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Failed to start the bot: {e}")
