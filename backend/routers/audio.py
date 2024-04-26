from fastapi import APIRouter

router = APIRouter(
    prefix="/audio",
    tags=["audio"],
)


@router.get("/")
async def root():
    return "Hello from the Audio API."
