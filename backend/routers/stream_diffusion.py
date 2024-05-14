from fastapi import APIRouter

router = APIRouter(
    prefix="/diffusion",
    tags=["diffusion"],
)


@router.get("/")
async def root():
    return "Hello from the Diffusion API."
