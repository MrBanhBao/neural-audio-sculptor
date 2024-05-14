<script lang="ts">
	import AudioPlayer from '$lib/components/audioPlayer/AudioPlayer.svelte';
	import ImageRenderer from '$lib/components/imageRenderer/ImageRenderer.svelte';
	import InformationPanel from '$lib/components/panels/InformationPanel.svelte';
	import FeatureMappingController from '$lib/components/featureMappingControllers/FeatureMappingController.svelte';
	import TransformManualController from '$lib/components/transformControllers/manual/TransformManualController.svelte';
	import TransformMappingController from '$lib/components/transformControllers/mapping/TransformMappingController.svelte';
	import TransformController from '$lib/components/transformControllers/TransformController.svelte';
	import MappingPanel from '$lib/components/panels/MappingPanel.svelte';

</script>

<div class="flex max-h-[710px] min-h-[710px]">
	<AudioPlayer></AudioPlayer>
	<InformationPanel></InformationPanel>
</div>
<div class="flex">
	<ImageRenderer></ImageRenderer>
	<MappingPanel></MappingPanel>
</div>
