<script lang="ts">
	import { currentGenerator } from '$lib/stores/store';
	import { getGeneratorOptions, getCurrentGenerator, setCurrentGenerator } from '$lib/apis/api';
	import { onMount } from 'svelte';
	import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';

	let generatorOptions: string[] = [];
	let selectedGenerator = $currentGenerator;

	async function fetchGeneratorOptions() {
		const response = await getGeneratorOptions();
		const data = await response.json();
		return data;
	}

	async function fetchCurrentGenerator() {
		const response = await getCurrentGenerator();
		const data = await response.json();
		return data.value;
	}

	async function updateCurrentGenerator(generator: string) {
		const response = await setCurrentGenerator({ value: generator });
		if (response.ok) {
			currentGenerator.set(generator);
		}
		console.log(response);
	}

	$: updateCurrentGenerator(selectedGenerator);

	let value: number = 0;

	onMount(async () => {
		generatorOptions = await fetchGeneratorOptions();
		selectedGenerator = await fetchCurrentGenerator();
		currentGenerator.set(selectedGenerator);
	});
</script>

<RadioGroup>
	<RadioItem bind:group={selectedGenerator} name="justify" value={'StyleGan'}>StyleGan</RadioItem>
	<RadioItem bind:group={selectedGenerator} name="justify" value={'StreamDiffusion'}
		>StreamDiffusion</RadioItem
	>
</RadioGroup>
