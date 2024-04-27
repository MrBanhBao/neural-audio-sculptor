<script lang="ts">
	let songTitle = undefined;
	let artist = undefined;
	let coverArt = 'src/lib/music-placeholder.png';
</script>

<div class="audio-info-container flex items-end">
	<img src={coverArt} width="125" alt="artwork of audio file." />
	<div class="p-4">
		{#if songTitle}
			<div class="placeholder mb-2 h-7 w-36 animate-pulse" />
		{:else}
			<div class="text-2xl font-bold">Song Title</div>
		{/if}
		{#if artist}
			<div class="placeholder w-14 animate-pulse" />
		{:else}
			<div class="text">Artist</div>
		{/if}
	</div>
</div>
