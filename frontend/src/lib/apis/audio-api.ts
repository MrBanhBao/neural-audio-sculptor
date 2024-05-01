let HOST: string | unknown = '127.0.0.1';
let PORT: number | unknown = 8000;

export async function loadAudioFile(path: StringValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/audio/load/file`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(path)
    })

    if (!response.ok) {
        throw new Error(response.statusText)
    }

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