# Coffee Shop Feedback Board

*Anonymous feedback collection for coffee shops with web interface and Telegram bot*

## Demo

**Live product:** Runs locally at `http://localhost` after deployment.

### Feedback Form
![Feedback Form](form-screenshot.png)

### Admin Dashboard
![Admin Dashboard](admin-screenshot.png)

## Product Context

**End users:** Coffee shop visitors (leave feedback) and owners (receive notifications)

**Problem:** Visitors hesitate to give feedback in person; owners miss valuable insights

**Solution:** Anonymous web form + Telegram bot notifications + admin dashboard

## Features

### Implemented
- Anonymous feedback form with rating and categories
- PostgreSQL database storage
- Admin dashboard to view all feedback
- Telegram bot with instant notifications
- Statistics commands: /stats, /list

### Not yet implemented
- QR codes for tables
- Reply to feedback

## Usage

**For visitors:** Open the web form, fill in rating, category, and message, then submit.

**For owners:** 
- View all feedback at /admin.html
- Receive Telegram notifications instantly
- Use /stats and /list commands in Telegram

## Deployment

**Requirements:** Ubuntu 24.04, Docker, Docker Compose

**1. Telegram Bot Setup (Required):**
- **Get `BOT_TOKEN`:** Message [@BotFather](https://t.me/botfather) in Telegram, run `/newbot`. Copy the token.
- **Get `ADMIN_CHAT_ID`:** Message [@userinfobot](https://t.me/userinfobot), run `/start`. Copy your ID.

**2. Clone and Configure:**
```bash
git clone <your-repo-url>
cd se-toolkit-hackathon
cp .env.example .env
```
Edit `.env` and paste your `BOT_TOKEN` and `ADMIN_CHAT_ID`.

**3. Start:**
```bash
docker compose up -d
```

**4. Access:**
- **Web App:** `http://localhost`
- **Admin Panel:** `http://localhost/admin.html`
```

## License

MIT
