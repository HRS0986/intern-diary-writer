from pydantic import BaseModel


class DailyRecord(BaseModel):
    record: str