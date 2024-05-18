<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { estimatePose } from '$lib/apis/api';
	import { SlideToggle } from '@skeletonlabs/skeleton';

	export let width: number = 640;
	export let height: nuber = 480;

	let videoElement: HTMLVideoElement;
	let canvasElement: HTMLCanvasElement;
	let active: boolean = false;
	let annotatedImageUrl: string;
	let interval: NodeJS.Timeout = null;

	async function startWebcam() {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ video: true });
			videoElement.srcObject = stream;
			videoElement.play();
		} catch (err) {
			console.error('Error accessing webcam: ', err);
		}
	}

	function captureImage() {
		const context = canvasElement.getContext('2d');
		context?.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
		return canvasElement.toDataURL('image/jpeg');
	}

	function handleClick() {
		if (!active) {
			console.log('start this shit');
			startProcessing();
		} else {
			console.log('stop this shit');
			stopProcessing();
		}
	}

	async function startProcessing() {
		if (interval !== null) return; // Avoid multiple intervals

		interval = setInterval(async () => {
			const capturedImage = captureImage();
			const response = await estimatePose({ value: capturedImage } as StringValue);
			const blob = await response.blob();
			annotatedImageUrl = URL.createObjectURL(blob);
		}, 125);
	}

	function stopProcessing() {
		if (interval !== null) {
			clearInterval(interval);
			interval = null;
		}
	}

	onMount(async () => {
		startWebcam();
	});

	onDestroy(() => {
		clearInterval(interval);
	});

	$: console.log(active);
</script>

<div>
	<video bind:this={videoElement} autoplay style="display: none;"></video>
	<canvas bind:this={canvasElement} width="640" height="480" style="display: none;"></canvas>
	<SlideToggle name="slider-label" bind:checked={active} on:click={handleClick}
		>Pose Estimation</SlideToggle
	>
	{#if annotatedImageUrl}
		<img src={annotatedImageUrl} alt="Processed Image" />
	{/if}
</div>
