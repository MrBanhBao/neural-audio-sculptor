<script lang="ts">
	import { getTransformManual3dArgs, setTransformManual3dArgs } from '$lib/apis/api';
	import { onMount } from 'svelte';
	import TransformManualSlider from './TransformManualSlider.svelte';

	export let paddingMode: string;
	let args3d: Transform3DArgs;

	async function get3dArgs() {
		const reponse = await getTransformManual3dArgs();
		const data = await reponse.json();
		return data;
	}

	onMount(async () => {
		args3d = await get3dArgs();
	});

	async function onChange(e) {
		args3d.padding_mode = paddingMode;
		const response = await setTransformManual3dArgs(args3d);
		const data = await response.json();
		console.log(data);
	}
</script>

{#if args3d}
	<table class="table table-hover">
		<thead>
			<tr>
				<th>Name</th>
				<th>Value</th>
			</tr>
		</thead>
		<tbody>
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
		</tbody>
	</table>
{/if}
