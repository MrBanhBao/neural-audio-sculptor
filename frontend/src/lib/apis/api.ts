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