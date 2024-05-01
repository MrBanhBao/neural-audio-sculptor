from typing import Dict, Union

import numpy as np
import numpy.typing as npt
import sounddevice as sd

from data_models import PlaybackState


class AudioPlayer:
    """
    Class which can outputs audio data via sound devices.

    Args:
        audio_tracks (Union[Dict[str, npt.NDArray[np.float32]], None]): Dictionary with key value pairs, where value is audio data.
        sample_rate (int): Sample rate of the audio data.
        block_size (int): Block size which will be read while playing audio frame.
    Attributes:
        audio_tracks (Dict[str, NDArray[Shape["*"], Float32]]): Dictionary with key value pairs, where value is audio data.
        sample_rate (int): Sample rate of the audio data.
        block_size (int): Block size which will be read while playing audio frame.
        selected_audio_tracks (Dict[str, bool]): Chosen audio data from audio_tracks.
        out_stream (sounddevice.OutputStream): Out stream to write audio data to an output device.
        current_frame (int): Current frame of the played audio.
        playback_state (PlaybackState): contains booleans for play, loop and mute
    """

    def __init__(
            self,
            audio_tracks: Union[Dict[str, npt.NDArray[np.float32]], None] = None,
            sample_rate: int = 44100,
            block_size: int = 512,
    ) -> None:
        self.audio_tracks: Dict[str, npt.NDArray[np.float32]] = audio_tracks
        self.sample_rate: int = sample_rate
        self.block_size: int = block_size
        self.selected_audio_tracks: Union[Dict[str, bool], None] = None
        self.out_stream: Union[sd.OutputStream, None] = None
        self.current_frame: int = 0
        self.playback_state: PlaybackState = PlaybackState()
        self.volume: float = 1
        self.previous_volume: float = self.volume

    def set_audio_data_tracks(
        self, audio_tracks: Dict[str, npt.NDArray[np.float32]]
    ) -> None:
        self.audio_tracks = audio_tracks
        self.current_frame = 0
        # per default main is on
        self.selected_audio_tracks = {
            track_name: True if track_name == "main" else False for track_name in self.audio_tracks.keys()
        }

        if self.out_stream is None:
            self.create_output_stream()

    def create_output_stream(self):
        if self.audio_tracks is not None:
            self.out_stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=list(self.audio_tracks.values())[0].shape[1],
                blocksize=self.block_size,
                callback=self._callback,
                #finished_callback=self._check_loop,
            )

            if self.play:
                self.out_stream.start()

    def _callback(self, outdata, frames, time, status) -> None:
        chunk_size = min(
            len(list(self.audio_tracks.values())[0]) - self.current_frame, frames
        )

        out_audio_chunk: npt.NDArray[np.float32] = self._create_out_audio_chunk(
            chunk_size=chunk_size, frames=frames
        )

        outdata[:chunk_size] = self.volume * out_audio_chunk
        self.current_frame += chunk_size

        # signals stream to end
        if self.current_frame >= len(self.audio_tracks['main']):
            self._check_loop()

    def _create_out_audio_chunk(self, chunk_size: int, frames: int) -> npt.NDArray[np.float32]:
        out_audio_chunk: npt.NDArray[np.float32] = np.zeros((chunk_size, 2))
        for track_name, selected in self.selected_audio_tracks.items():
            if selected:
                track_audio_chunk = self.audio_tracks[track_name][
                                    self.current_frame: self.current_frame + chunk_size
                                    ]
                out_audio_chunk += track_audio_chunk
                out_audio_chunk = out_audio_chunk
        return out_audio_chunk

    def _check_loop(self) -> None:
        if self.playback_state.loop and self.playback_state.play:
            self.current_frame = 0
        else:
            self.playback_state.play = False
            self.current_frame = 0
            self.out_stream.stop()

    def get_playback_states(self) -> PlaybackState:
        return self.playback_state

    def set_playback_states(self, playback_states: PlaybackState) -> None:
        self.playback_state = playback_states

        if self.playback_state.play:
            self.out_stream.start()
        else:
            self.out_stream.stop()

        if self.playback_state.mute:
            self.previous_volume = self.volume
            self.volume = 0
        else:
            self.volume = self.previous_volume

    def modify_selected_audio_tracks(self, key: str, value: bool) -> bool:
        if key in self.selected_audio_tracks:
            self.selected_audio_tracks[key] = value
            return True
        else:
            return False

    def set_volume(self, volume: float) -> None:
        if volume > 1.3:  # todo magic number
            self.volume = 1.3
        else:
            self.volume = volume
            if self.volume == 0:
                self.playback_state.mute = True
            else:
                self.playback_state.mute = False

    def set_current_frame(self, frame: int) -> None:
        # TODO if clauses
        self.current_frame = frame