import os
from telegram.ext import Updater, CommandHandler

# TOKEN ni Railway variables ichidan oladi
TOKEN = os.getenv("TOKEN")

def start(update, context):
    update.message.reply_text("Assalomu alaykum! IT forumlar haqida sizga habar berib turaman.")

def help_command(update, context):
    update.message.reply_text("Yordam: /start buyrug'ini yuboring.")

def main():
    if not TOKEN:
        print("❌ TOKEN topilmadi. Iltimos, Railway Variables ichiga TOKEN qo'shing.")
        return

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    print("✅ Bot ishga tushdi.")
    updater.idle()

if __name__ == '__main__':
    main()
