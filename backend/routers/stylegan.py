import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse

import utils.store as store
from core.generators.stylegan.wrapper import StyleGan2Ada
from data_models import FeatureMapInfo
from routers.audio import audio_player
from utils import img_array_to_image_byte_pil

router = APIRouter(
    prefix="/stylegan",
    tags=["stylegan"],
)


model_file = "/home/hao/Documents/stylegan2_models/metfaces.pkl"
generator = StyleGan2Ada(model_file=model_file, device=None)
hop_length = store.config.audio.hop_length

executor = ThreadPoolExecutor()
@router.get("/")
async def root():
    pass

async def run_blocking_function():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, generate_image)
    return result

def generate_image():
    index = int(audio_player.current_frame / hop_length)
    img_array = generator.routine(index=index, transform_args=store.args_3D)
    img_byte: bytes = img_array_to_image_byte_pil(img_array)
    return img_byte

@router.websocket("/ws/routine")
async def run_routine(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if audio_player.playback_state.play:
                img_byte: bytes = await run_blocking_function()
                await websocket.send_bytes(img_byte)
                # await asyncio.sleep(0)
            else:
                # release routine when nothing is happening
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


@router.post("/delete/speed/feature-mapping")
async def delete_speed_feature_dict(featureMapInfo: FeatureMapInfo) -> JSONResponse:
    try:
        success = generator.delete_speed_feature_dict(featureMapInfo)
        if success:
            return JSONResponse(status_code=200, content=f"Successfully deleted feature mapping.")
        else:
            return JSONResponse(status_code=500, content=f"Failed deleting feature mapping.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/ws/feature-mapping")
async def get_ws_feature_infos() -> List[FeatureMapInfo]:
    print(generator.get_ws_feature_infos())
    return generator.get_ws_feature_infos()

@router.post("/set/ws/feature-mapping")
async def modify_ws_feature_dict(featureMapInfo: FeatureMapInfo) -> JSONResponse:
    try:
        success = generator.modify_ws_feature_dict(featureMapInfo)
        if success:
            return JSONResponse(status_code=200, content=f"Successfully modified feature mapping.")
        else:
            return JSONResponse(status_code=500, content=f"Failed modifying feature mapping.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delete/ws/feature-mapping")
async def delete_ws_feature_dict(featureMapInfo: FeatureMapInfo) -> JSONResponse:
    try:
        success = generator.delete_ws_feature_dict(featureMapInfo)
        if success:
            return JSONResponse(status_code=200, content=f"Successfully deleted feature mapping.")
        else:
            return JSONResponse(status_code=500, content=f"Failed deleting feature mapping.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
