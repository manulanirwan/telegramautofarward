import os, asyncio, threading
import gradio as gr
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURATION FROM SECRETS ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "").strip()

# --- YOUR CHANNELS ---
SOURCE_CHAT = "manulanirwan1" 
DEST_CHAT = "MrManulaCrypto"

async def run_bot():
    if not STRING_SESSION:
        print("❌ Error: STRING_SESSION is empty.")
        return
        
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    
    @client.on(events.NewMessage(chats=SOURCE_CHAT))
    async def handler(event):
        try:
            # Check if the message has any text
            if event.message.text:
                # We send ONLY the text and formatting (bold/links)
                # We removed the 'file' part to bypass the protected chat error
                await client.send_message(
                    DEST_CHAT, 
                    event.message.text, 
                    formatting_entities=event.message.entities
                )
                print(f"✅ Text copied successfully to {DEST_CHAT}")
            else:
                print("ℹ️ Ignored: Message contained media but no text.")
                
        except Exception as e:
            print(f"⚠️ Error during copy: {e}")

    print("Connecting...")
    await client.start()
    print("🚀 Bot is active! Monitoring for TEXT messages...")
    await client.run_until_disconnected()

# UI for Hugging Face
def status(): return "Telegram Bot is running (Text Only Mode)"
demo = gr.Interface(fn=status, inputs=[], outputs="text")

if __name__ == "__main__":
    def start_telethon():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
    
    threading.Thread(target=start_telethon, daemon=True).start()
    demo.launch(server_name="0.0.0.0", server_port=7860)