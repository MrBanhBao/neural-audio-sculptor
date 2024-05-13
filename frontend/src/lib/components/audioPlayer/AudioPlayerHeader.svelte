<script lang="ts">
	import { IconPlaylist } from '@tabler/icons-svelte';
	import Modal from '../utils/Modal.svelte';
	import Finder from '$lib/components/finder/Finder.svelte';
	import { loadAudioFile } from '$lib/apis/audio-api';
	import { audioMetaData, statusFeedback } from '$lib/stores/store';
	import { onDestroy } from 'svelte';

	let fileName = 'None';
	let showModal = false;

	const unsubscribe = audioMetaData.subscribe(() => {
		fileName = $audioMetaData.file_name;
	});

	onDestroy(() => {
		unsubscribe();
	});

	async function handleResponseFunction(response) {
		if (response?.ok) {
			const data = (await response.json()) as AudioMetaData;
			audioMetaData.set(data);
			statusFeedback.set({ status: 'successfull', message: 'Done loading and splitting audio.' });
		} else {
			console.log('failed');
			statusFeedback.set({ status: 'failed', message: response.statusText });
		}
	}
</script>

<header class="card-header flex flex-col items-start">
	<button
		type="button"
		class="btn-m variant-filled-primary btn btn-md rounded-full"
		on:click={() => (showModal = true)}
	>
		<span><IconPlaylist stroke="2" /></span>
		<span>Load Music</span>
	</button>
	<span class="mt-4">File: {fileName}</span>
</header>

<Modal bind:showModal title="Music Finder">
	<Finder configKeyName="music_dir" endpointFunction={loadAudioFile} {handleResponseFunction}
	></Finder>
</Modal>
