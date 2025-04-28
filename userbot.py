from pyrogram import Client, filters
import re
import requests

# ====== Your Config ======
API_ID = 27420567
API_HASH = "9c52853ecccd13f5dbbf36db5acd2b31"
SESSION_NAME = "DealsByAKSession"

SOURCE_CHANNELS = ["gosfdeals", "techscannerr", "PremiumDeals"]  # source channels
TARGET_CHANNEL = "Ak3690"  # your channel username without @
AFFILIATE_TAG = "dealsbyak04-21"  # Amazon affiliate tag
EARNKARO_USER_ID = "2904863"  # your EarnKaro User ID
# ===========================

# Function to convert Amazon links
def convert_amazon_links(text):
    pattern = r"(https?://(?:www\.)?amazon\.in[^\s]*)"
    def replace_link(match):
        url = match.group(1)
        if "tag=" in url:
            return re.sub(r"tag=[^&\s]+", f"tag={AFFILIATE_TAG}", url)
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AFFILIATE_TAG}"
    return re.sub(pattern, replace_link, text)

# Function to convert Ajio, Myntra, Flipkart links via EarnKaro
def convert_earnkaro_links(text):
    patterns = [
        r"(https?://(?:www\.)?ajio\.com[^\s]*)",
        r"(https?://(?:www\.)?myntra\.com[^\s]*)",
        r"(https?://(?:www\.)?flipkart\.com[^\s]*)"
    ]
    for pattern in patterns:
        for match in re.findall(pattern, text):
            ek_url = f"https://ekaro.in/enkr{EARNKARO_USER_ID}?deeplink={match}"
            text = text.replace(match, ek_url)
    return text

# Pyrogram Client
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.channel & filters.chat(SOURCE_CHANNELS))
async def copy_and_convert(client, message):
    try:
        text = message.text or message.caption or ""
        
        # First Amazon, then EarnKaro
        converted_text = convert_amazon_links(text)
        converted_text = convert_earnkaro_links(converted_text)

        if message.photo:
            await client.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo.file_id, caption=converted_text)
        elif message.document:
            await client.send_document(chat_id=TARGET_CHANNEL, document=message.document.file_id, caption=converted_text)
        else:
            await client.send_message(chat_id=TARGET_CHANNEL, text=converted_text)

        print(f"✅ Message copied successfully: {converted_text[:50]}...")

    except Exception as e:
        print(f"❌ Error: {e}")

print("🚀 Userbot is running... Monitoring source channels.")
app.run()
