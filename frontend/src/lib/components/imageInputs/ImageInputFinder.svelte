<script lang="ts">
	import { getImageInputPreviewData } from '$lib/apis/api';
	import ImageInputPreview from './ImageInputPreview.svelte';
	import { onMount } from 'svelte';

	let previewData: ImageInputPreview[] = [];

	async function fetchImageInputPreviewData() {
		const response = await getImageInputPreviewData();
		const data = await response.json();
		return data;
	}

	onMount(async () => {
		previewData = await fetchImageInputPreviewData();
	});
</script>

<div class="flex flex-wrap justify-evenly">
	{#each previewData as preview}
		<ImageInputPreview name={preview.name} path={preview.path} imagePaths={preview.images}
		></ImageInputPreview>
	{/each}
</div>
