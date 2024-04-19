import asyncio
from asyncio import subprocess, create_subprocess_exec
import ffmpy
from ffmpy import FFmpeg
import websockets
from multiprocessing import Queue
import wave

class NetworkClient:
    def __init__(self, input: Queue, output: Queue):
        self.uri = "wss://deepgram-ws-production.up.railway.app"
        self.input = input
        self.output = output
        self.websocket = None

    async def _receive_data(self):
        print("Start receiving data!")
        with wave.open('music.wav', 'rb') as wav_file:
            frames = wav_file.getnframes()
            sample_width = wav_file.getsampwidth()
            channels = wav_file.getnchannels()
            print(f"File for playing is loaded! Frames: {frames}, Channels: {channels}, Sample Width: {sample_width}")
            data = wav_file.readframes(frames)
            
            chunk_frames = 1024 # Frames
            chunk_bytes = chunk_frames * channels * sample_width
            chunks = [data[i:i + chunk_bytes] for i in range(0, len(data), chunk_bytes)]
            print(f"Number of chunks to play: {len(chunks)}")

            await asyncio.sleep(10)

            for chunk in chunks:
                self.output.put(chunk)
                await asyncio.sleep(0.03)
            print("All chunks are sent!")

        # while True:
        #     data = await self.websocket.recv()
        #     print("Get some data from server!")
        #     # out, _ = ff.run(input_data=data, stdout=subprocess.PIPE)
        #     self.output.put(data)
        #     await asyncio.sleep(0)

    async def _send_data(self):
        # while True:
        #     data = self.input.get()
        #     await self.websocket.send(data)
        #     # print("Data is sent!")
        #     await asyncio.sleep(0)
        pass

    async def run(self):
        await asyncio.gather(
            asyncio.create_task(self._send_data()),
            asyncio.create_task(self._receive_data())
        )
        # async with websockets.connect(self.uri) as websocket:
        #     self.websocket = websocket
        #     await asyncio.gather(
        #         asyncio.create_task(self._send_data()),
        #         asyncio.create_task(self._receive_data())
        #     )


def network_client_main(input: Queue, output: Queue):
    client = NetworkClient(input, output)
    asyncio.run(client.run())
