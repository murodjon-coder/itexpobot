import os
from telegram.ext import Updater, CommandHandler

TOKEN = os.getenv("TOKEN")

def start(update, context):
    update.message.reply_text("Bot ishga tushdi!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

def start(update, context):
    update.message.reply_text(
        "Assalomu alaykum! 👋 Siz IT forumlari haqida eslatmalar oluvchi botga ulandingiz. "
        "Bo‘lishadigan eng yaqin tadbir: ICT WEEK 2025."
    )

def reminder(update, context):
    update.message.reply_text(
        "📢 Eslatma: ICT WEEK 2025 — 23–26-sentabr kunlari CAEx Uzbekistan markazida bo‘lib o‘tadi.\n"
        "Ro‘yxatdan o‘tish → https://ictweek.uz"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("eslatma", reminder))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
