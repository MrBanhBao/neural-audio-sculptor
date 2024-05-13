<script lang="ts">
	import { wsRoutineUrl } from '$lib/apis/stylegan-api';
	import { onMount, onDestroy } from 'svelte';
	import { IconPaint, IconWindowMaximize } from '@tabler/icons-svelte';
	import Modal from '../utils/Modal.svelte';
	import Finder from '$lib/components/finder/Finder.svelte';
	import { loadModelFile } from '$lib/apis/stylegan-api';
	import { statusFeedback } from '$lib/stores/store';

	let ws: WebSocket;
	let isConnected = false;
	let winRef: Window | null = null;
	let imgSrc: string = '/images/img-placeholder.jpg';

	let showModal = false;

	function connectWebSocket() {
		ws = new WebSocket(wsRoutineUrl);

		ws.binaryType = 'arraybuffer'; // Specify that binary data will be received as ArrayBuffer

		ws.onopen = (event) => {
			console.log('WebSocket connection opened:', event);
			isConnected = true;
		};

		ws.onmessage = (event) => {
			const arrayBuffer = event.data;
			const blob = new Blob([arrayBuffer], { type: 'image/jpeg' });
			const objectURL: string = URL.createObjectURL(blob);
			imgSrc = objectURL;
		};

		ws.onclose = (event) => {
			console.log('WebSocket connection closed:', event);
		};

		ws.onerror = (event) => {
			console.error('WebSocket error:', event);
		};
	}

	function reconnectWebSocket() {
		if (!isConnected) {
			console.log('Reconnecting WebSocket...');
			connectWebSocket();
		}
	}

	function disconnectWebSocket() {
		ws?.close();
	}

	onMount(() => {
		connectWebSocket();
	});

	onDestroy(() => {
		isConnected = false;
		disconnectWebSocket();
	});

	function openImage() {
		const features = 'width=512,height=512';
		winRef = window.open('Test', '_blank');

		const content = `
            <style>
                body {
                    background-color: black;
                    margin: 0;
                    padding: 0;
                }

                .image-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
            </style>
            <div class="image-container">
                <img id="image" src=${imgSrc} alt="Image" style="width: auto; height: 100%;">
            </div>`;
		winRef?.document.write(content);
	}

	function updateImage(newImg: string) {
		if (winRef) {
			winRef.document.getElementById('image').src = newImg; // Update directly
		}
	}

	$: {
		updateImage(imgSrc);
	}

	async function handleResponseFunction(response) {
		if (response?.ok) {
			statusFeedback.set({ status: 'successfull', message: 'Done loading model file.' });
		} else {
			console.log('failed');
			statusFeedback.set({ status: 'failed', message: response.statusText });
		}
	}
</script>

<div class="card min-w-[400px] max-w-[400px] p-4">
	<div class="mb-2">
		<img width="360" src={imgSrc} alt="generated for music viz." />
	</div>
	<div>
		<button
			type="button"
			class="btn-m variant-filled-primary btn btn-md rounded-full"
			on:click={() => (showModal = true)}
		>
			<span><IconPaint /></span>
			<span>Load Model</span>
		</button>
		<button type="button" class="variant-filled btn-icon" on:click={openImage}
			><IconWindowMaximize /></button
		>
	</div>
</div>

<Modal bind:showModal title="StyleGan Models">
	<Finder
		configKeyName="stylegan_checkpoints"
		endpointFunction={loadModelFile}
		{handleResponseFunction}
	></Finder>
</Modal>
