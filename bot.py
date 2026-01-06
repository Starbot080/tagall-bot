import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ========== DUMMY WEB SERVER ==========
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

# ========== TELEGRAM BOT ==========
TOKEN = os.getenv("8360005960:AAFrM_VHc3hpO6WeFa-9M_sC8ReOTqlWvys")
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

async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tagall))
    await app.run_polling()

# ========== MAIN ==========
if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    asyncio.run(run_bot())
