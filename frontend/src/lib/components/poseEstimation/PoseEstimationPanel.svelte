<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import {
		estimatePose,
		getPoseEstimationActiveState,
		setPoseEstimationActiveState
	} from '$lib/apis/api';
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

	async function handleClick() {
		if (!active) {
			console.log('start this shit');
			const response = await setPoseEstimationActiveState({ value: true } as BooleanValue);
			if (!response.ok) {
				return;
			}
			active = true;
			startProcessing();
		} else {
			const response = await setPoseEstimationActiveState({ value: false } as BooleanValue);
			if (!response.ok) {
				return;
			}
			active = false;
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
		}, 150);
	}

	function stopProcessing() {
		if (interval !== null) {
			clearInterval(interval);
			interval = null;
		}
	}

	onMount(async () => {
		startWebcam();
		const response = await getPoseEstimationActiveState();
		const data = await response.json();
		active = data.value;
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
