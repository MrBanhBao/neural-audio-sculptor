<script lang="ts">
	import AudioPlayer from '$lib/components/audioPlayer/AudioPlayer.svelte';
	import AudioTracker from '$lib/components/audioTracker/AudioTracker.svelte';
	import ImageRenderer from '$lib/components/imageRenderer/ImageRenderer.svelte';
	import FeatureTracker from '$lib/components/featureTracker/FeatureTracker.svelte';
	import InformationPanel from '$lib/components/informationPanel/InformationPanel.svelte';
</script>

<div class="flex max-h-[710px] min-h-[710px]">
	<AudioPlayer></AudioPlayer>
	<InformationPanel></InformationPanel>
</div>
<ImageRenderer></ImageRenderer>
