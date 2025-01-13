from fastapi import FastAPI, WebSocket, Body
from opcua_start import period_client
import asyncio
from pydantic import BaseModel

app = FastAPI(on_shutdown=[period_client.disconnect])


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/getvalue/{node_name}")
async def get_value(node_name: str):
    return {"value": period_client[node_name].get_value()}


@app.put("/torque-start")
async def torque_start():
    print("torque start")
    period_client["start"].set_bool(True)
    return {"res": "success"}


@app.put("/torque-stop")
async def torque_stop():
    print("torque stop")
    period_client["stop"].set_bool(True)
    return {"res": "success"}


class AimTorque(BaseModel):
    torque: float


@app.put("/set-torque")
async def set_torque(aim_torque: AimTorque = Body(embed=True)):
    print("set-torque", aim_torque.torque)
    period_client["aim_torque"].set_real(aim_torque.torque)
    return {"res": "success"}


@app.websocket("/heartbeat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("客户端连接成功")
    try:
        heartbeat = period_client["heartbeat"]
        while True:
            data = await websocket.receive_text()
            heartvalue = heartbeat.get_value()
            print("心跳值:", heartvalue)
            await asyncio.sleep(0.3)
            if heartvalue > 60000:
                heartvalue = 1  # 心跳从1开始，0表示断开连接
            heartbeat.set_int(heartvalue + 1)

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
    try:
        jog_add = period_client["jog_add"]
        while True:
            data = await websocket.receive_text()
            print("jog add: ", data)
            if data == "exit":
                print(3333333333333333333)
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
    try:
        jog_add = period_client["jog_sub"]
        while True:
            data = await websocket.receive_text()
            print("jog sub: ", data)
            if data == "exit":
                print(3333333333333333333)
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
