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

# Function to clean text: removes links and @mentions
def clean_message_text(text):
    if not text:
        return ""
    
    # 1. Remove URLs (http, https, www)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # 2. Remove Telegram Mentions (e.g., @Trader09s)
    text = re.sub(r'@\w+', '', text)
    
    # 3. Clean up extra spaces left behind
    text = re.sub(r' +', ' ', text)
    
    return text.strip()

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
                # Process the text
                final_text = clean_message_text(raw_text)
                
                # Only send if there is still text left after cleaning
                if final_text:
                    await client.send_message(DEST_CHAT, final_text)
                    print(f"✅ Cleaned text sent to {DEST_CHAT}")
                else:
                    print("ℹ️ Message ignored: Empty after removing links/mentions.")
            else:
                print("ℹ️ Message ignored: No text content.")
                
        except Exception as e:
            print(f"⚠️ Error: {e}")

    print("Connecting...")
    await client.start()
    print("🚀 Bot active! Monitoring: Text only. (No Links, No @Mentions)")
    await client.run_until_disconnected()

# UI for Hugging Face
def status(): return "Bot Running: Cleaning Links & Mentions"
demo = gr.Interface(fn=status, inputs=[], outputs="text")

if __name__ == "__main__":
    def start_telethon():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
    
    threading.Thread(target=start_telethon, daemon=True).start()
    demo.launch(server_name="0.0.0.0", server_port=7860)