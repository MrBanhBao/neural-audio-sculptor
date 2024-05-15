<script lang="ts">
	import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';
	import {
		getTransformationMode,
		setTransformationMode,
		getPaddingModes,
		setPaddingMode
	} from '$lib/apis/api';

	import TransformMappingController from './mapping/TransformMappingController.svelte';
	import TransformManualController from './manual/TransformManualController.svelte';
	import { onMount } from 'svelte';

	let transformationMode: string = 'mapping';
	let paddingModes: string[] = [];
	let paddingMode: string = 'reflection';

	onMount(async () => {
		transformationMode = await fetchTransformationMode();
		paddingModes = await fetchPaddingModes();
	});

	async function fetchTransformationMode() {
		const response = await getTransformationMode();
		const data = await response.json();
		return data.value;
	}

	async function fetchPaddingModes() {
		const response = await getPaddingModes();
		const data = await response.json();
		return data;
	}

	async function updateTransformationMode(transformationMode: string) {
		const response = await setTransformationMode({ value: transformationMode } as StringValue);
		console.log(response);
	}

	async function updatePaddingMode() {
		const response = await setPaddingMode({ value: paddingMode });
		console.log(response);
	}
	$: updateTransformationMode(transformationMode);
</script>

<div class="card flex flex-col p-4">
	<div class="flex flex-row items-center">
		<div class="mb-2 mt-2 pr-8">
			<label>Transformation mode:</label>
			<RadioGroup
				class="w-[215px] rounded-full"
				hover="hover:variant-soft-primary"
				active="variant-filled-primary"
			>
				<RadioItem bind:group={transformationMode} name="justify" value={'mapping'}
					>Mapping</RadioItem
				>
				<RadioItem bind:group={transformationMode} name="justify" value={'manual'}>Manual</RadioItem
				>
			</RadioGroup>
		</div>
		<div class="mb-2 mt-2">
			<label>Padding mode:</label>
			<select class="select mt-1" bind:value={paddingMode} on:change={updatePaddingMode}>
				{#each paddingModes as paddingOptions}
					<option value={paddingOptions}>{paddingOptions}</option>
				{/each}
			</select>
		</div>
	</div>

	<div class:hidden={!(transformationMode === 'mapping')}>
		<TransformMappingController></TransformMappingController>
	</div>

	<div class:hidden={!(transformationMode === 'manual')}>
		<TransformManualController {paddingMode}></TransformManualController>
	</div>
</div>

<style>
	.hidden {
		visibility: hidden;
	}
</style>
