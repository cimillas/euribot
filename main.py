import logging, os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import euribor

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Calma Juan Carlos, que aún queda...")

async def getEuriborValues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    euribor12 = euribor.retrieveEuriborValue(euribor.URL_EURIBOR_12m)
    euribor6 = euribor.retrieveEuriborValue(euribor.URL_EURIBOR_6m)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"El úlimo valor del Euríbor (12 meses) es {euribor12}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"El úlimo valor del Euríbor (6 meses) es {euribor6}")

if __name__ == '__main__':
    load_dotenv()
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    start_handler = CommandHandler('start', start)
    values_handler = CommandHandler('euribor', getEuriborValues)
    application.add_handler(start_handler)
    application.add_handler(values_handler)
    
    application.run_polling()