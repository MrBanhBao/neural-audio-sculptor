<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { estimatePose } from '$lib/apis/api';

	export let width: number = 640;
	export let height: nuber = 480;

	let videoElement: HTMLVideoElement;
	let canvasElement: HTMLCanvasElement;
	let isRunning = false;
	let photo;
	let interval = null;

	async function startWebcam() {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ video: true });
			videoElement.srcObject = stream;
			videoElement.play();
		} catch (err) {
			console.error('Error accessing webcam: ', err);
		}
	}

	// Function to capture an image from the webcam
	function captureImage() {
		const context = canvasElement.getContext('2d');
		context?.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
		return canvasElement.toDataURL('image/jpeg');
	}

	// Function to start the continuous capture and send process
	async function startProcessing() {
		if (interval !== null) return; // Avoid multiple intervals

		interval = setInterval(async () => {
			const capturedImage = captureImage();
			console.log(capturedImage);
			const response = await estimatePose({value: capturedImage} as StringValue);
			console.log(await response.json());
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
</script>

<div>
	<video bind:this={videoElement} autoplay style="display: none;"></video>
	<canvas bind:this={canvasElement} width="640" height="480" style=""></canvas>
	<button on:click={startProcessing}>Start Processing</button>
	<button on:click={stopProcessing}>Stop Processing</button>
	{#if photo}
		<img src={photo} alt="Processed Image" />
	{/if}
</div>
