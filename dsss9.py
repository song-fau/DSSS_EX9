from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,CallbackContext

async def start(update:Update,context:CallbackContext)->None:
    await update.message.reply_text("Hello!Welcome to the bot.")

async def process(update:Update,context:CallbackContext)->None:
    await update.message.reply_text(f"You said:{update.message.text}")

def main()->None:
    API_TOKEN ="API Token"
    application =Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler("start",start))
    application.add_handler(MessageHandler(filters.TEXT&~filters.COMMAND,process))
    application.run_polling()

if __name__ == "__main__":
    main()
