<script lang="ts">
	import { onMount } from 'svelte';
	import { getFileStructure } from '$lib/apis/api';
	import yaml from 'js-yaml';
	import Folder from './Folder.svelte';

	export let configKeyName: string = 'music_dir';
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

	onMount(async () => {
		const path = await getPath(configKeyName);
		fileStructure = await requestFileStructure(path);
	});
</script>

{#if fileStructure === undefined}
	<p>Loading...</p>
{:else}
	<Folder name={fileStructure.name} files={fileStructure.files}></Folder>
{/if}
