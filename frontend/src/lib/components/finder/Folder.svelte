<script lang="ts">
	import File from './File.svelte';
	import { IconFolder, IconFolderOpen } from '@tabler/icons-svelte';

	export let name: string;
	export let files: Array<TypeFolder | TypeFile>;
	export let endpointFunction: Function;

	let expanded = false;

	function toggle() {
		expanded = !expanded;
	}
</script>

<button class="flex flex-row items-center" on:click={toggle}>
	{#if expanded}
		<IconFolderOpen class="icon" />
	{:else}
		<IconFolder class="icon" />
	{/if}
	{name}
</button>

{#if expanded}
	<ul>
		{#each files as file}
			<li>
				{#if 'files' in file}
					<svelte:self {...file} {endpointFunction} />
				{:else}
					<File {...file} {endpointFunction} />
				{/if}
			</li>
		{/each}
	</ul>
{/if}

<style>
	button {
		color: var(--fg-1);
		font-weight: bold;
		cursor: pointer;
		border: none;
		margin: 0;
	}

	button > :global(.icon) {
		margin-right: 0.25em;
	}

	ul {
		padding: 0.2em 0 0 0.5em;
		margin: 0 0 0 0.5em;
		list-style: none;
		border-left: 1px solid rgba(128, 128, 128, 0.4);
	}

	li {
		padding: 0.2em 0;
	}
</style>
