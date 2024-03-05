import json
import uuid
import time
import decimal

import redis.asyncio as redis

from fastapi import APIRouter

from ..models import Event, Bet
from ..constant import EventState
from ..utils import get_redis_connection


bet_router = APIRouter()


@bet_router.get("/receive_all_key")
async def receive_all_events():
    """Получить все эвенты."""
    redis_connect = await get_redis_connection()

    async with redis_connect as rc:
        keys_event = await rc.get("event")
        events = json.loads(keys_event)
        events = [Event.parse_raw(item) for item in events]
    return events


@bet_router.post("/register_bet")
async def register_bet(event_id: str, amount_of_bet: str) -> list[Bet]:
    """Регистрация ставки пользователя."""

    bet_id = str(uuid.uuid4())
    bet_list = []
    amount = decimal.Decimal(amount_of_bet)

    bet = Bet(bet_id=bet_id, event_id=event_id, amount=amount)
    redis_connect = await get_redis_connection()
    async with redis_connect as rc:
        bet_list.append(bet.json())
        bet_json: str = json.dumps(bet_list)
        if not await rc.exists('bet'):
            await rc.set('bet', bet_json)
        bet_all: str = await rc.get("bet")
        bet_all: list = json.loads(bet_all)
        bet_all.append(bet.json())
        await rc.set('bet', json.dumps(bet_all))
        bet_get: str = await rc.get("bet")
    return [Bet.parse_raw(item) for item in json.loads(bet_get)]


@bet_router.get("/history_bet")
async def history_bet():
    redis_connect = await get_redis_connection()

    # decd43a9-71d7-4516-b5cb-f9b608eddbf2
    # 7ecf05e6-b6c0-4d4d-9b19-2839767c13b7

    events = []

    async with redis_connect as rc:
        bet_json: str = await rc.get("bet")
        bets: list[Bet] = json.loads(bet_json)
        for bet in bets:
            bet_item = Bet.parse_raw(bet)
            event_id = bet_item.event_id
            if not await rc.exists(event_id):
                continue
            event = await rc.get(str(event_id))
            events.append(event)

    return [Event.parse_raw(item) for item in events]










