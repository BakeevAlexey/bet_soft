import decimal

from typing import Optional

from pydantic import BaseModel

from .constant import EventState


class Event(BaseModel):
    event_id: str
    coefficient: str
    deadline: Optional[int]
    state: Optional[EventState]


class Bet(BaseModel):
    bet_id: str
    event_id: str
    amount: decimal.Decimal
