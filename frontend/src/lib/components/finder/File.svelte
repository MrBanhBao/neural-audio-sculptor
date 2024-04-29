<script lang="ts">
	import { IconFileMusic, IconFile, IconRobot } from '@tabler/icons-svelte';

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
		endpointFunction();
		console.log('Clicked');
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
