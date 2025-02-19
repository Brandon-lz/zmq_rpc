# 工艺参数

import reflex as rx
import sqlmodel
from datetime import datetime
from pydantic import BaseModel


class ProcessSet(rx.Model, table=True):
    value: str = sqlmodel.Field(nullable=False, description="参数内容")
    created_at: datetime = sqlmodel.Field(nullable=False,default_factory=datetime.now)

    class Config:
        table_name = "process_set"


class ProcessSetValue(BaseModel):
    id:int
    values:list[float]