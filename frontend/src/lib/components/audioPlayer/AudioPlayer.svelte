<script lang="ts">
	import AudioPlayerHeader from './AudioPlayerHeader.svelte';
	import AudioPlayerInfo from './AudioPlayerInfo.svelte';
	import AudioPlayerTimeCtrl from './AudioPlayerTimeCtrl.svelte';
	import AudioPlayerPlaybackCtrl from './AudioPlayerPlaybackCtrl.svelte';
</script>

<div class="card flex min-w-[400px] max-w-[400px] flex-col p-4">
	<AudioPlayerHeader />
	<section class="flex flex-grow flex-col justify-center">
		<AudioPlayerInfo />
		<AudioPlayerTimeCtrl />
		<AudioPlayerPlaybackCtrl />
	</section>
</div>
