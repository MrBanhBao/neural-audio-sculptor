import { readable, writable } from 'svelte/store';

export const config = writable({} as Config)
export const audioMetaData = writable({} as AudioMetaData);
export const currentFrame = writable(0)
export const isPlaying = writable(false);
export const statusFeedback = writable({ status: "idle", message: "" } as StatusFeedback);

export const audioFileName = writable('');
export const audioTracks = writable();
export const featureTrack = writable();