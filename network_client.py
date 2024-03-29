import asyncio
import websockets

class NetworkClient:
    def __init__(self, input: asyncio.Queue, output: asyncio.Queue):
        self.uri = "wss://ws-dummy-production.up.railway.app"
        self.input = input
        self.output = output
        self.websocket = None

    async def _receive_data(self):
        while True:
            data = await self.websocket.recv()
            await self.output.put(data)


    async def _send_data(self):
        pass

    async def run(self):
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket

            await asyncio.gather(
                asyncio.create_task(self._receive_data())
            )