<script lang="ts">
	import { setTransform3dArgs } from '$lib/apis/api';
	import { onMount } from 'svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let name: string;
	export let min: number;
	export let max: number;
	export let stepSize: number;
	export let value: number;

	async function onChange(e) {
		dispatch('inputChange', e);
	}
</script>

<div class="flex flex-col">
	<div>
		<span class="ml-2">{name}:</span> <span>{value}</span>
	</div>
	<div>
		<input class="mb-4" type="range" bind:value {min} {max} step={stepSize} on:input={onChange} />
	</div>
</div>
