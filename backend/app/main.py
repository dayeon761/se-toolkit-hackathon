from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


@app.get("/")
def read_root():
    return {"message": "Coffee Feedback API is running"}
