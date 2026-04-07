import os
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

CATEGORIES = {
    "coffee": "☕ Кофе",
    "service": "🤝 Обслуживание",
    "atmosphere": "🏠 Атмосфера",
    "other": "📝 Другое"
}

CATEGORY_EMOJI = {
    "coffee": "☕",
    "service": "🤝",
    "atmosphere": "🏠",
    "other": "📝"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📊 Статистика", callback_data="stats"),
            InlineKeyboardButton("📋 Последние", callback_data="list"),
        ],
        [
            InlineKeyboardButton("☕ По категориям", callback_data="filter_category"),
            InlineKeyboardButton("⭐ По оценкам", callback_data="filter_rating"),
        ],
        [
            InlineKeyboardButton("💩 Плохие (1-2⭐)", callback_data="filter_bad"),
            InlineKeyboardButton("🌟 Хорошие (4-5⭐)", callback_data="filter_good"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "☕ *Добро пожаловать в Coffee Feedback Bot!*\n\n"
        "Новые отзывы приходят автоматически.\n"
        "Выбери действие ниже:",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BACKEND_URL}/api/stats")
        data = resp.json()
    await update.message.reply_text(
        f"📊 *Статистика:*\n\n"
        f"Всего отзывов: `{data['total']}`\n"
        f"Средний рейтинг: `{data['avg_rating']}`/5\n"
        f"Сегодня: `{data['today']}`",
        parse_mode="Markdown",
    )


async def list_feedbacks(update: Update, context: ContextTypes.DEFAULT_TYPE, limit=5):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BACKEND_URL}/api/feedback")
        feedbacks = resp.json()[:limit]

    if not feedbacks:
        await update.message.reply_text("📭 Отзывов пока нет.")
        return

    text = f"📋 *Последние {limit} отзывов:*\n\n"
    for fb in feedbacks:
        cat_emoji = CATEGORY_EMOJI.get(fb["category"], "📝")
        stars = "⭐" * (fb["rating"] or 0)
        text += f"{cat_emoji} *{fb['author']}* | {stars} | {fb['category']}\n"
        text += f"💬 _{fb['message'][:100]}_\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "stats":
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/stats")
            data = resp.json()
        keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data="back_menu")]]
        await query.edit_message_text(
            f"📊 *Статистика:*\n\n"
            f"Всего отзывов: `{data['total']}`\n"
            f"Средний рейтинг: `{data['avg_rating']}`/5\n"
            f"Сегодня: `{data['today']}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif action == "list":
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/feedback")
            feedbacks = resp.json()[:5]

        if not feedbacks:
            keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data="back_menu")]]
            await query.edit_message_text("📭 Отзывов пока нет.", reply_markup=InlineKeyboardMarkup(keyboard))
            return

        text = "📋 *Последние 5 отзывов:*\n\n"
        for fb in feedbacks:
            cat_emoji = CATEGORY_EMOJI.get(fb["category"], "📝")
            stars = "⭐" * (fb["rating"] or 0)
            text += f"{cat_emoji} *{fb['author']}* | {stars}\n"
            text += f"💬 _{fb['message'][:100]}_\n\n"

        keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data="back_menu")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "filter_category":
        keyboard = [[InlineKeyboardButton(CATEGORIES[k], callback_data=f"cat_{k}")] for k in CATEGORIES]
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_menu")])
        await query.edit_message_text(
            "☕ *Выбери категорию:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif action.startswith("cat_"):
        category = action.replace("cat_", "")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/feedback/category/{category}")
            feedbacks = resp.json()[:5]

        if not feedbacks:
            await query.edit_message_text(f"📭 В категории «{CATEGORIES[category]}» отзывов нет.")
            return

        text = f"☕ *{CATEGORIES[category]}* — последние 5:\n\n"
        for fb in feedbacks:
            stars = "⭐" * (fb["rating"] or 0)
            text += f"*{fb['author']}* | {stars}\n"
            text += f"💬 _{fb['message'][:100]}_\n\n"

        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_menu")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "filter_rating":
        keyboard = [
            [InlineKeyboardButton(f"{'⭐' * i} {i}", callback_data=f"rating_{i}")]
            for i in range(5, 0, -1)
        ]
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_menu")])
        await query.edit_message_text(
            "⭐ *Фильтр по оценке:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif action.startswith("rating_"):
        rating = int(action.replace("rating_", ""))
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/feedback/rating/{rating}")
            feedbacks = resp.json()[:5]

        if not feedbacks:
            await query.edit_message_text(f"📭 Оценок «{rating}» пока нет.")
            return

        stars = "⭐" * rating
        text = f"{stars} *Оценка {rating}/5* — последние 5:\n\n"
        for fb in feedbacks:
            cat_emoji = CATEGORY_EMOJI.get(fb["category"], "📝")
            text += f"{cat_emoji} *{fb['author']}*\n"
            text += f"💬 _{fb['message'][:100]}_\n\n"

        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_menu")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "filter_bad":
        await _show_rating_filter(update, context, query, [1, 2], "💩")

    elif action == "filter_good":
        await _show_rating_filter(update, context, query, [4, 5], "🌟")

    elif action.startswith("delete_"):
        fb_id = int(action.replace("delete_", ""))
        async with httpx.AsyncClient() as client:
            resp = await client.delete(f"{BACKEND_URL}/api/feedback/{fb_id}")
        keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data="back_menu")]]
        if resp.status_code == 200:
            await query.edit_message_text("✅ Отзыв удален.", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text("❌ Ошибка при удалении.", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "back_menu":
        keyboard = [
            [
                InlineKeyboardButton("📊 Статистика", callback_data="stats"),
                InlineKeyboardButton("📋 Последние", callback_data="list"),
            ],
            [
                InlineKeyboardButton("☕ По категориям", callback_data="filter_category"),
                InlineKeyboardButton("⭐ По оценкам", callback_data="filter_rating"),
            ],
            [
                InlineKeyboardButton("💩 Плохие (1-2⭐)", callback_data="filter_bad"),
                InlineKeyboardButton("🌟 Хорошие (4-5⭐)", callback_data="filter_good"),
            ],
        ]
        await query.edit_message_text(
            "☕ *Меню:*\nВыбери действие:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def _show_rating_filter(update, context, query, ratings, emoji):
    all_feedbacks = []
    async with httpx.AsyncClient() as client:
        for r in ratings:
            resp = await client.get(f"{BACKEND_URL}/api/feedback/rating/{r}")
            all_feedbacks.extend(resp.json())
    all_feedbacks.sort(key=lambda x: x["created_at"], reverse=True)
    all_feedbacks = all_feedbacks[:5]

    if not all_feedbacks:
        keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data="back_menu")]]
        await query.edit_message_text(f"{emoji} Плохих/хороших отзывов пока нет.", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    text = f"{emoji} *Отзывы с оценкой {ratings}*: \n\n"
    for fb in all_feedbacks:
        cat_emoji = CATEGORY_EMOJI.get(fb["category"], "📝")
        stars = "⭐" * (fb["rating"] or 0)
        text += f"{cat_emoji} *{fb['author']}* | {stars}\n"
        text += f"💬 _{fb['message'][:100]}_\n\n"

    keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data="back_menu")]]
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


async def notify_telegram(message: str, rating: int, author: str, category: str, fb_id: int):
    """Отправка уведомления в Telegram с кнопкой удаления"""
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        return

    cat_emoji = CATEGORY_EMOJI.get(category, "📝")
    stars = "⭐" * rating if rating else ""

    text = f"☕ *Новый отзыв!*\n\n"
    text += f"{cat_emoji} *Автор:* {author}\n"
    if rating:
        text += f"⭐ *Оценка:* {rating}/5\n"
    text += f"💬 *Сообщение:* _{message}_"

    keyboard = [[InlineKeyboardButton("❌ Удалить", callback_data=f"delete_{fb_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json={
                "chat_id": ADMIN_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown",
                "reply_markup": reply_markup.to_dict(),
            })
        except Exception:
            pass


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("list", lambda u, c: list_feedbacks(u, c)))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
