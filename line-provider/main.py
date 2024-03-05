from fastapi import FastAPI

from app.routers import bet_router, event_router

app = FastAPI()

app.include_router(event_router)
app.include_router(bet_router)
