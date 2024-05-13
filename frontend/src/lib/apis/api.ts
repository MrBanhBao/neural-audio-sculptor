import { onMount } from 'svelte';
import yaml from 'js-yaml';

// read config
// const configFile: string = fs.readFileSync('../config.yaml', 'utf8');
// const config = yaml.load(configFile);

// set const
let HOST: string | unknown = '127.0.0.1';
let PORT: number | unknown = 8000;

//const response = await fetch('config.yaml');
//const text = await response.text();
//const config = yaml.load(text);

/* onMount(async () => {
    try {
        const response = await fetch('../config.yaml');
        const text = await response.text();
        const config = yaml.load(text);

        HOST = config.backend.host;
        PORT = config.backend.port;
        console.log(HOST, PORT)
    } catch (error) {
        console.error('Error reading YAML file:', error);
    }
}); */

// API endpoints

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


/* export async function getTransform2dArgs() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/transform-2d-args`)

    return response;
} */

export async function getTransform3dArgs() {
    const response = await fetch(`http://${HOST}:${PORT}/api/get/transform-3d-args`)

    return response;
}

/* export async function setTransform2dArgs(args: Transform2DArgs) {
    const response = await fetch(`http://${HOST}:${PORT}/api/set/transform-2d-args`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(args)
    });

    return response;
} */

export async function setTransform3dArgs(args: Transform3DArgs) {
    const response = await fetch(`http://${HOST}:${PORT}/api/set/transform-3d-args`, {
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
