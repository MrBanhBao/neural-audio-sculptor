import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse

import utils.store as store
from core.generators.stylegan import StyleGan2Ada
from data_models import FeatureMapInfo, StringValue
from routers.audio import audio_player
from utils import img_array_to_image_byte_pil, set_transform3d_maps

router = APIRouter(
    prefix="/stylegan",
    tags=["stylegan"],
)


model_file = os.path.join(store.config.backend.stylegan_checkpoints, "VisionaryArt.pkl")
generator = StyleGan2Ada(model_file=model_file, device=None)
hop_length = store.config.audio.hop_length

executor = ThreadPoolExecutor()
@router.get("/")
async def root():
    return "Hello from the StlyeGan API."


@router.post("/load/file")
def load_model_file(model_path: StringValue):
    try:
        print(f"Loading Model File: {model_path}...")
        generator.load_model(model_path.value)
        return JSONResponse(status_code=200, content=f"Successfully load model file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def run_blocking_function():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, generate_image)
    return result


def generate_image():
    index = int(audio_player.current_frame / hop_length)

    # update args_3D
    if store.pose_estimation_is_active:
        store.manual_args_3D.rotate_x = store.pose_landmarks["nose"].x * 2 # Todo: hard coded

    feat_args3d = set_transform3d_maps(index=index,
                                       args=store.manual_args_3D,
                                       map_infos=list(store.transform_3d_mapping_dict.values()),
                                       feature_dict=store.audio_features)

    img_array = generator.routine(index=index, transform_args=feat_args3d)
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
