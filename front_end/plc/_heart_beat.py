from threading import Thread
from .opcua_start import PLCREADY
from .opcua_start import period_client
import time


def heartbeat_function():
    while True:
        time.sleep(1)
        if not PLCREADY:
            continue
        run()


def run():
    while True:
        heart_beat = period_client["heart_beat"]
        alivesign: int = heart_beat.get_value()
        if alivesign > 6000:
            alivesign = 0
        print("Heart Beat", alivesign)

        time.sleep(0.2)

        heart_beat.set_word(alivesign + 1)

        time.sleep(0.2)

def start_heartbeat():
    Thread(target=heartbeat_function, args=(), daemon=True).start()
