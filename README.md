# ☕ Coffee Shop Feedback Board

*Anonymous feedback collection for coffee shops with web interface and Telegram bot*

## Demo

**Live product:** [Deploy on Render](#deployment) or run locally at `http://localhost`.

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
- **"Back to Main Menu" button** on every screen for easy navigation
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
- View all feedback at `/admin`
- Receive Telegram notifications instantly with delete button
- Use inline keyboard menu: Statistics, Last Reviews, Filters by category/rating

## Deployment

### Option A: Render.com (Recommended — Public URL)

**Free hosting with automatic HTTPS:**

1. Fork this repository on GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click **New → Blueprint Instance**
4. Select your forked repository
5. Render will read `render.yaml` and create all services automatically
6. Add environment variables:
   - `BOT_TOKEN` — from [@BotFather](https://t.me/botfather)
   - `ADMIN_CHAT_ID` — from [@userinfobot](https://t.me/userinfobot)
7. Click **Apply** and wait for deployment (~2 minutes)
8. Your app will be live at `https://coffee-feedback-xxxx.onrender.com`

### Option B: Local (Docker)

**Requirements:** Ubuntu 24.04, Docker, Docker Compose

**1. Telegram Bot Setup:**
- **Get `BOT_TOKEN`:** Message [@BotFather](https://t.me/botfather), run `/newbot`. Copy the token.
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
- **Admin Panel:** `http://localhost/admin`
- **API Docs:** `http://localhost:8000/docs`

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 18 |
| Web Client | HTML + CSS + JavaScript |
| Telegram Bot | python-telegram-bot |
| Deployment | Docker + Docker Compose / Render |

## Project Structure

```
coffee-feedback/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application + static files
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── database.py      # Database connection
│   │   └── routers/
│   │       ├── feedback.py  # Feedback CRUD + Telegram notifications
│   │       └── admin.py     # Stats + filtering endpoints
│   ├── Dockerfile
│   └── requirements.txt
├── bot/
│   ├── bot.py               # Telegram bot with inline keyboards
│   ├── Dockerfile
│   └── requirements.txt
├── web/
│   ├── index.html           # Feedback form
│   ├── admin.html           # Admin dashboard
│   └── style.css, script.js, admin.js
├── docker-compose.yml
├── render.yaml              # Render.com deployment config
├── Caddyfile
└── README.md
```

## API Endpoints

### Public:
| Method | Path | Description |
|---|---|---|
| GET | `/` | Web feedback form |
| GET | `/admin` | Admin dashboard |
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
