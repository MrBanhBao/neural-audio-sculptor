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

<tr>
	<td class="centered"> <span>{name}: </span></td>
	<td class="centered">
		<div class="flex flex-col items-center">
			<input class="mt-4" type="range" bind:value {min} {max} step={stepSize} on:input={onChange} />
			<span>{value}</span>
		</div>
	</td>
</tr>

<style>
	.centered {
		text-align: center;
		vertical-align: middle;
	}
</style>
