import websockets as ws
import asyncio
import json

connections = set()

async def consumer_handler(websocket, path):
    while True:
        msg = await websocket.recv()
        msg_obj = json.loads(msg)
        await consume(msg_obj)

async def producer_handler(websocket, path):
    while True:
        msg_obj = await produce()
        msg = json.dumps(msg_obj)
        await websocket.send(msg)

async def consume(msg):
    print(msg)
    pass

async def produce():
    return 

async def handler(websocket, path):
    connections.add(websocket)
    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when = asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()
    connections.remove(websocket)

async def get_key():
    return 'C major'

async def get_bpm():
    return 120

async def get_suggestions():
    return [0, 1, 2, 3, 4]

methods = {
    'get_key' : get_key,
    'get_bpm' : get_bpm,
    'get_suggestions' : get_suggestions
}

asyncio.get_event_loop().run_until_complete(
    ws.serve(handler, 'localhost', 8888)
)
asyncio.get_event_loop().run_forever()