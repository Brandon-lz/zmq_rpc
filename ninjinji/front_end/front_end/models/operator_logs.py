from typing import Sequence
import reflex as rx
from sqlalchemy import ScalarResult
import sqlmodel
from datetime import datetime
import pandas as pd
from .system import get_system_settings,Settings

class OperatorLogs(rx.Model, table=True):
    worker_name: str = sqlmodel.Field(unique=False,nullable=False,index=True)
    worker_id: str = sqlmodel.Field(unique=False,nullable=False,index=True,description="操作人员工号")
    class_group: str = sqlmodel.Field(nullable=True,description="班组")
    operation_time: datetime = sqlmodel.Field(default_factory=datetime.now,nullable=False,description="操作时间",index=True)
    operation_year: int = sqlmodel.Field(default_factory=lambda: datetime.now().year,description="操作年份")
    operation_month: int = sqlmodel.Field(default_factory=lambda: datetime.now().month,description="操作月份")
    operation_day: int = sqlmodel.Field(default_factory=lambda: datetime.now().day,description="操作日")
    operation_type: str = sqlmodel.Field(nullable=True,description="操作类型")
    operation_content: str = sqlmodel.Field(nullable=True,description="操作内容")
    operation_result: str = sqlmodel.Field(nullable=True,description="操作结果")
    
    def __repr__(self):
        return f"OperatorLogs(worker_name={self.worker_name}, worker_id={self.worker_id}, class_group={self.class_group}, operation_time={self.operation_time}, operation_type={self.operation_type}, operation_content={self.operation_content}, operation_result={self.operation_result})"

    class Config:
        table_name = "operator_logs"


def add_operator_log(worker_name: str, worker_id: str, class_group: str, operation_content: str, operation_type: str = "",  operation_result: str = ""):
    system = get_system_settings()
    if system is not None:
        settings = Settings(**system.settings)
        if not settings.open_log_record:
            return
    with rx.session() as sess:
        sess.expire_on_commit = False  # Make sure the user object is accessible. https://sqlalche.me/e/14/bhk3
        sess.add(OperatorLogs(worker_name=worker_name, worker_id=worker_id, class_group=class_group, operation_type=operation_type, operation_content=operation_content, operation_result=operation_result))
        sess.commit()

def get_operator_logs(year: int = None, month: int = None, day: int = None)->pd.DataFrame:
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    if day is None:
        day = datetime.now().day
    with rx.session() as sess:
        query: ScalarResult[OperatorLogs] = sess.exec(sqlmodel.select(OperatorLogs).where(OperatorLogs.operation_year == year, OperatorLogs.operation_month == month, OperatorLogs.operation_day == day).order_by(OperatorLogs.operation_time.desc()))
        logs: Sequence[OperatorLogs] = query.all()
        first = True
        if len(logs) == 0:
            return pd.DataFrame()
        for log in logs:
            if first:
                df = pd.DataFrame(log.dict(), index=[0])
                first = False
            else:
                df: pd.DataFrame = pd.concat([df, pd.DataFrame(log.dict(),index=[0])],ignore_index=True)
        df = df[["worker_name","worker_id","operation_time","operation_type","operation_content","operation_result"]]
        df.columns = ["操作人员","操作人员工号","操作时间","操作类型","操作内容","操作结果"]
        df.reset_index(drop=True, inplace=True)
        return df