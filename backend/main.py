import copy
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

import utils.store as store
from data_models import Folder, Config, Transform2DArgs, Transform3DArgs, FeatureMapInfo
from routers import audio, diffusion, stylegan
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
app.include_router(diffusion.router)
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


@app.get("/get/transform-3d-args")
def get_transform_3d_args() -> Transform3DArgs:
    return store.args_3D


@app.put("/set/transform-2d-args")
def update_transform_2d_args(args2d: Transform2DArgs) -> JSONResponse:
    try:
        store.args_2D = args2d

        return JSONResponse(content="2D args updated successfully.", status_code=201)
    except Exception as e:
        print(e)
        return JSONResponse(content="2D args updated failed.", status_code=500)


@app.put("/set/transform-3d-args")
def update_transform_3d_args(args3d: Transform3DArgs) -> JSONResponse:
    try:
        store.args_3D = args3d
        return JSONResponse(content="3D args updated successfully.", status_code=201)
    except Exception as e:
        print(e)
        return JSONResponse(content="3D args updated failed.", status_code=500)

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


if __name__ == "__main__":
    uvicorn.run(app, host=store.config.backend.host, port=store.config.backend.port)
