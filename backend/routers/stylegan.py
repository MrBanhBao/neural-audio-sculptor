from fastapi import APIRouter

router = APIRouter(
    prefix="/stylegan",
    tags=["stylegan"],
)


@router.get("/")
async def root():
    return "Hello from the StyleGan API."
