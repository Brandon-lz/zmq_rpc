import reflex as rx
import random
from typing import List, Dict


class DashboardPageState(rx.State):
    data = [
        {"time": 0, "uv": 4000, "pv": 2400, "amt": 2400},
        {"time": 1, "uv": 5000, "pv": 3000, "amt": 2400},
        {"time": 2, "uv": 6000, "pv": 4400, "amt": 2400},
        {"time": 3, "uv": 7000, "pv": 5400, "amt": 2400},
        {"time": 4, "uv": 8000, "pv": 6400, "amt": 2400},
        {"time": 5, "uv": 6000, "pv": 2400, "amt": 2400},
        {"time": 6, "uv": 5000, "pv": 1400, "amt": 2400},
    ]

    def add_data(self):
        self.data.append(
            {
                "time": len(self.data),
                "uv": random.randint(4000, 8000),
                "pv": random.randint(2400, 6400),
                "amt": random.randint(2400, 6400),
            }
        )


class BarChartState(rx.State):
    data: List[Dict[str, int]] = [
        {"month": "1月", "uv": 4000, "pv": 2400, "amt": 2400},
        {"month": "2月", "uv": 3000, "pv": 1398, "amt": 2210},
        {"month": "3月", "uv": 2000, "pv": 9800, "amt": 2290},
        {"month": "4月", "uv": 2780, "pv": 3908, "amt": 2000},
        {"month": "5月", "uv": 1890, "pv": 4800, "amt": 2181},
        {"month": "6月", "uv": 2390, "pv": 3800, "amt": 2500},
        {"month": "7月", "uv": 3490, "pv": 4300, "amt": 2100},
    ]


class PieChartState(rx.State):
    data: List[Dict[str, int]] = [
        {"name": "合格", "value": 400},
        {"name": "不合格", "value": 300},
        {"name": "Group C", "value": 300},
        {"name": "Group D", "value": 200},
        {"name": "Group E", "value": 278},
        {"name": "Group F", "value": 189},
    ]
