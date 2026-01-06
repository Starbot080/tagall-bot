import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8360005960:AAFrM_VHc3hpO6WeFa-9M_sC8ReOTqlWvys"

if not TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😈 TagAll Bot Ready!\nUse /tagall to disturb everyone 😂"
    )

async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users = set()

    async for msg in context.bot.get_chat_history(chat_id, limit=200):
        if msg.from_user and not msg.from_user.is_bot:
            users.add(msg.from_user)

    if not users:
        await update.message.reply_text("No users to tag.")
        return

    text = "🔔 Attention everyone:\n\n"
    for user in users:
        text += f"[{user.first_name}](tg://user?id={user.id}) "

    await update.message.reply_text(text, parse_mode="Markdown")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tagall))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
