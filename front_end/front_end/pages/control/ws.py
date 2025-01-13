from websocket import WebSocket, create_connection
import json

config = {}

with open("config.json") as f:
    config = json.load(f)

def get_heart_beat_ws() -> WebSocket:
    return create_connection(f"ws://{config['opcua-middleware']}/heartbeat")


def get_jog_add_ws() -> WebSocket:
    return create_connection(f"ws://{config['opcua-middleware']}/jog_add")

def get_jog_sub_ws() -> WebSocket:
    return create_connection(f"ws://{config['opcua-middleware']}/jog_sub")


def send_ws_json(ws: WebSocket, data) -> int:
    return ws.send(json.dumps(data))
