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
{:then number}
	<div class="card p-4">
		<div class="flex flex-col items-center">
			<input
				class="mt-4"
				type="range"
				bind:value={args3d.rotate_x}
				min="0"
				max="10"
				step="0.01"
				on:input={onChange}
			/>
			<span>{args3d.rotate_x}</span>
		</div>
	</div>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
