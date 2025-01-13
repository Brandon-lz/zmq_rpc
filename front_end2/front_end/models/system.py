import reflex as rx
import sqlmodel
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from sqlalchemy.orm.attributes import InstrumentedAttribute



class Settings(BaseModel):
    open_log_record:bool
    

class System(rx.Model, table=True):
    if TYPE_CHECKING:   # 实际不建议这样，有可能忘记改else里的字段
        version: InstrumentedAttribute = sqlmodel.Field(primary_key=True)
        settings: InstrumentedAttribute = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
        create_at: InstrumentedAttribute = sqlmodel.Field(default_factory=datetime.now,sa_column=sqlmodel.Column(sqlmodel.DateTime(timezone=True), index=True))
        # update_at: InstrumentedAttribute = sqlmodel.Field(default_factory=datetime.now,sa_column=sqlmodel.Column(sqlmodel.DateTime(timezone=True), onupdate=datetime.now,index=True))  
    else:
        version: int = sqlmodel.Field(primary_key=True)
        settings: dict = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
        create_at: datetime = sqlmodel.Field(default_factory=datetime.now,sa_column=sqlmodel.Column(sqlmodel.DateTime(timezone=True), index=True))
        # 保存时自动更新时间
        # update_at:datetime = sqlmodel.Field(default_factory=datetime.now,sa_column=sqlmodel.Column(sqlmodel.DateTime(timezone=True), onupdate=datetime.now,index=True))


def get_system_settings() -> System | None:
    with rx.session() as session:
        return session.exec(sqlmodel.select(System).order_by(System.version.desc()).limit(1)).first()


def update_system_settings(settings: Settings) -> System:
    with rx.session() as session:
        system = System(settings=settings.model_dump())
        session.add(system)
        session.commit()
        session.refresh(system)
        print(f"System version: {system.version} update at: {system.create_at} settings: {system.settings}")
        
        old_systems =  session.exec(sqlmodel.select(System).filter(System.create_at<(datetime.now()-timedelta(days=10.0)))).all()
        for old_system in old_systems:
            session.delete(old_system)
            session.commit()
            print(f"Deleted system version: {old_system.version} create at: {old_system.create_at}")
        return system
        