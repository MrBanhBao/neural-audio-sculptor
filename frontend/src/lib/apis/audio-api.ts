const HOST: string | unknown = '127.0.0.1';
const PORT: number | unknown = 8000;

const webSocketUrl = `ws://${HOST}:${PORT}`

export const wsRoutineUrl = `${webSocketUrl}/api/stylegan/ws/routine`

export async function loadAudioFile(path: StringValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/load/file`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(path)
    })

    return response;
}

export async function loadAudioCover(path: StringValue) {

    const response = await fetch(`http://${HOST}:${PORT}/api/audio/load/cover`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(path)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getPlaybackState() {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/get/player/playback-state`);

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function updatePlaybackState(playbackState: PlaybackState) {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/update/player/playback-state`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(playbackState)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function setAudioVolume(volume: NumberValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/set/player/volume`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(volume)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getCurrentFrame() {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/get/player/current-frame`);

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function setCurrentFrame(frame: NumberValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/set/player/current-frame`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(frame)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getAudioFile(path: string) {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/get/file/?path=${path}`);

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getSelectedAudioTracks() {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/get/player/selected-audio-tracks`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function setSelectedAudioTrack(selectedAudioTrack: SelectedAudioTrack) {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/set/player/selected-audio-track`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(selectedAudioTrack)
    });

    return response;
}

export async function getFeaturesFile(path: string) {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/get/features/?path=${path}`);

    return response;
}

export async function getTrackAndFeatureNames() {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/get/track-feat-names`);

    return response;
}