import re
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== SOZLAMALAR ==================
import os

TOKEN = os.getenv("BOT_TOKEN")

PHISHING_WORDS = [
    "login",
    "verify",
    "verification",
    "free",
    "gift",
    "bonus",
    "airdrop",
    "telegram",
    "account",
    "confirm",
    "security",
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ================== /start ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 TG-Guard Bot\n\n"
        "🔗 Link yuboring — men uni phishing yoki xavfli ekanini tekshiraman.\n"
        "📎 Shubhali fayllardan ogohlantiraman.\n\n"
        "Akkauntingizni ehtiyot qiling!"
    )

# ================== LINK TEKSHIRISH ==================
async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    score = 0

    if "http://" in text or "https://" in text:
        if "http://" in text:
            score += 1

        if re.search(r"\d+\.\d+\.\d+\.\d+", text):
            score += 2

        for word in PHISHING_WORDS:
            if word in text:
                score += 1

        if score >= 3:
            await update.message.reply_text("❌ XAVFLI LINK (PHISHING)")
            try:
                await update.message.delete()
            except:
                pass

        elif score == 2:
            await update.message.reply_text("⚠️ SHUBHALI LINK")

        else:
            await update.message.reply_text("✅ LINK XAVFSIZ")

# ================== FAYL OGОHLANTIRISH ==================
async def check_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚠️ DIQQAT!\n\n"
        "Noma’lum fayllar akkauntni buzishga olib kelishi mumkin.\n"
        "Agar ishonchingiz bo‘lmasa — OCHMANG!"
    )

# ================== BOTNI ISHGA TUSHURISH ==================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_link))
    app.add_handler(MessageHandler(filters.Document.ALL, check_file))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
