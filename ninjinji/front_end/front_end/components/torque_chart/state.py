import reflex as rx
from typing import List, Dict
import random
import time

class TorqueChartState(rx.State):
    data: List[Dict] = [
        {"timestamp": "2025-01-20 14:23:28", "目标扭矩": 4000, "实际扭矩": 2400, "amt": 2400},
        {"timestamp": "2025-01-20 14:23:29", "目标扭矩": 3000, "实际扭矩": 2000, "amt": 2000},
        {"timestamp": "2025-01-20 14:23:30", "目标扭矩": 2000, "实际扭矩": 1600, "amt": 1600},
        {"timestamp": "2025-01-20 14:23:31", "目标扭矩": 1000, "实际扭矩": 1200, "amt": 1200},
        {"timestamp": "2025-01-20 14:23:32", "目标扭矩": 500, "实际扭矩": 800, "amt": 800},
    ]

    @rx.event
    def change_data(self):
        self.data.append({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "目标扭矩": random.randint(1000, 5000), "实际扭矩": random.randint(1000, 5000), "amt": random.randint(1000, 5000)})

    @rx.event
    def clear_data(self):
        self.data = [
            {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "目标扭矩": 0, "实际扭矩": 0, "amt": 0},
        ]