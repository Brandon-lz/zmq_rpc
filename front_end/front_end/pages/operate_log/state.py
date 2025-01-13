import reflex as rx
import pandas as pd
from front_end.models import get_operator_logs
from datetime import datetime


class LogState(rx.State):

    filter_year: int = 0
    filter_month: int = 0
    filter_day: int = 0

    def select_data(self, date):
        print(date)
        print(type(date))

    @rx.cached_var
    def data(self) -> pd.DataFrame:
        if self.filter_day == 0:
            self.filter_day = datetime.now().day
        if self.filter_month == 0:
            self.filter_month = datetime.now().month
        if self.filter_year == 0:
            self.filter_year = datetime.now().year
        return get_operator_logs(
            int(self.filter_year), int(self.filter_month), int(self.filter_day)
        )
