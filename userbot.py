from pyrogram import Client, filters
import re, os, requests

# API Details
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_NAME = "DealsByAKSession"

# Channels
SOURCE_CHANNELS = ["gosfdeals", "techscannerr", "PremiumDeals"]  # without @
TARGET_CHANNEL = "Ak3690"  # without @

# Amazon Affiliate
AFFILIATE_TAG = "dealsbyak04-21"

# EarnKaro Details
EARNKARO_USER_ID = "2904863"  # <-- Your real User ID

# Initialize Pyrogram Client
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

# Amazon Affiliate Link Converter
def convert_amazon_links(text):
    pattern = r"(https?://(?:www\.)?amazon\.in[^\s]*)"
    def replace_link(match):
        url = match.group(1)
        if "tag=" in url:
            return re.sub(r"tag=[^&\s]+", f"tag={AFFILIATE_TAG}", url)
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AFFILIATE_TAG}"
    return re.sub(pattern, replace_link, text)

# EarnKaro Link Generator
def convert_earnkaro_links(text):
    pattern = r"(https?://(?:www\.)?(?:ajio|myntra|flipkart)\.com[^\s]*)"
    links = re.findall(pattern, text)
    for link in links:
        try:
            api_url = f"https://earnkaro.com/api/v2/deals/generate-affiliate-link?url={link}&user_id={EARNKARO_USER_ID}"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                affiliate_link = data.get("shortenedUrl") or data.get("affiliateUrl")
                if affiliate_link:
                    text = text.replace(link, affiliate_link)
        except Exception as e:
            print(f"EarnKaro conversion error: {e}")
    return text

# Main function to Forward and Convert Messages
@app.on_message(filters.channel & filters.chat(SOURCE_CHANNELS))
async def forward_and_convert(client, message):
    try:
        text = message.text or message.caption or ""
        
        # Step 1: Convert Amazon links
        text = convert_amazon_links(text)
        
        # Step 2: Convert EarnKaro links (Ajio, Myntra, Flipkart)
        text = convert_earnkaro_links(text)

        # Sending Photo or Text
        if message.photo:
            await client.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo.file_id, caption=text)
        else:
            await client.send_message(chat_id=TARGET_CHANNEL, text=text)

        print(f"Sent successfully: {text[:50]}...")

    except Exception as e:
        print(f"Error: {e}")

print("✅ Userbot is running... Monitoring channels.")
app.run()
