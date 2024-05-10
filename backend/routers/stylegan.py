from fastapi import APIRouter

from core.generators.stylegan.wrapper import StyleGan2Ada

router = APIRouter(
    prefix="/stylegan",
    tags=["stylegan"],
)


model_file = "/home/hao/Documents/stylegan2_models/afhqcat.pkl"
generator = StyleGan2Ada(model_file=model_file, device=None)

@router.get("/")
async def root():
    t = generator.routine(index=10)
    print(t.shape)
    pass



