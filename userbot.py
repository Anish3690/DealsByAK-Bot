from pyrogram import Client, filters
import re
import os
import requests
import json

# Your Details (Already Filled)
API_ID = 27420567
API_HASH = "9c52853ecccd13f5dbbf36db5acd2b31"
SESSION_NAME = "DealsByAKSession"

SOURCE_CHANNELS = ["gosfdeals", "techscannerr", "PremiumDeals"]  # Channels you copy deals from
TARGET_CHANNEL = "Ak3690"  # Your channel
AMAZON_TAG = "dealsbyak04-21"  # Amazon Affiliate Tag
EARNKARO_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODA2NDM0ODBiZTM0ZDU1NzUxNmQyMTQiLCJlYXJua2FybyI6IjI5MDQ4NjMiLCJpYXQiOjE3NDU4MjY4NzB9.HiVyhirpXoM-5KjEfsseC5xNIudIT4cIy1b-rMeKJsE"

# Start the app
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

# Amazon Affiliate Link Converter
def convert_amazon_links(text):
    pattern = r"(https?://(?:www\.)?amazon\.in[^\s]*)"
    def replace(match):
        url = match.group(1)
        if "tag=" in url:
            return re.sub(r"tag=[^&\s]+", f"tag={AMAZON_TAG}", url)
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AMAZON_TAG}"
    return re.sub(pattern, replace, text)

# EarnKaro Link Converter (Ajio, Flipkart, Myntra, etc.)
def convert_with_earnkaro(text):
    try:
        url = "https://ekaro-api.affiliaters.in/api/converter/public"
        headers = {
            "Authorization": f"Bearer {EARNKARO_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "deal": text,
            "convert_option": "convert_only"
        })
        res = requests.post(url, headers=headers, data=payload)
        data = res.json()
        if data.get("success") == 1:
            return data["data"]
        else:
            print(f"EarnKaro Conversion Failed: {data.get('message')}")
            return text
    except Exception as e:
        print(f"EarnKaro Error: {e}")
        return text

# When New Message Comes
@app.on_message(filters.channel & filters.chat(SOURCE_CHANNELS))
async def handle_message(client, message):
    try:
        text = message.text or message.caption or ""
        # Step 1: Convert Amazon links
        text = convert_amazon_links(text)
        # Step 2: Convert Ajio/Flipkart/Myntra links
        text = convert_with_earnkaro(text)

        if message.photo:
            await client.send_photo(
                chat_id=TARGET_CHANNEL,
                photo=message.photo.file_id,
                caption=text,
                disable_web_page_preview=True
            )
        else:
            await client.send_message(
                chat_id=TARGET_CHANNEL,
                text=text,
                disable_web_page_preview=True
            )

        print(f"✅ Posted to @{TARGET_CHANNEL}: {text[:60]}...")

    except Exception as e:
        print(f"❌ Error: {e}")

print("✅ Userbot is running. Listening for deals...")
app.run()
