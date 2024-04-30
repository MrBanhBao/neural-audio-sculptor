<script lang="ts">
	import { audioMetaData } from '$lib/stores/store';
	import { onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';

	let songTitle: string | undefined = undefined;
	let artist: string | undefined = undefined;
	let coverArt: string | undefined = 'images/music-placeholder.png';

	const unsubscribe = audioMetaData.subscribe(() => {
		songTitle = $audioMetaData.title;
		artist = $audioMetaData.artist;
	});

	onDestroy(() => {
		unsubscribe();
	});
</script>

<div class="audio-info-container flex items-end">
	<img src={coverArt} width="125" alt="artwork of audio file." />
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
