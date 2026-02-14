import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es ClowBot, un assistant intelligent, stratégique et un peu drôle."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "Erreur IA : " + str(e)

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("ClowBot intelligent lancé...")
app.run_polling()
