import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine
from app import models
from app.routers import feedback, admin

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coffee Feedback API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feedback.router)
app.include_router(admin.router)

# Serve static files (web frontend)
WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
if os.path.isdir(WEB_DIR):
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/")
def read_root():
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"message": "Coffee Feedback API is running"}


@app.get("/admin")
def admin_page():
    admin_path = os.path.join(WEB_DIR, "admin.html")
    if os.path.isfile(admin_path):
        return FileResponse(admin_path)
    return {"message": "Admin page not found"}
