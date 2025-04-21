import logging
import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# === CONFIGURATION === #
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNELS = ["@gosfdeals", "@techscannerr", "@PremiumDeals"]
TARGET_CHANNEL = "@Ak3690"
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "dealsbyak04-21")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")
WEBHOOK_SECRET_PATH = "/webhook"

# === LOGGING === #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === LINK CONVERTER === #
def convert_amazon_links(text):
    pattern = r"(https?://(?:www\.)?amazon\.in(?:/[^\s]*)?)"
    def replace_link(match):
        url = match.group(1)
        if "tag=" in url:
            return re.sub(r"tag=[^&\s]+", f"tag={AFFILIATE_TAG}", url)
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AFFILIATE_TAG}"
    return re.sub(pattern, replace_link, text)

# === MESSAGE HANDLER === #
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    source = update.effective_chat.username

    if f"@{source}" not in SOURCE_CHANNELS:
        return

    text = message.text or message.caption or ""
    updated_text = convert_amazon_links(text)

    if message.text:
        await context.bot.send_message(chat_id=TARGET_CHANNEL, text=updated_text)
    elif message.caption and message.photo:
        await context.bot.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo[-1].file_id, caption=updated_text)

# === ENTRY POINT === #
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    # Set webhook and run
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{WEBHOOK_DOMAIN}{WEBHOOK_SECRET_PATH}"
    )
