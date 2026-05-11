import os, asyncio, threading
import gradio as gr
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "").strip()

# Change these to your actual channel usernames or IDs
SOURCE_CHAT = "@source_channel_name" 
DEST_CHAT = "@your_channel_name"

async def run_bot():
    if not STRING_SESSION:
        print("❌ Error: STRING_SESSION is empty.")
        return
        
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    
    @client.on(events.NewMessage(chats=SOURCE_CHAT))
    async def handler(event):
        try:
            # We use send_message instead of forward_messages 
            # to bypass 'protected content' restrictions.
            await client.send_message(
                DEST_CHAT, 
                event.message.message,      # Copies the text
                file=event.message.media,    # Downloads & re-uploads photos/videos
                formatting_entities=event.message.entities # Keeps bold/italic/links
            )
            print("✅ Message successfully copied and re-posted.")
        except Exception as e:
            print(f"⚠️ Error during copy: {e}")

    print("Connecting...")
    await client.start()
    print("🚀 Bot is active! Monitoring for messages...")
    await client.run_until_disconnected()

# Simple UI to keep Hugging Face awake
def status(): return "Telegram Bot is running in the background."
demo = gr.Interface(fn=status, inputs=[], outputs="text")

if __name__ == "__main__":
    def start_telethon():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
    
    threading.Thread(target=start_telethon, daemon=True).start()
    demo.launch(server_name="0.0.0.0", server_port=7860)