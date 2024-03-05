import decimal
import json

from fastapi import APIRouter, HTTPException
from aiohttp import ClientError, ClientSession


bet_router = APIRouter()


@bet_router.get("/events")
async def events():
    async with ClientSession() as session:
        try:
            async with session.get("http://line-provider:8000/receive_all_key") as response:
                response.raise_for_status()
                return await response.json()
        except ClientError as e:
            raise HTTPException(status_code=500, detail="Ошибка при выполнении запроса")


@bet_router.post("/bet")
async def bet(event_id: str, amount_of_bet: str):
    """Отправка ставки."""
    async with ClientSession() as session:
        try:
            url = "http://line-provider:8000/register_bet"
            data = {"event_id": event_id, "amount_of_bet": amount_of_bet}
            data_json = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            async with session.post(url, json=data_json, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except ClientError as e:
            raise HTTPException(status_code=500, detail="Ошибка при выполнении запроса")


@bet_router.get("/bets")
async def bets():
    """"""
    async with ClientSession() as session:
        try:
            async with session.get("http://line-provider:8000/history_bet") as response:
                response.raise_for_status()
                return await response.json()
        except ClientError as e:
            raise HTTPException(status_code=500, detail="Ошибка при выполнении запроса")


