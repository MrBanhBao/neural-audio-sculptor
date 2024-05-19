import { onMount } from 'svelte';
import yaml from 'js-yaml';

// set const
let HOST: string | unknown = '127.0.0.1';
let PORT: number | unknown = 8000;

export async function getConfig() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/config`)

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getFileStructure(path: string) {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/filestructure/?path=${path}`)

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getTransformManual3dArgs() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/manual/transform-3d-args`)

    return response;
}

export async function getTransformMapping3dArgs() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/mapping/transform-3d-args`)

    return response;
}

export async function getTransformationMode() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/transformation/mode`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getPaddingModes() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/args3d/padding-modes`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function setPaddingMode(mode: StringValue) {
    const response = await fetch(`http://${HOST}:${PORT}/set/args3d/padding-mode`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mode)
    });

    return response;
}

export async function setTransformationMode(mode: StringValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/set/transformation/mode`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mode)
    });

    return response;
}


export async function setTransformManual3dArgs(args: Transform3DArgs) {
    const response = await fetch(`http://${HOST}:${PORT}/api/set/manual/transform-3d-args`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(args)
    });

    return response;
}

export async function setTransformMapping3dArgs(args: Transform3DArgs) {
    const response = await fetch(`http://${HOST}:${PORT}/api/set/mapping/transform-3d-args`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(args)
    });

    return response;
}

export async function getTransform3dFeatureInfos() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/args3d/feature-mapping`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}


export async function setTransform3dFeatureInfo(info: FeatureMapInfo) {
    const response = await fetch(`http://${HOST}:${PORT}/api/set/args3d/feature-mapping`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(info)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}


export async function getGeneratorOptions() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/generator-options`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getCurrentGenerator() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/current-generator`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}


export async function setCurrentGenerator(info: StringValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/set/current-generator`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(info)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}



export async function getPoseEstimationActiveState() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/pose/active-state`);
    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function setPoseEstimationActiveState(active: BooleanValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/set/pose/active-state`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(active)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}


export async function estimatePose(data: StringValue) {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/pose`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error(response.statusText)
    }

    return response;
}

export async function getImageInputPreviewData() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/image-preview-data`);

    return response;
}

export async function getImageFile(path: string) {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/image/?path=${path}`);

    return response;
}