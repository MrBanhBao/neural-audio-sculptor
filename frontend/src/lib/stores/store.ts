import { readable, writable } from 'svelte/store';

export const config = writable({} as Config)
export const audioMetaData = writable({} as AudioMetaData);
export const currentFrame = writable(0)