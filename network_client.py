import asyncio
from asyncio import subprocess, create_subprocess_exec
import ffmpy
from ffmpy import FFmpeg
import websockets
from multiprocessing import Queue

class NetworkClient:
    def __init__(self, input: Queue, output: Queue):
        self.uri = "wss://ws-dummy-production.up.railway.app"
        self.input = input
        self.output = output
        self.websocket = None

    async def _receive_data(self):
        ff = FFmpeg(
            inputs={'pipe:0': None},
            outputs={'pipe:1': '-f s16le -acodec pcm_s16le -ar 44100 -ac 2'}
        )

        while True:
            data = await self.websocket.recv()
            print("Get some data from server!")
            out, _ = ff.run(input_data=data, stdout=subprocess.PIPE)
            print("Convert data to pcm!")
            self.output.put(out)

    async def _send_data(self):
        pass

    async def run(self):
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            await asyncio.gather(
                asyncio.create_task(self._send_data()),
                asyncio.create_task(self._receive_data())
            )


def network_client_main(input: Queue, output: Queue):
    client = NetworkClient(input, output)
    asyncio.run(client.run())