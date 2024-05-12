<script lang="ts">
	import AudioPlayer from '$lib/components/audioPlayer/AudioPlayer.svelte';
	import ImageRenderer from '$lib/components/imageRenderer/ImageRenderer.svelte';
	import InformationPanel from '$lib/components/informationPanel/InformationPanel.svelte';
	import StyleGanMappingController from '$lib/components/mappingController/StyleGanMappingController.svelte';
	import TransformControll from '$lib/components/mappingController/TransformControll.svelte';
</script>

<div class="flex max-h-[710px] min-h-[710px]">
	<AudioPlayer></AudioPlayer>
	<InformationPanel></InformationPanel>
</div>
<div class="flex">
	<ImageRenderer></ImageRenderer>
	<StyleGanMappingController></StyleGanMappingController>
	<TransformControll />
</div>
