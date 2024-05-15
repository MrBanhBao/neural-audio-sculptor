const HOST: string | unknown = '127.0.0.1';
const PORT: number | unknown = 8000;

const webSocketUrl = `ws://${HOST}:${PORT}`

export const wsRoutineUrl = `${webSocketUrl}/api/diffusion/ws/routine`

export async function getSpeedFeatureInfos() {
    const response = await fetch(`http://${HOST}:${PORT}/api/diffusion/get/speed/feature-mapping`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function setSpeedFeatureInfo(info: FeatureMapInfo) {
    const response = await fetch(`http://${HOST}:${PORT}/api/diffusion/set/speed/feature-mapping`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(info)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}


export async function getLatentFeatureInfos() {
    const response = await fetch(`http://${HOST}:${PORT}/api/diffusion/get/latent/feature-mapping`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}


export async function setLatentFeatureInfo(info: FeatureMapInfo) {
    const response = await fetch(`http://${HOST}:${PORT}/api/diffusion/set/latent/feature-mapping`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(info)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}