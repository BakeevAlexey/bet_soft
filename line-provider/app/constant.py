from enum import Enum


class EventState(Enum):
    NEW = "new"
    FINISHED_WIN = "finished_win"
    FINISHED_LOSE = "finished_lose"
