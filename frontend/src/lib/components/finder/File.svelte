<script lang="ts">
	import { IconFileMusic, IconFile, IconRobot } from '@tabler/icons-svelte';
	import { audioMetaData, statusFeedback } from '$lib/stores/store';
	import SquareLetterP from '@tabler/icons-svelte/IconSquareLetterP.svelte';

	export let name: string;
	export let path: string;
	export let endpointFunction: Function;
	export let handleResponseFunction: Function;

	const audioFileExtensions: string[] = [
		'mp3',
		'mp4',
		'm4a',
		'wma',
		'wav',
		'aiff',
		'aac',
		'ogg',
		'flac'
	];
	const pickleFileExtensions: string[] = ['pkl'];

	async function handleClick() {
		statusFeedback.set({ status: 'pending', message: 'Loading data...' });

		const value: StringValue = { value: path };
		const response = await endpointFunction(value);
		handleResponseFunction(response);
	}

	$: fileExtention = name.slice(name.lastIndexOf('.') + 1).toLocaleLowerCase();
</script>

<span on:click={handleClick} class="flex items-center">
	{#if audioFileExtensions.includes(fileExtention)}
		<IconFileMusic />
	{:else if pickleFileExtensions.includes(fileExtention)}
		<IconRobot />
	{:else}
		<IconFile />
	{/if}
	{name}
</span>

<style>
	span {
		cursor: pointer;
		border: none;
		margin: 0;
	}
</style>
