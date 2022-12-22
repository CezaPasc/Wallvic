import asyncio
import os
if os.getenv("ENV")!="TEST":
    from wall.matrix import Matrix
import websockets
import json

import config


class Server(object):

    def __init__(self):
        self.matrix = None
        self.init_matrix()

    def init_matrix(self):
        if os.getenv("ENV")!="TEST":
            self.matrix = Matrix(
                led_count=419,
                rows=config.ROWS,
                length=config.LENGTH,
                pin=config.DATA_PIN,
                dead_pixels=config.DEAD_PIXELS
            )
        


    async def handle(self, websocket, path):
        print("Listening socket messages...")
        current_matrix = self.matrix.get_colors()
        await websocket.send(json.dumps({"topic": "init", "msg": current_matrix}))

        while True:
            data = await websocket.recv()
            if data == "CLEAR":
                if os.getenv("ENV")!="TEST":
                    self.matrix.clear()
                continue

            reply = f"Data recieved as:  {data}!"
            j = json.loads(data)
            print(reply)

            pos, c_d = j["pos"], j["color"]
            x, y = pos[0], pos[1]
            h = c_d.lstrip("#")
            color = tuple(int(h[i:i+2], 16) for i in (2, 0, 4))
            print(pos, color)
            if os.getenv("ENV")!="TEST":
                self.matrix.set_pixel(x, y, color)
            await websocket.send({"topic": "update_on", "msg": color})

    def run(self):
        start_server = websockets.serve(json.dumps(self.handle, '0.0.0.0', 5678))

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

