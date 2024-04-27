<script lang="ts">
	import { IconPlaylist } from '@tabler/icons-svelte';
	import Modal from '../utils/Modal.svelte';
	let fileName = 'None';
	let showModal = false;
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
<Modal bind:showModal title="Music Finder">Test</Modal>
