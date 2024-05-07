// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types
declare namespace App {
	// interface Locals {}
	// interface PageData {}
	// interface Error {}
	// interface Platform {}
}

type Config = {
	backend: {
		host: string;
		port: number;
		device: string | null;
		cache_dir: string;
		music_dir: string;
		stylegan_checkpoints: string;
	}
	frontend: {
		host: string;
		port: number;
	}
	audio: {
		sample_rate: number;
		hop_length: number;
		frame_length: number;
	}
}

type TypeFile = {
	name: string;
	path: string;
}

type TypeFolder = {
	name: string;
	files: Array<TypeFile | TypeFolder>
}

type StringValue = {
	value: string;
}

type NumberValue = {
	value: number;
}

type AudioMetaData = {
	artist: string;
	title: string;
	path: string;
	file_name: string;
	num_frames: number;
	sample_rate: number;
	duration: number;
	image: string;
}

type PlaybackState = {
	play: boolean;
	loop: boolean;
	mute: boolean;
}

type StatusFeedback = {
	status: "pending" | "successfull" | "failed" | "idle";
	message: string;
}

type WaveSurferTrack = {
	name: string;
	active: boolean;
	url: string;
}

type SelectedAudioTrack = {
	name: string;
	active: boolean
}

type FeatureTrackInfo = {
	id: string;
	selectedTrack: string;
	selectedFeature: string;
	audioData: number[] | null;
}