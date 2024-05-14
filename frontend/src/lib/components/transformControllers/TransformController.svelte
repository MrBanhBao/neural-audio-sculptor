<script lang="ts">
	import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';
	import { getTransformationMode, setTransformationMode } from '$lib/apis/api';

	import TransformMappingController from './mapping/TransformMappingController.svelte';
	import TransformManualController from './manual/TransformManualController.svelte';
	import { onMount } from 'svelte';

	let mode: string = 'mapping';

	onMount(async () => {
		mode = await fetchTransformatonMode();
		// mode = await getTransformationMode();
	});

	async function fetchTransformatonMode() {
		const response = await getTransformationMode();
		const data = await response.json();
		return data.value;
	}

	async function updateMode(mode: string) {
		const reponse = await setTransformationMode({ value: mode } as StringValue);
		console.log(reponse);
	}

	$: updateMode(mode);
</script>

<div class="card flex flex-col p-4">
	<span>Transformation:</span>
	<RadioGroup
		class="mb-2 mt-2 w-[215px] rounded-full"
		hover="hover:variant-soft-primary"
		active="variant-filled-primary"
	>
		<RadioItem bind:group={mode} name="justify" value={'mapping'}>Mapping</RadioItem>
		<RadioItem bind:group={mode} name="justify" value={'manual'}>Manual</RadioItem>
	</RadioGroup>

	<div class:hidden={!(mode === 'mapping')}>
		<TransformMappingController></TransformMappingController>
	</div>

	<div class:hidden={!(mode === 'manual')}>
		<TransformManualController></TransformManualController>
	</div>
</div>

<style>
	.hidden {
		visibility: hidden;
	}
</style>
