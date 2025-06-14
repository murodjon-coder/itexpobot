from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_itpark_events
import os
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import logging
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_itpark_events, "interval", hours=12)
scheduler.start()
# Logging sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# TOKEN
TOKEN = os.getenv("TOKEN")

# Forumlar ro'yxatini yuklash
def load_forums():
    try:
        with open("forumlar.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# Foydalanuvchilarni yuklash
def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# Foydalanuvchilarni saqlash
def save_users(users):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Foydalanuvchini qo‘shish
def add_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

# /start komanda
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    add_user(user_id)
    update.message.reply_text("Assalomu alaykum! IT forumlar haqida sizga habar berib turaman.\n\nYordam: /help")

# /help komanda
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("/start - Botni ishga tushurish\n/forumlar - Yaqin forumlar\n/eslatma_on - Har kuni eslatma\n/eslatma_off - Eslatmani to‘xtatish\n/help - Yordam")

# /forumlar komanda
def forumlar(update: Update, context: CallbackContext):
    forumlar = load_forums()
    if not forumlar:
        update.message.reply_text("Hozircha forumlar mavjud emas.")
    else:
        text = "\n\n".join([f"{f['sana']} — {f['nomi']}" for f in forumlar])
        update.message.reply_text("Yaqinlashayotgan forumlar:\n\n" + text)

# Eslatma yuborish
def send_reminders(context: CallbackContext):
    users = load_users()
    forumlar = load_forums()
    if forumlar:
        matn = "\n\n".join([f"{f['sana']} — {f['nomi']}" for f in forumlar])
        for user_id in users:
            context.bot.send_message(chat_id=user_id, text=f"📢 Bugungi IT forumlar:\n\n{matn}")

# Scheduler
scheduler = BackgroundScheduler()

# /eslatma_on komanda
def eslatma_on(update: Update, context: CallbackContext):
    job = scheduler.get_job("daily_reminder")
    if job is None:
        scheduler.add_job(send_reminders, "interval", hours=24, id="daily_reminder", args=[context])
        scheduler.start()
        update.message.reply_text("✅ Har kuni eslatma yoqildi.")
    else:
        update.message.reply_text("⏳ Eslatma allaqachon yoqilgan.")

# /eslatma_off komanda
def eslatma_off(update: Update, context: CallbackContext):
    job = scheduler.get_job("daily_reminder")
    if job:
        scheduler.remove_job("daily_reminder")
        update.message.reply_text("❌ Eslatma o‘chirildi.")
    else:
        update.message.reply_text("🚫 Hech qanday eslatma yo‘q.")

# Main funktsiya
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("forumlar", forumlar))
    dp.add_handler(CommandHandler("eslatma_on", eslatma_on))
    dp.add_handler(CommandHandler("eslatma_off", eslatma_off))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
