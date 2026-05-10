import os, asyncio, threading
import gradio as gr
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- FRIENDS CHANGE THESE ---
SOURCE = "@source_channel" # Channel to copy from
DEST = "@your_channel"     # Channel to send to

# --- SYSTEM CODE (Don't Change) ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "").strip()

async def start_forwarder():
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    @client.on(events.NewMessage(chats=SOURCE))
    async def handler(event):
        await client.send_message(DEST, event.message)
    await client.start()
    await client.run_until_disconnected()

# UI to keep it alive
def status(): return "Forwarder is ACTIVE 24/7"
if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(start_forwarder()), daemon=True).start()
    gr.Interface(fn=status, inputs=[], outputs="text").launch(server_name="0.0.0.0", server_port=7860)
