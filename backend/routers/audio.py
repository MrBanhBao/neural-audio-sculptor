import os
from typing import List

from fastapi import APIRouter, HTTPException, Response, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse

import utils.store as store
from core.audio import AudioLoader, AudioPlayer
from core.audio.utils import split_audio, calculate_audio_features
from data_models import AudioMetaData, StringValue, PlaybackState, FloatValue, IntegerValue, SelectedAudioTrack
from utils import is_splitted, create_directory

router = APIRouter(
    prefix="/audio",
    tags=["audio"],
)

sample_rate = store.config.audio.sample_rate
block_size = store.config.audio.block_size
cache_dir = store.config.backend.cache_dir
track_names = store.track_names

audio_loader = AudioLoader(sample_rate=sample_rate)
audio_player = AudioPlayer(sample_rate=sample_rate, block_size=block_size)


@router.get("/")
async def root():
    return "Hello from the Audio API."


@router.post("/load/file")
def load_audio(audio_path: StringValue, background_tasks: BackgroundTasks) -> AudioMetaData:
    print(f"Loading Audio: {audio_path}...")
    store.isFeaturesReady = False

    audio_data_tracks = {}
    audio_data, audio_meta_data = audio_loader.load_audio(audio_path.value)
    audio_data_tracks["main"] = audio_data
    folder_name = os.path.splitext(audio_meta_data.file_name)[0]
    directory = os.path.join(cache_dir, folder_name)

    files = [os.path.join(directory, f"{track}.wav") for track in track_names[1:]]
    if not is_splitted(files):
        create_directory(directory)
        splitted_audio_data_tracks = split_audio(audio_data=audio_data, save_dir=directory)
    else:
        print(f'Found splitted audio data for {folder_name}.')
        splitted_audio_data_tracks = load_audio_data_tracks(directory, track_names[1:])

    audio_data_tracks.update(splitted_audio_data_tracks)

    # calculate in background
    background_tasks.add_task(calculate_audio_features, audio_data_tracks, folder_name)

    audio_player.set_audio_data_tracks(audio_data_tracks)
    print("Done!")
    return audio_meta_data


def load_audio_data_tracks(directory: str, track_names: List[str]):
    audio_data_tracks = {}
    for track_name in track_names:
        file = os.path.join(directory, f"{track_name}.wav")
        audio, _ = audio_loader.load_audio(file)
        audio_data_tracks[track_name] = audio
    return audio_data_tracks


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


@router.get("/get/player/playback-state")
def get_playback_states() -> PlaybackState:
    try:
        return audio_player.get_playback_states()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update/player/playback-state")
def update_playback_states(playback_states: PlaybackState) -> PlaybackState:
    try:
        audio_player.set_playback_states(playback_states)
        return audio_player.get_playback_states()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/set/player/volume")
def set_audio_volume(volume: FloatValue):
    try:
        print(volume.value)
        audio_player.set_volume(volume.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/player/current-frame")
def get_current_frame() -> JSONResponse:
    try:
        return JSONResponse(content={"value": audio_player.current_frame})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/set/player/current-frame")
def set_current_frame(frame: IntegerValue):
    try:
        audio_player.set_current_frame(frame.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/file")
def get_audio(path: str):
    return FileResponse(path)


@router.get("/get/player/selected-audio-tracks")
def set_current_frame() -> JSONResponse:
    try:
        return audio_player.selected_audio_tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/set/player/selected-audio-track")
def set_current_frame(data: SelectedAudioTrack) -> JSONResponse:
    try:
        success = audio_player.set_selected_audio_tracks(data.name, data.active)
        if success:
            return JSONResponse(status_code=200, content=f"Successfully set {data.name} to {data.active}")
        else:
            return JSONResponse(status_code=500, content=f"Failed set {data.name} to {data.active}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/features")
def get_features(path: str):
    if store.isFeaturesReady:
        return FileResponse(path)
    else:
        return JSONResponse(status_code=500, content=f"Features are not ready yet.")


@router.get("/get/track-feat-names")
def get_features() -> dict[str, List[str]]:
    return {"trackNames": store.track_names, "featureNames": store.feature_names}
