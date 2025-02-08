from fastapi import FastAPI, WebSocket, Body
import asyncio
from pydantic import BaseModel
import math

# dev mode
import os
import random
from dataclasses import dataclass

dev_mode:str = os.getenv("dev_mode")

@dataclass
class TestValue:
    aim_torque:float = 0.7
    heartbeat:int = 0

    def get_torque_value(self)->float:
        return float(random.randint(0,60000))/10.0 

testvalue = TestValue()
app = FastAPI()


if not dev_mode:
    from opcua_start import period_client
    app = FastAPI(on_shutdown=[period_client.disconnect])


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/getvalue/{node_name}")
async def get_value(node_name: str):
    if dev_mode:
        result = None
        if node_name=="torque_value":
            result = testvalue.get_torque_value()
        elif node_name == "aim_torque":
            result = testvalue.aim_torque
        elif node_name == "heartbeat":
            result = testvalue.heartbeat
        return {"value": result}
    return {"value": period_client[node_name].get_value()}


@app.put("/torque-start")
async def torque_start():
    print("torque start")
    if dev_mode:
        return {"res": "success"}
    period_client["start"].set_bool(True)
    return {"res": "success"}


@app.put("/torque-stop")
async def torque_stop():
    print("torque stop")
    if dev_mode:
        return {"res": "success"}
    period_client["stop"].set_bool(True)
    return {"res": "success"}


class AimTorque(BaseModel):
    torque: float


@app.put("/set-torque")
async def set_torque(aim_torque: AimTorque = Body(embed=True)):
    print("set-torque", aim_torque.torque)
    if dev_mode:
        testvalue.aim_torque = aim_torque.torque
        return {"res": "success"}
    period_client["aim_torque"].set_real(aim_torque.torque)
    return {"res": "success"}


@app.websocket("/heartbeat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("客户端连接成功")
    try:
        if dev_mode:
            heartbeat = None
        else:
            heartbeat = period_client["heartbeat"]
        while True:
            data = await websocket.receive_text()
            if dev_mode:
                testvalue.heartbeat += 1
            else:
                heartvalue = heartbeat.get_value()
                print("心跳值:", heartvalue)
                if heartvalue > 60000:
                    heartvalue = 1  # 心跳从1开始，0表示断开连接
                heartbeat.set_int(heartvalue + 1)
            await asyncio.sleep(0.3)

    except:
        pass
    finally:
        print("心跳断开连接")
        try:
            heartbeat.set_int(0)
            await websocket.close()
        except:
            pass


@app.websocket("/jog_add")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("jog_add")
    if dev_mode:
        while True:
            data = await websocket.receive_text()
            print("jog add: ", data)
    try:
        jog_add = period_client["jog_add"]
        while True:
            data = await websocket.receive_text()
            print("jog add: ", data)
            if data == "exit":
                period_client["jog_add"].set_bool(False)
                break
            jog_add.set_bool(True)

            # await websocket.send_text(f"Message text was: {data}")
    except:
        print("jog add stop")
        period_client["jog_add"].set_bool(False)
    finally:
        print("jog add exit")
        try:
            await websocket.close()
        except:
            pass


@app.websocket("/jog_sub")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("jog_sub")
    if dev_mode:
        while True:
            data = await websocket.receive_text()
            print("jog sub: ", data)
    try:
        jog_add = period_client["jog_sub"]
        while True:
            data = await websocket.receive_text()
            print("jog sub: ", data)
            if data == "exit":
                period_client["jog_sub"].set_bool(False)
                break
            jog_add.set_bool(True)

            # await websocket.send_text(f"Message text was: {data}")
    except:
        print("jog sub stop")
        period_client["jog_sub"].set_bool(False)
    finally:
        print("jog sub exit")
        try:
            await websocket.close()
        except:
            pass


# @app.websocket("/jog_sub")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     print("jog_sub")
#     try:
#         jog_sub = period_client["jog_sub"]
#         while True:
#             data = await websocket.receive_text()
#             print("jog add: ", data)
#             jog_sub.set_bool(True)

#             # await websocket.send_text(f"Message text was: {data}")
#     except:
#         print("jog add stop")
#         period_client["jog_sub"].set_bool(False)
#     finally:
#         print("jog add exit")
#         try:
#             await websocket.close()
#         except:
#             pass


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000, reload=False, workers=1)
