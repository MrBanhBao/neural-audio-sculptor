<script lang="ts">
	import { getTransform3dArgs, setTransform3dArgs } from '$lib/apis/api';
	import { onMount } from 'svelte';
	import TransformManualSlider from './TransformManualSlider.svelte';

	let args3d: Transform3DArgs;

	async function get3dArgs() {
		const reponse = await getTransform3dArgs();
		const data = await reponse.json();
		return data;
	}

	onMount(async () => {
		args3d = await get3dArgs();
	});

	async function onChange(e) {
		const response = await setTransform3dArgs(args3d);
		const data = await response.json();
		console.log(data);
	}
</script>

{#if args3d}
	<div class="card p-4">
		<div>Transformation:</div>
		<TransformManualSlider
			name="Translate X"
			min={-1}
			max={1}
			stepSize={0.01}
			bind:value={args3d.translate_x}
			on:inputChange={onChange}
		/>
		<TransformManualSlider
			name="Translate Y"
			min={-1}
			max={1}
			stepSize={0.01}
			bind:value={args3d.translate_y}
			on:inputChange={onChange}
		/>
		<TransformManualSlider
			name="Translate Z"
			min={-1}
			max={1}
			stepSize={0.01}
			bind:value={args3d.translate_z}
			on:inputChange={onChange}
		/>
		<TransformManualSlider
			name="Rotate X"
			min={-2}
			max={2}
			stepSize={0.01}
			bind:value={args3d.rotate_x}
			on:inputChange={onChange}
		/>
		<TransformManualSlider
			name="Rotate Y"
			min={-2}
			max={2}
			stepSize={0.01}
			bind:value={args3d.rotate_y}
			on:inputChange={onChange}
		/>
		<TransformManualSlider
			name="Rotate Z"
			min={-2}
			max={2}
			stepSize={0.01}
			bind:value={args3d.rotate_z}
			on:inputChange={onChange}
		/>
	</div>
{:else}
	<p>...waiting</p>
{/if}
