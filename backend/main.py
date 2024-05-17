import base64
import copy
import io
from typing import List

import uvicorn
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

import utils.store as store
from data_models import Folder, Config, Transform2DArgs, Transform3DArgs, FeatureMapInfo, StringValue
from routers import audio, stream_diffusion, stylegan
from utils import create_nested_file_structure

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        # "http://127.0.0.1:8080",
        #'"http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio.router)
app.include_router(stream_diffusion.router)
app.include_router(stylegan.router)


@app.get("/")
async def root():
    return "Hello from the Main API."


@app.get("/get/filestructure")
def get_filestructure(path: str) -> Folder:
    try:
        return create_nested_file_structure(root_path=path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get/config")
def get_filestructure() -> Config:
    try:
        config = copy.deepcopy(store.config)
        config.backend.device = str(
            config.backend.device
        )  # convert torch.device to str so it is serializable
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get/transform-2d-args")
def get_transform_2d_args() -> Transform2DArgs:
    return store.args_2D

@app.put("/set/transform-2d-args")
def update_transform_2d_args(args2d: Transform2DArgs) -> JSONResponse:
    try:
        store.args_2D = args2d

        return JSONResponse(content="2D args updated successfully.", status_code=201)
    except Exception as e:
        print(e)
        return JSONResponse(content="2D args updated failed.", status_code=500)

@app.get("/get/manual/transform-3d-args")
def get_transform_3d_args() -> Transform3DArgs:
    return store.manual_args_3D

@app.get("/get/mapping/transform-3d-args")
def get_transform_3d_args() -> Transform3DArgs:
    return store.mapping_args_3D


@app.put("/set/manual/transform-3d-args")
def update_transform_3d_args(args3d: Transform3DArgs) -> JSONResponse:
    try:
        store.manual_args_3D = args3d
        return JSONResponse(content="3D args updated successfully.", status_code=201)
    except Exception as e:
        print(e)
        return JSONResponse(content="3D args updated failed.", status_code=500)


@app.put("/set/mapping/transform-3d-args")
def update_transform_3d_args(args3d: Transform3DArgs) -> JSONResponse:
    try:
        store.mapping_args_3D = args3d
        return JSONResponse(content="3D args updated successfully.", status_code=201)
    except Exception as e:
        print(e)
        return JSONResponse(content="3D args updated failed.", status_code=500)

@app.get("/get/transformation/mode")
def get_transformation_mode() -> StringValue:
    value = StringValue(value=store.transformation_mode)
    return value

@app.get("/get/args3d/padding-modes")
def get_padding_modes() -> List[str]:
    return store.padding_modes


@app.post("/set/args3d/padding-mode")
def set_padding_mode(mode: StringValue):
    store.mapping_args_3D.padding_mode = mode.value
    store.manual_args_3D.padding_mode = mode.value
    return True


@app.put("/set/transformation/mode")
def set_transformation_mode(mode: StringValue):
    store.transformation_mode = mode.value
    return True

@app.get("/get/args3d/feature-mapping")
def get_3d_transform_feature_infos() -> List[FeatureMapInfo]:
    return list(store.transform_3d_mapping_dict.values())


@app.post("/set/args3d/feature-mapping")
def modify_3d_transform_feature_infos(featureMapInfo: FeatureMapInfo):
    try:
        feat_id = featureMapInfo.id
        store.transform_3d_mapping_dict[feat_id] = featureMapInfo
        return JSONResponse(content="Modified 3d transform feature mapping successfully.", status_code=201)
    except Exception as e:
        print(e)
        return JSONResponse(content="Failed 3d transform feature mapping successfully.", status_code=500)


@app.get("/get/generator-options")
def get_generator_options() -> List[str]:
    return store.generators

@app.get("/get/current-generator")
def get_current_generator() -> StringValue:
    return StringValue(value=store.current_generator)

@app.post("/set/current-generator")
def set_current_generator(mode: StringValue):
    store.current_generator = mode.value
    return True


@app.post("/get/pose")
def estimate_pose(data: StringValue):
        # Decode base64 image
        #print(data)
        image_data = base64.b64decode(data.value.split(",")[1])
        image = Image.open(io.BytesIO(image_data))
        image.show()
        # Process the image (for example, convert to grayscale)
        #processed_image = ImageOps.grayscale(image)

        #return {"processed_image": f"data:image/png;base64,{processed_image_base64}"}
        return True

if __name__ == "__main__":
    uvicorn.run(app, host=store.config.backend.host, port=store.config.backend.port)
