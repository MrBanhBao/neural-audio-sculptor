<script lang="ts">
	import { audioMetaData, currentFrame, isPlaying } from '$lib/stores/store';
	import { onDestroy, onMount } from 'svelte';
	import { getCurrentFrame, setCurrentFrame } from '$lib/apis/audio-api';

	let interval;

	$: numberOfFrames = $audioMetaData.num_frames;

	$: currentTimeStamp = calculateTimestamp($currentFrame, $audioMetaData.sample_rate);
	$: endTimeStamp = calculateTimestamp($audioMetaData.num_frames, $audioMetaData.sample_rate);

	function calculateTimestamp(frame: number, sampleRate: number): string {
		if (frame == null || sampleRate == null) {
			return '--:--';
		} else {
			let minutes: number = frame / sampleRate / 60;
			let seconds: number = (minutes - Math.floor(minutes)) * 60;
			return `${Math.floor(minutes).toString().padStart(2, '0')}:${Math.ceil(seconds).toString().padStart(2, '0')}`;
		}
	}

	async function handleCurrentFrameChange(event: any) {
		let frame = event.target.valueAsNumber;
		const response = await setCurrentFrame({ value: frame } as NumberValue);
	}

	async function updateCurrentFrame() {
		if ($isPlaying) {
			const response = await getCurrentFrame();
			const updatedFrame = (await response.json()).value;
			currentFrame.set(updatedFrame);
		}
	}

	onMount(() => {
		interval = setInterval(updateCurrentFrame, 500);
	});

	onDestroy(() => {
		clearInterval(interval);
	});
</script>

<div class="time-control-container flex flex-col">
	<input
		class="mt-4"
		type="range"
		bind:value={$currentFrame}
		min="0"
		max={numberOfFrames}
		step="1"
		on:input={handleCurrentFrameChange}
	/>
	<div class="time-container flex flex-row justify-between">
		<span>{currentTimeStamp}</span>
		<span>{endTimeStamp}</span>
	</div>
</div>
