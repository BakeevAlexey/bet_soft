import json
import uuid
import time

import redis.asyncio as redis

from fastapi import APIRouter

from ..models import Event
from ..constant import EventState
from ..utils import get_redis_connection


event_router = APIRouter()


@event_router.get("/add_full_data_redis")
async def add_full_data_redis():
    """Заргузка дефолтных данных для ставок."""
    redis_connect: redis.Redis = await get_redis_connection()

    events = [
        Event(event_id="", coefficient="1.2", deadline=int(time.time()) + 600, state=EventState.NEW.value),
        Event(event_id="", coefficient="1.15", deadline=int(time.time()) + 60, state=EventState.FINISHED_WIN.value),
        Event(event_id="", coefficient="1.67", deadline=int(time.time()) + 90, state=EventState.NEW.value),
        Event(event_id="", coefficient="1.67", deadline=int(time.time()) + 90, state=EventState.FINISHED_LOSE.value)
    ]

    save_events: list[str] = []

    for event in events:
        pk = str(uuid.uuid4())
        event.event_id = pk
        save_events.append(event.json())

    save_events_json = json.dumps(save_events)

    async with redis_connect.pipeline(transaction=True) as rc:
        # Сделано для полного обновления базы.
        await rc.flushdb()
        await rc.set("event", save_events_json).execute()

    return {"message": "Данные обновлены."}


@event_router.post("/create_event")
async def create_event(event: Event):
    redis_connect = await get_redis_connection()
    async with redis_connect as rc:
        events_json: str = await rc.get("event")
        events: list[Event | str] = json.loads(events_json)
        events.append(event.json())
        await rc.set("event", json.dumps(events))
    return event
