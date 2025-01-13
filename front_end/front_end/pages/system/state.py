import reflex as rx
from front_end.models.system import Settings,update_system_settings,get_system_settings
from sqlmodel import select
from datetime import datetime, timedelta

class SystemState(rx.State):
    # init时候把这三行注释掉
    _system = get_system_settings()
    _settings = Settings(**_system.settings)
    open_log_record: bool = _settings.open_log_record
    # open_log_record: bool = False
    mes_url:str = "http://127.0.0.1:8000"
    
    
    def toggle_log_record(self,value:bool):
        print(f"Toggling log record to {value}")
        self.open_log_record = value
        system = update_system_settings(Settings(open_log_record=value))
        print(f"System settings updated: {system}")