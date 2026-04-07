# ☕ Coffee Shop Feedback Board

*Anonymous feedback collection for coffee shops with web interface and Telegram bot*

## Demo

**Live product:** Runs locally on your machine. After deployment, open:

🌐 **[http://localhost](http://localhost)** — Feedback form  
📊 **[http://localhost/admin](http://localhost/admin)** — Admin dashboard

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

**Requirements:** Ubuntu 24.04 (or any OS with Docker), Docker, Docker Compose

**1. Install Docker** (if not installed):
```bash
# Ubuntu 24.04
sudo apt update && sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
# Log out and log back in
```

**2. Telegram Bot Setup:**
- **Get `BOT_TOKEN`:** Open [@BotFather](https://t.me/botfather) in Telegram, send `/newbot`, follow instructions, copy the token.
- **Get `ADMIN_CHAT_ID`:** Open [@userinfobot](https://t.me/userinfobot), send `/start`, copy your numeric ID.

**3. Clone and Configure:**
```bash
git clone https://github.com/dayeon761/se-toolkit-hackathon.git
cd se-toolkit-hackathon
cp .env.example .env
```
Edit `.env` and paste your `BOT_TOKEN` and `ADMIN_CHAT_ID`.

**4. Start:**
```bash
docker compose up -d
```

**5. Open in browser:**
- **Feedback form:** http://localhost
- **Admin panel:** http://localhost/admin
- **API docs:** http://localhost:8000/docs

**To stop:**
```bash
docker compose down
```

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
