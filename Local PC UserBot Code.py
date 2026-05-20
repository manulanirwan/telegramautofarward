from telethon import TelegramClient, events

# ===== CONFIG =====
api_id =             # From https://my.telegram.org
api_hash = ''      # From https://my.telegram.org
phone_number = ''  # Your Telegram account number

# You can add more channels in this list
source_channels = [
    '',   # e.g. '@CryptoSignals'
    '',    # e.g. '@AltcoinUpdates' 
    ]

destination_channel = ''  # e.g. '@MyCryptoHub'

# Create the Telegram client
client = TelegramClient('userbot_session', api_id, api_hash)

@client.on(events.NewMessage(chats=source_channels))
async def copy_text(event):
    try:
        # Copy text only (no media)
        if event.message.text:
            text = event.message.text
            await client.send_message(destination_channel, text)
            print(f"✅ Message copied from {event.chat.title}: {text[:50]}...")
        else:
            print(f"⚠️ Non-text message from {event.chat.title} — skipped.")
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    await client.start(phone_number)
    print("🚀 Userbot running — listening for messages...")
    print(f"📡 Source channels: {', '.join(source_channels)}")
    print(f"🎯 Destination channel: {destination_channel}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
