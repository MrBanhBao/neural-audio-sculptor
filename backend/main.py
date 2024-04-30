import copy

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

import utils.store as store
from data_models import Folder, Config
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


if __name__ == "__main__":
    uvicorn.run(app, host=store.config.backend.host, port=store.config.backend.port)
