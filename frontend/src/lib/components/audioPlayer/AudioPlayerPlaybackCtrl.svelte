<script lang="ts">
	import {
		IconPlayerPlayFilled,
		IconPlayerPauseFilled,
		IconVolume,
		IconVolumeOff,
		IconRepeat,
		IconRepeatOff
	} from '@tabler/icons-svelte';
	import { onMount } from 'svelte';
	import { isPlaying } from '$lib/stores/store';
	import { getPlaybackState, updatePlaybackState, setAudioVolume } from '$lib/apis/audio-api';

	let playbackState: PlaybackState = { play: false, loop: true, mute: false };
	let volume: number = 1;
	let maxVolume: number = 1.3;

	async function fetchPlaybackState() {
		const response = await getPlaybackState();
		playbackState = await response.json();
	}

	async function handleVolumeChange(event: any) {
		volume = event.target.valueAsNumber;
		const response = await setAudioVolume({ value: volume } as NumberValue);
	}

	async function togglePlaybackState(playbackType: string) {
		let tempPlaybackState: PlaybackState = JSON.parse(JSON.stringify(playbackState));
		const key = playbackType as keyof PlaybackState;
		if (tempPlaybackState[key]) {
			tempPlaybackState[key] = false;
		} else {
			tempPlaybackState[key] = true;
		}

		const response = await updatePlaybackState(tempPlaybackState);
		playbackState = await response.json();
		isPlaying.set(playbackState.play);
	}

	onMount(async () => {
		fetchPlaybackState;
	});
</script>

<div class="playback-container flex items-center justify-center">
	<button
		type="button"
		class="btn-icon-md variant-filled btn-icon"
		on:click={() => togglePlaybackState('loop')}
	>
		{#if playbackState.loop}
			<IconRepeat size="24"></IconRepeat>
		{:else}
			<IconRepeatOff size="24"></IconRepeatOff>
		{/if}
	</button>
	<button
		type="button"
		class="variant-filled btn-icon btn-icon-xl ml-4 mr-4"
		on:click={() => togglePlaybackState('play')}
	>
		{#if playbackState.play}
			<IconPlayerPauseFilled size="46"></IconPlayerPauseFilled>
		{:else}
			<IconPlayerPlayFilled size="46"></IconPlayerPlayFilled>
		{/if}
	</button>
	<button
		type="button"
		class="btn-icon-md variant-filled btn-icon"
		on:click={() => togglePlaybackState('mute')}
	>
		{#if playbackState.mute}
			<IconVolumeOff size="24"></IconVolumeOff>
		{:else}
			<IconVolume size="24"></IconVolume>
		{/if}
	</button>
	<input
		class="ml-1 w-28"
		type="range"
		id="slider"
		bind:value={volume}
		min="0"
		max={maxVolume}
		step="0.01"
		on:input={handleVolumeChange}
	/>
</div>
