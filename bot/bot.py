import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "☕ Добро пожаловать в Coffee Feedback Bot!\n\n"
        "Новые отзывы будут приходить автоматически.\n"
        "Команды:\n"
        "/stats - статистика\n"
        "/list - последние 5 отзывов"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BACKEND_URL}/api/stats")
        data = resp.json()
    await update.message.reply_text(
        f"📊 Статистика:\n"
        f"Всего отзывов: {data['total']}\n"
        f"Средний рейтинг: {data['avg_rating']}\n"
        f"Сегодня: {data['today']}"
    )


async def list_feedbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BACKEND_URL}/api/feedback")
        feedbacks = resp.json()[:5]

    if not feedbacks:
        await update.message.reply_text("📭 Отзывов пока нет.")
        return

    text = "📋 Последние 5 отзывов:\n\n"
    for fb in feedbacks:
        text += f"👤 {fb['author']} | ⭐ {fb['rating']}/5 | {fb['category']}\n"
        text += f"💬 {fb['message'][:100]}...\n\n"

    await update.message.reply_text(text)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("list", list_feedbacks))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
