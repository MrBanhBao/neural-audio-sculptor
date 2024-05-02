<script lang="ts">
	import { IconFileMusic, IconFile, IconRobot } from '@tabler/icons-svelte';
	import { audioMetaData, statusFeedback } from '$lib/stores/store';
	import SquareLetterP from '@tabler/icons-svelte/IconSquareLetterP.svelte';

	export let name: string;
	export let path: string;
	export let endpointFunction: Function;

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
		statusFeedback.set({ status: 'pending', message: 'Loading and splitting audio.' });

		const value: StringValue = { value: path };
		const response = await endpointFunction(value);
		if (response?.ok) {
			const data = (await response.json()) as AudioMetaData;
			audioMetaData.set(data);
			statusFeedback.set({ status: 'successfull', message: 'Done loading and splitting audio.' });
		} else {
			statusFeedback.set({ status: 'failed', message: response.statusText });
		}
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
