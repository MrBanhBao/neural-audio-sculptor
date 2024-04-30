<script lang="ts">
	import AudioPlayerHeader from './AudioPlayerHeader.svelte';
	import AudioPlayerInfo from './AudioPlayerInfo.svelte';
	import AudioPlayerTimeCtrl from './AudioPlayerTimeCtrl.svelte';
	import AudioPlayerPlaybackCtrl from './AudioPlayerPlaybackCtrl.svelte';
</script>

<div class="card p-4">
	<AudioPlayerHeader />
	<section class="p-4">
		<AudioPlayerInfo />
		<AudioPlayerTimeCtrl />
		<AudioPlayerPlaybackCtrl />
	</section>
	<footer class="card-footer">(footer)</footer>
</div>
