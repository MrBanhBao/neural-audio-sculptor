const HOST: string | unknown = '127.0.0.1';
const PORT: number | unknown = 8000;

const webSocketUrl = `ws://${HOST}:${PORT}`

export const wsRoutineUrl = `${webSocketUrl}/api/stylegan/ws/routine`


export async function loadModelFile(path: StringValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/stylegan/load/file`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(path)
    })

    return response;
}

export async function getSpeedFeatureInfos() {
    const response = await fetch(`http://${HOST}:${PORT}/api/stylegan/get/speed/feature-mapping`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getWsFeatureInfos() {
    const response = await fetch(`http://${HOST}:${PORT}/api/stylegan/get/ws/feature-mapping`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function setSpeedFeatureInfo(info: FeatureMapInfo) {
    const response = await fetch(`http://${HOST}:${PORT}/api/stylegan/set/speed/feature-mapping`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(info)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function setWsFeatureInfo(info: FeatureMapInfo) {
    const response = await fetch(`http://${HOST}:${PORT}/api/stylegan/set/ws/feature-mapping`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(info)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}
