from fastapi import APIRouter, HTTPException, Response

from core.audio import AudioLoader
from data_models import AudioMetaData, StringValue

router = APIRouter(
    prefix="/audio",
    tags=["audio"],
)


audio_loader = AudioLoader()

@router.get("/")
async def root():
    return "Hello from the Audio API."

@router.post("/load/file")
def load_audio(audio_path: StringValue) -> AudioMetaData:
    try:
        audio_data, audio_meta_data = audio_loader.load_audio(audio_path.value)
        print("here i am")
        return audio_meta_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load/cover")
def load_audio(audio_path: StringValue) -> Response:
    try:
        img_bytes = audio_loader.load_cover(audio_path.value)
        if img_bytes is not None:
            return Response(content=img_bytes, media_type="image/jpeg")
        else:
            raise HTTPException(status_code=500, detail="There is no cover.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))