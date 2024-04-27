<script lnag="ts">
	import {
		IconPlayerPlayFilled,
		IconPlayerPauseFilled,
		IconVolume,
		IconVolumeOff,
		IconRepeat,
		IconRepeatOff
	} from '@tabler/icons-svelte';

	let play = true;
	let mute = false;
	let repeat = true;
</script>

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
	<button type="button" class="btn-icon-md variant-filled btn-icon" on:click={() => (mute = !mute)}>
		{#if mute}
			<IconVolume size="24"></IconVolume>
		{:else}
			<IconVolumeOff size="24"></IconVolumeOff>
		{/if}
	</button>
</div>
