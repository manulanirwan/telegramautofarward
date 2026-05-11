import os, asyncio, threading, re
import gradio as gr
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "").strip()

# --- CHANNELS ---
SOURCE_CHAT = "targetmoonx" 
DEST_CHAT = "MrManulaCrypto"

# This is the "Cleaner" function that removes links
def remove_links(text):
    if not text:
        return ""
    # This pattern finds https://, http://, and www. links
    url_pattern = r'https?://\S+|www\.\S+'
    # Replace links with an empty space
    clean_text = re.sub(url_pattern, '', text)
    return clean_text.strip()

async def run_bot():
    if not STRING_SESSION:
        print("❌ Error: STRING_SESSION is empty.")
        return
        
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    
    @client.on(events.NewMessage(chats=SOURCE_CHAT))
    async def handler(event):
        try:
            raw_text = event.message.text
            if raw_text:
                # 1. Clean the text (remove links)
                final_text = remove_links(raw_text)
                
                # 2. Only send if there is still text left after cleaning
                if final_text:
                    await client.send_message(DEST_CHAT, final_text)
                    print(f"✅ Clean text sent to {DEST_CHAT}")
                else:
                    print("ℹ️ Message ignored: It only contained links.")
            else:
                print("ℹ️ Message ignored: No text found.")
                
        except Exception as e:
            print(f"⚠️ Error: {e}")

    print("Connecting...")
    await client.start()
    print("🚀 Bot active! Monitoring for text (Links will be removed).")
    await client.run_until_disconnected()

# UI for Hugging Face
def status(): return "Bot Running: Text Only & No Links"
demo = gr.Interface(fn=status, inputs=[], outputs="text")

if __name__ == "__main__":
    def start_telethon():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
    
    threading.Thread(target=start_telethon, daemon=True).start()
    demo.launch(server_name="0.0.0.0", server_port=7860)