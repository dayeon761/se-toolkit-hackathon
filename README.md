# ☕ Coffee Shop Feedback Board

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

### Version 1 — Core Features
- Anonymous feedback form with rating (1-5) and categories
- PostgreSQL database storage
- Admin dashboard to view and manage feedback

### Version 2 — Advanced Features
- **Telegram bot with inline keyboard menu** — no need to type commands
- **Instant notifications** with interactive "Delete" button
- **Filter by category** — coffee, service, atmosphere, other
- **Filter by rating** — view all reviews with a specific score
- **Quick filters** — "Good reviews" (4-5⭐) and "Bad reviews" (1-2⭐)
- **Delete reviews directly from Telegram** — one tap, no need to open admin panel

### Not yet implemented
- QR codes for tables
- Reply to feedback
- Sentiment analysis

## Usage

**For visitors:** Open the web form, fill in rating, category, and message, then submit.

**For owners:**
- View all feedback at `/admin.html`
- Receive Telegram notifications instantly with delete button
- Use inline keyboard menu: Statistics, Last Reviews, Filters by category/rating

## Deployment

**Requirements:** Ubuntu 24.04, Docker, Docker Compose

**1. Telegram Bot Setup (Required):**
- **Get `BOT_TOKEN`:** Message [@BotFather](https://t.me/botfather) in Telegram, run `/newbot`. Copy the token.
- **Get `ADMIN_CHAT_ID`:** Message [@userinfobot](https://t.me/userinfobot), run `/start`. Copy your ID.

**2. Clone and Configure:**
```bash
git clone https://github.com/dayeon761/se-toolkit-hackathon.git
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
- **API Docs:** `http://localhost:8000/docs`

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 18 |
| Web Client | HTML + CSS + JavaScript |
| Telegram Bot | python-telegram-bot |
| Deployment | Docker + Docker Compose |
| Reverse Proxy | Caddy |

## Project Structure

```
coffee-feedback/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── database.py      # Database connection
│   │   └── routers/
│   │       ├── feedback.py  # Feedback CRUD + Telegram notifications
│   │       └── admin.py     # Stats + filtering endpoints
│   └── Dockerfile
├── bot/
│   ├── bot.py               # Telegram bot with inline keyboards
│   └── Dockerfile
├── web/
│   ├── index.html           # Feedback form
│   ├── admin.html           # Admin dashboard
│   └── style.css, script.js, admin.js
├── docker-compose.yml
├── Caddyfile
└── README.md
```

## API Endpoints

### Public:
| Method | Path | Description |
|---|---|---|
| POST | `/api/feedback` | Create new feedback |

### Admin:
| Method | Path | Description |
|---|---|---|
| GET | `/api/feedback` | Get all feedbacks |
| GET | `/api/feedback/category/{cat}` | Filter by category |
| GET | `/api/feedback/rating/{n}` | Filter by rating |
| DELETE | `/api/feedback/{id}` | Delete feedback |
| PUT | `/api/feedback/{id}/read` | Mark as read |
| GET | `/api/stats` | Get statistics |

## License

MIT
