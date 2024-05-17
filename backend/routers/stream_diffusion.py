import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse

import utils.store as store
from core.generators.stream_diffusion import StreamDiffuser
from data_models import FeatureMapInfo, StringValue
from routers.audio import audio_player
from utils import img_pil_to_bytes, set_transform3d_maps

router = APIRouter(
    prefix="/diffusion",
    tags=["diffusion"],
)

image_dir = '/home/hao/Downloads/00000'
generator = StreamDiffuser(image_dir)
hop_length = store.config.audio.hop_length

executor = ThreadPoolExecutor()
@router.get("/")
async def root():
    return "Hello from the StreamDiffusion API."


async def run_blocking_function():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, generate_image)
    return result


def generate_image():
    index = int(audio_player.current_frame / hop_length)

    # update args_3D
    #if store.transformation_mode == "mapping":
    feat_args3d = set_transform3d_maps(index=index,
                                       args=store.manual_args_3D,
                                       map_infos=list(store.transform_3d_mapping_dict.values()),
                                       feature_dict=store.audio_features)
    #else:
    #    feat_args3d = store.manual_args_3D

    img_array = generator.routine(index=index, transform_args=feat_args3d)
    img_byte: bytes = img_pil_to_bytes(img_array)
    return img_byte


@router.websocket("/ws/routine")
async def run_routine(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if audio_player.playback_state.play:
                img_byte: bytes = await run_blocking_function()
                await websocket.send_bytes(img_byte)
            else:
                # release coroutine when nothing is happening
                await asyncio.sleep(0)
    except WebSocketDisconnect:
        print("Client disconnected")


@router.get("/get/speed/feature-mapping")
async def get_speed_feature_infos() -> List[FeatureMapInfo]:
    return generator.get_speed_feature_infos()


@router.post("/set/speed/feature-mapping")
async def modify_speed_feature_dict(featureMapInfo: FeatureMapInfo) -> JSONResponse:
    try:
        success = generator.modify_speed_feature_dict(featureMapInfo)
        if success:
            return JSONResponse(status_code=200, content=f"Successfully modified feature mapping.")
        else:
            return JSONResponse(status_code=500, content=f"Failed modifying feature mapping.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/latent/feature-mapping")
async def get_latent_feature_infos() -> List[FeatureMapInfo]:
    return generator.get_latent_feature_infos()

@router.post("/set/latent/feature-mapping")
async def modify_latent_feature_dict(featureMapInfo: FeatureMapInfo) -> JSONResponse:
    try:
        success = generator.modify_latent_feature_dict(featureMapInfo)
        if success:
            return JSONResponse(status_code=200, content=f"Successfully modified feature mapping.")
        else:
            return JSONResponse(status_code=500, content=f"Failed modifying feature mapping.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/prompt")
async def get_prompt() -> StringValue:
    return StringValue(value=generator.store.prompt)


@router.post("/set/prompt")
async def set_prompt(prompt: StringValue) -> JSONResponse:
    try:
        success = generator.set_prompt(prompt.value)
        if success:
            return JSONResponse(status_code=200, content=f"Successfully setting prompt.")
        else:
            return JSONResponse(status_code=500, content=f"Failed setting prompt.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))