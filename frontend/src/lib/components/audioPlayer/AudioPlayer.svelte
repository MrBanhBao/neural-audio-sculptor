<script lang="ts">
	import {
		IconPlayerPlayFilled,
		IconPlaylist,
		IconPlayerPauseFilled,
		IconVolume,
		IconVolumeOff,
		IconRepeat,
		IconRepeatOff
	} from '@tabler/icons-svelte';

	let fileName = 'None';
	let coverArt = 'src/lib/music-placeholder.png';

	let currentFrame = 50;
	let numberOfFrames = 100;

	let currentTimeStamp = '--:--';
	let endTimeStamp = '--:--';

	let play = true;
	let mute = false;
	let repeat = true;
</script>

<div class="card p-4">
	<header class="card-header flex items-center">
		<button type="button" class="btn-m variant-filled-primary btn btn-md rounded-full">
			<span><IconPlaylist stroke="2" /></span>
			<span>Load Music</span>
		</button>
		<span class="pl-4">{fileName}</span>
	</header>
	<section class="p-4">
		<div class="audio-info-container flex items-end">
			<img src={coverArt} width="125" alt="artwork of audio file." />
			<div class="p-4">
				<div class="text-2xl font-bold">Song Title</div>
				<div class="text">Artist</div>
			</div>
		</div>
		<div class="time-control-container flex flex-col">
			<input
				class="mt-4"
				type="range"
				bind:value={currentFrame}
				min="0"
				max={numberOfFrames}
				step="1"
			/>
			<div class="time-container flex flex-row justify-between">
				<span>{currentTimeStamp}</span>
				<span>{endTimeStamp}</span>
			</div>
		</div>
		<div class="playback-container flex items-center justify-center">
			<button
				type="button"
				class="btn-icon-md variant-filled btn-icon"
				on:click={() => (repeat = !repeat)}
			>
				{#if repeat}
					<IconRepeatOff size="24"></IconRepeatOff>
				{:else}
					<IconRepeat size="24"></IconRepeat>
				{/if}
			</button>
			<button
				type="button"
				class="variant-filled btn-icon btn-icon-xl ml-4 mr-4"
				on:click={() => (play = !play)}
			>
				{#if play}
					<IconPlayerPauseFilled size="46"></IconPlayerPauseFilled>
				{:else}
					<IconPlayerPlayFilled size="46"></IconPlayerPlayFilled>
				{/if}
			</button>
			<button
				type="button"
				class="btn-icon-md variant-filled btn-icon"
				on:click={() => (mute = !mute)}
			>
				{#if mute}
					<IconVolume size="24"></IconVolume>
				{:else}
					<IconVolumeOff size="24"></IconVolumeOff>
				{/if}
			</button>
		</div>
	</section>
	<footer class="card-footer">(footer)</footer>
</div>
