<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { getFileStructure } from '$lib/apis/api';
	import yaml from 'js-yaml';
	import Folder from './Folder.svelte';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	export let configKeyName: string = 'music_dir';
	export let endpointFunction: Function;

	let milliseconds = 2500;
	let timeout: NodeJS.Timeout;
	let error = false;
	let fileStructure: TypeFolder | undefined;

	async function getPath(configKey: string): Promise<string> {
		const response = await fetch('config.yaml');
		const text = await response.text();
		const configObj = yaml.load(text) as Config;

		let key = configKeyName as keyof Config;
		return configObj.backend[key];
	}

	async function requestFileStructure(path: string): Promise<TypeFolder | undefined> {
		const response = await getFileStructure(path);
		if (response?.ok) {
			const data = await response.json();
			return data as TypeFolder;
		}

		return undefined;
	}

	function setTimer() {
		const timeout = setTimeout(() => {
			if (!fileStructure) {
				error = true;
			}
		}, milliseconds);

		return timeout;
	}

	onMount(async () => {
		const path = await getPath(configKeyName);
		fileStructure = await requestFileStructure(path);

		timeout = setTimer();
	});

	onDestroy(() => {
		clearTimeout(timeout);
	});
</script>

{#if fileStructure === undefined}
	{#if error}
		<div>Error: Failed to load file structure!</div>
	{:else}
		<!-- <span class="flex"><ProgressRadial class="mr-2" width="w-5" text />Loading...</span> -->
		<div>Error: Failed to load file structure!</div>
	{/if}
{:else}
	<Folder name={fileStructure.name} files={fileStructure.files} {endpointFunction}></Folder>
{/if}
