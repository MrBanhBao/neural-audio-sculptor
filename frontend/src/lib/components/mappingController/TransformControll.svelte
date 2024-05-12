<script lang="ts">
	import { getTransform3dArgs, setTransform3dArgs } from '$lib/apis/api';
	import { onMount } from 'svelte';

	let args3d: Transform3DArgs = get3dArgs();
	let value = 0;

	async function get3dArgs() {
		const reponse = await getTransform3dArgs();
		const data = await reponse.json();

		if (reponse.ok) {
			console.log(data);
			return data;
		} else {
			throw new Error(data);
		}
	}

	onMount(async () => {});

	async function onChange(e) {
		const response = await setTransform3dArgs(args3d);
		const data = await response.json();
		console.log(data);
	}
</script>

{#await args3d}
	<p>...waiting</p>
{:then there}
	<div class="card p-4">
		<div class="flex flex-col items-center">
			<input
				class="mt-4"
				type="range"
				bind:value={args3d.rotate_x}
				min="-2"
				max="2"
				step="0.01"
				on:input={onChange}
			/>
			<span>Rote X: {args3d.rotate_x}</span>
		</div>
		<div class="flex flex-col items-center">
			<input
				class="mt-4"
				type="range"
				bind:value={args3d.rotate_y}
				min="-2"
				max="2"
				step="0.001"
				on:input={onChange}
			/>
			<span>Rote Y: {args3d.rotate_y}</span>
		</div>
		<div class="flex flex-col items-center">
			<input
				class="mt-4"
				type="range"
				bind:value={args3d.rotate_z}
				min="-2"
				max="2"
				step="0.001"
				on:input={onChange}
			/>
			<span>Rote Z: {args3d.rotate_z}</span>http://localhost:5173/
		</div>
		<div class="flex flex-col items-center">
			<input
				class="mt-4"
				type="range"
				bind:value={args3d.translate_x}
				min="-2"
				max="2"
				step="0.001"
				on:input={onChange}
			/>
			<span>Transl X: {args3d.translate_x}</span>http://localhost:5173/
		</div>
		<div class="flex flex-col items-center">
			<input
				class="mt-4"
				type="range"
				bind:value={args3d.translate_y}
				min="-2"
				max="2"
				step="0.001"
				on:input={onChange}
			/>
			<span>Transl Y: {args3d.translate_y}</span>
		</div>
		<div class="flex flex-col items-center">
			<input
				class="mt-4"
				type="range"
				bind:value={args3d.translate_z}
				min="-2"
				max="2"
				step="0.01"
				on:input={onChange}
			/>
			<span>Transl Z: {args3d.translate_z}</span>
		</div>
	</div>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
