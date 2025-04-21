from pyrogram import Client, filters
import re, os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_NAME = "DealsByAKSession"

SOURCE_CHANNELS = ["gosfdeals", "techscannerr", "PremiumDeals"]
TARGET_CHANNEL = "Ak3690"
AFFILIATE_TAG = "dealsbyak04-21"

def convert_amazon_links(text):
    pattern = r"(https?://(?:www\.)?amazon\.in[^\s]*)"
    def replace_link(match):
        url = match.group(1)
        if "tag=" in url:
            return re.sub(r"tag=[^&\s]+", f"tag={AFFILIATE_TAG}", url)
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AFFILIATE_TAG}"
    return re.sub(pattern, replace_link, text)

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.channel & filters.chat(SOURCE_CHANNELS))
async def forward_and_convert(client, message):
    try:
        text = message.text or message.caption or ""
        converted_text = convert_amazon_links(text)

        if message.photo:
            await client.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo.file_id, caption=converted_text)
        else:
            await client.send_message(chat_id=TARGET_CHANNEL, text=converted_text)

        print(f"Forwarded from @{message.chat.username}: {converted_text[:50]}...")

    except Exception as e:
        print(f"Error: {e}")

print("Userbot is running... Monitoring source channels.")
app.run()
