import websockets

class NetworkClient:
    def __init__(self):
        self.uri = "wss://websocket-echo.com/"

    async def run(self):
        async with websockets.connect(self.uri) as websocket:
            name = "Hello World!"

            await websocket.send(name)
            print(f">>> {name}")

            greeting = await websocket.recv()
            print(f"<<< {greeting}")