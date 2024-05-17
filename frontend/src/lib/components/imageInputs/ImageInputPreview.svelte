<script lang="ts">
	import { setImageInputDirectory } from '$lib/apis/stream-diffusion-api';
	import { getImageFile } from '$lib/apis/api';
	import { onMount } from 'svelte';

	export let name: string = 'name';
	export let path: string = 'path';
	export let imagePaths: string[] = [];

	let imageUrls: string[] = [];

	async function fetchImage(image: string) {
		const response = await getImageFile(image);
		if (response.ok) {
			const blob = await response.blob();
			return URL.createObjectURL(blob);
		} else {
			console.error('Failed to fetch image:', path);
			return '';
		}
	}

	async function fetchImages(imagePaths) {
		for (let image of imagePaths) {
			const url = await fetchImage(image);
			imageUrls = [...imageUrls, url];
		}
	}

	async function handleClick() {
		const response = await setImageInputDirectory({ value: path } as StringValue);
	}

	onMount(async () => {
		await fetchImages(imagePaths);
	});
</script>

<div class="card variant-ghost-surface m-2 flex w-[350px] flex-col items-center">
	<header class="card-header text-xl">{name}</header>
	<section class="">
		<span class="ml-4">Preview:</span>
		<div class="flex flex-wrap items-center justify-around p-4">
			{#each imageUrls as src}
				<img width={100} {src} class="p-1" />
			{/each}
		</div>
	</section>
	<footer class="card-footer">
		<button type="button" class="variant-filled btn btn-sm" on:click={handleClick}>Choose</button>
	</footer>
</div>
