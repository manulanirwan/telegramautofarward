import os
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- KEEP ALIVE SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- TELEGRAM BOT LOGIC ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
SOURCE_ID = targetmoonx  # Replace with source channel ID or username
DEST_ID = MrManulaCrypto    # Replace with your channel ID or username

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_ID))
async def handler(event):
    await client.send_message(DEST_ID, event.message)

if __name__ == "__main__":
    Thread(target=run_web).start() # Starts the web server
    print("Forwarder Started...")
    client.start()
    client.run_until_disconnected()
