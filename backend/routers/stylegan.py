import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import utils.store as store
from core.generators.stylegan.wrapper import StyleGan2Ada
from routers.audio import audio_player
from utils import img_array_to_image_byte_pil

router = APIRouter(
    prefix="/stylegan",
    tags=["stylegan"],
)


model_file = "/home/hao/Documents/stylegan2_models/afhqcat.pkl"
generator = StyleGan2Ada(model_file=model_file, device=None)
hop_length = store.config.audio.hop_length

@router.get("/")
async def root():
    pass


@router.websocket("/ws/routine")
async def run_routine(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if audio_player.playback_state.play:
                index = int(audio_player.current_frame / hop_length)
                img_array = generator.routine(index=index)
                img_byte: bytes = img_array_to_image_byte_pil(img_array)
                await websocket.send_bytes(img_byte)
                await asyncio.sleep(0)
            else:
                # release routine when nothing is happening
                await asyncio.sleep(0)
    except WebSocketDisconnect:
        print("Client disconnected")




