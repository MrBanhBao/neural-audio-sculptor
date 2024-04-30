<script lang="ts">
	import { IconPlaylist } from '@tabler/icons-svelte';
	import Modal from '../utils/Modal.svelte';
	import Finder from '$lib/components/finder/Finder.svelte';
	import { loadAudioFile } from '$lib/apis/api';
	import { audioMetaData } from '$lib/stores/store';
	import { onDestroy } from 'svelte';

	let fileName = 'None';
	let showModal = false;

	const unsubscribe = audioMetaData.subscribe(() => {
		fileName = $audioMetaData.file_name;
	});

	onDestroy(() => {
		unsubscribe();
	});
</script>

<header class="card-header flex items-center">
	<button
		type="button"
		class="btn-m variant-filled-primary btn btn-md rounded-full"
		on:click={() => (showModal = true)}
	>
		<span><IconPlaylist stroke="2" /></span>
		<span>Load Music</span>
	</button>
	<span class="pl-4">File: {fileName}</span>
</header>

<Modal bind:showModal title="Music Finder">
	<Finder configKeyName="music_dir" endpointFunction={loadAudioFile}></Finder>
</Modal>
