from fastapi import FastAPI
from app.routers import files, questions, ping

app = FastAPI()

app.include_router(files.router)
app.include_router(questions.router)
app.include_router(ping.router)