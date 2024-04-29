import copy

from fastapi import FastAPI
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
        "http://127.0.0.1:8080",
        "http://localhost:8080",
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
    return create_nested_file_structure(root_path=path)


@app.get("/get/config")
def get_filestructure() -> Config:
    config = copy.deepcopy(store.config)
    # convert torch.device to str so it is serializable
    config.backend.device = str(config.backend.device)
    return config
