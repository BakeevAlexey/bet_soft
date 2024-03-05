from fastapi import FastAPI

from app.routers import bet_router

app = FastAPI()

app.include_router(bet_router)
