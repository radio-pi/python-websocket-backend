from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from pathlib import Path
import json
import asyncio

from .player import PLAYER


class PlayRequest(BaseModel):
    url: str


class VolumeRequest(BaseModel):
    volume: int


class SleepTimerRequest(BaseModel):
    time: int  # in minutes


app = FastAPI()

app.mount("/image", StaticFiles(directory="radiopi/static/image"), name="image")


@app.get("/", response_class=HTMLResponse)
async def index():
    index = Path("radiopi/static/index.html").read_text()
    return HTMLResponse(content=index, status_code=200)


@app.post("/play")
async def play(data: PlayRequest):
    PLAYER.play(data.url)
    return {}


@app.post("/stop")
async def stop():
    PLAYER.stop()
    return {}


@app.get("/volume")
async def volume():
    vol = PLAYER.get_volume()
    return {"volume": f"{vol}"}


@app.post("/volume")
async def volume(data: VolumeRequest):
    PLAYER.set_volume(data.volume)
    return {}


@app.get("/sleeptimer")
async def sleeptimer():
    timeinminutes = PLAYER.get_sleep_timer()
    return {"sleeptimer": f"{timeinminutes}"}


@app.post("/sleeptimer")
async def sleeptimer(data: SleepTimerRequest):
    PLAYER.set_sleep_timer(data.time)
    return {}


@app.post("/sleeptimer/cancle")
async def sleeptimer():
    print("cancel")
    PLAYER.set_sleep_timer(0)
    return {}


@app.get("/streamurls")
async def streamurls():
    streamlist = [
        {
            "name": "Hardbase",
            "url": "http://listen.hardbase.fm/tunein-mp3-pls",
            "img": "/image/Hardbasefm.jpg",
            "orderid": 1,
        },
        {
            "name": "Technobase",
            "url": "http://listen.technobase.fm/tunein-mp3-asx",
            "img": "",
            "orderid": 2,
        },
        {
            "name": "Radio 24",
            "url": "http://icecast.radio24.ch/radio24",
            "img": "https://upload.wikimedia.org/wikipedia/de/thumb/3/33/Radio_24_Logo.svg/154px-Radio_24_Logo.svg.png",
            "orderid": 0,
        },
        {
            "name": "Radio SRF 1",
            "url": "http://stream.srg-ssr.ch/m/drs1/mp3_128",
            "img": "https://www.srf.ch/play/v3/svgs/radio-srf-1-small.svg",
            "orderid": 3,
        },
        {
            "name": "Radio SRF 2",
            "url": "http://stream.srg-ssr.ch/m/drs2/mp3_128",
            "img": "https://www.srf.ch/play/v3/svgs/radio-srf-2-kultur-small.svg",
            "orderid": 4,
        },
        {
            "name": "Radio SRF 3",
            "url": "http://stream.srg-ssr.ch/m/drs3/mp3_128",
            "img": "https://www.srf.ch//play/v3/svgs/radio-srf-3-small.svg",
            "orderid": 5,
        },
        {
            "name": "Radio Swiss Jazz",
            "url": "http://stream.srg-ssr.ch/m/rsj/mp3_128",
            "img": "",
            "orderid": 6,
        },
        {
            "name": "Radio Swiss Pop",
            "url": "http://stream.srg-ssr.ch/m/rsp/mp3_128",
            "img": "",
            "orderid": 7,
        },
    ]

    return streamlist


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

        # State
        self.old_volume = -1
        self.old_title = ""
        self.old_stream_key = ""

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Initial status
        await manager.send_personal_message(
            {"volume": f"{PLAYER.get_volume()}"}, websocket
        )
        await manager.send_personal_message(
            {"title": f"{PLAYER.get_title()}"}, websocket
        )
        await manager.send_personal_message(
            {"stream_key": f"{PLAYER.get_playing_key()}"}, websocket
        )
        while True:
            await asyncio.sleep(0.1)

            # check volume
            volume = PLAYER.get_volume()
            if volume != manager.old_volume:
                manager.old_volume = volume
                await manager.broadcast({"volume": f"{volume}"})

            # check title
            title = PLAYER.get_title()
            if title != manager.old_title:
                manager.old_title = title
                await manager.broadcast({"title": f"{title}"})

            # check stream_key
            key = PLAYER.get_playing_key()
            if key != manager.old_stream_key:
                manager.old_stream_key = key
                await manager.broadcast({"stream_key": f"{key}"})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client #{1} left the chat")
