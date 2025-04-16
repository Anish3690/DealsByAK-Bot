import logging
import re
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# === CONFIGURATION === #
BOT_TOKEN = "7900527205:AAEXzN8Kg9y8TkTxIZZP1kgi5HhZYYgfGAs"
SOURCE_CHANNELS = ["@gosfdeals", "@techscannerr", "@PremiumDeals"]
TARGET_CHANNEL = "@Ak3690"
AFFILIATE_TAG = "dealsbyak04-21"

# === LOGGING SETUP === #
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# === AFFILIATE LINK CONVERTER === #
def convert_amazon_links(text):
    # Detect and convert Amazon links to affiliate links
    pattern = r"(https?://(?:www\.)?amazon\.in(?:/[^\s]*)?)"
    def replace_link(match):
        url = match.group(1)
        if "tag=" in url:
            return re.sub(r"tag=[^&\s]+", f"tag={AFFILIATE_TAG}", url)
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AFFILIATE_TAG}"
    return re.sub(pattern, replace_link, text)

# === MESSAGE HANDLER === #
def handle_message(update: Update, context: CallbackContext):
    message = update.effective_message
    source = update.effective_chat.username

    if f"@{source}" not in SOURCE_CHANNELS:
        return

    text = message.text or message.caption or ""
    updated_text = convert_amazon_links(text)

    if message.text:
        context.bot.send_message(chat_id=TARGET_CHANNEL, text=updated_text)
    elif message.caption and message.photo:
        context.bot.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo[-1].file_id, caption=updated_text)

# === MAIN FUNCTION === #
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.chat(username=SOURCE_CHANNELS) & Filters.all, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
