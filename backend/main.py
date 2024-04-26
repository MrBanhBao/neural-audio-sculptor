from fastapi import FastAPI

from routers import audio, diffusion, stylegan

app = FastAPI()

app.include_router(audio.router)
app.include_router(diffusion.router)
app.include_router(stylegan.router)


@app.get("/")
async def root():
    return "Hello from the Main API."
