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
	import { getPlaybackState, updatePlaybackState } from '$lib/apis/audio-api';

	let playbackState: PlaybackState = { play: false, loop: true, mute: false };

	async function fetchPlaybackState() {
		const response = await getPlaybackState();
		playbackState = await response.json();
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
</div>
