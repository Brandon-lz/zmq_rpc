import reflex as rx
import sqlmodel
from datetime import datetime


class User(rx.Model, table=True):
    name: str = sqlmodel.Field(unique=False, nullable=False)
    worker_id: str = sqlmodel.Field(unique=True, nullable=False, description="工号")
    class_group: str = sqlmodel.Field(nullable=True, description="班组")
    password: str = sqlmodel.Field(nullable=False)
    face_path: str = sqlmodel.Field(nullable=True, description="人脸图片路径")
    is_superuser: bool = sqlmodel.Field(default=False)
    created_at: datetime = sqlmodel.Field(nullable=False,default_factory=datetime.now)
