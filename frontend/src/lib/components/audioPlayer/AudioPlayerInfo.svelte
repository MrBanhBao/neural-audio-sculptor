<script lang="ts">
	import { audioMetaData } from '$lib/stores/store';
	import { onMount, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';
	import { loadAudioCover } from '$lib/apis/api';

	let songTitle: string | undefined = undefined;
	let artist: string | undefined = undefined;
	let coverArt: string | undefined = 'images/music-placeholder.png';

	$: {
		fetchCoverArt($audioMetaData.path);
	}

	$: songTitle = $audioMetaData.title;
	$: artist = $audioMetaData.artist;

	async function fetchCoverArt(value: string) {
		if (value != undefined) {
			const path: StringValue = { value: value };
			const response = await loadAudioCover(path);

			if (response?.ok) {
				const imgBlob = await response.blob();
				coverArt = URL.createObjectURL(imgBlob);
			}
		}
	}
</script>

<div class="audio-info-container flex items-end">
	{#if coverArt}
		<img src={coverArt} width="150" alt="Cover artwork of audio file." />
	{/if}
	<div class="p-4">
		{#if songTitle != undefined}
			<div class="text-2xl font-bold" transition:fade>{songTitle}</div>
		{:else}
			<div class="placeholder mb-2 h-7 w-36 animate-pulse" />
		{/if}
		{#if artist}
			<div class="text" transition:fade>{artist}</div>
		{:else}
			<div class="placeholder w-14 animate-pulse" />
		{/if}
	</div>
</div>
