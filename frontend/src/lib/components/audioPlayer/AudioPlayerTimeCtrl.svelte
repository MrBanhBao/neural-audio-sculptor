<script lang="ts">
	import { audioMetaData } from '$lib/stores/store';
	import { onDestroy } from 'svelte';

	let currentFrame = 0;
	let numberOfFrames: number | null = null;

	let currentTimeStamp = '--:--';
	let endTimeStamp: string;

	function calculateTimestamp(frame: number, sampleRate: number): string {
		if (frame == null) {
			return '--:--';
		} else {
			let minutes: number = frame / sampleRate / 60;
			let seconds: number = (minutes - Math.floor(minutes)) * 60;
			return `${Math.floor(minutes).toString().padStart(2, '0')}:${Math.ceil(seconds).toString().padStart(2, '0')}`;
		}
	}

	const unsubscribe = audioMetaData.subscribe(() => {
		numberOfFrames = $audioMetaData.num_frames;
		endTimeStamp = calculateTimestamp($audioMetaData.num_frames, $audioMetaData.sample_rate);
	});

	onDestroy(() => {
		unsubscribe();
	});
</script>

<div class="time-control-container flex flex-col">
	<input
		class="mt-4"
		type="range"
		bind:value={currentFrame}
		min="0"
		max={numberOfFrames}
		step="1"
	/>
	<div class="time-container flex flex-row justify-between">
		<span>{currentTimeStamp}</span>
		<span>{endTimeStamp}</span>
	</div>
</div>
