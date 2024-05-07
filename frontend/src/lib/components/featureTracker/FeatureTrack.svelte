<script lang="ts">
	import { onMount } from 'svelte';
	import { createEventDispatcher } from 'svelte';
	import { IconSquareX } from '@tabler/icons-svelte';
	import WaveSurfer from 'wavesurfer.js';

	export let id: string = 'test';
	export let trackNames: string[] = ['main', 'vocals', 'drums', 'bass', 'piano', 'other'];
	export let featureNames: string[] = ['rme', 'energy', 'pitch'];
	export let audioData: number[] = [0];
	export let duration: number = 1;

	const dispatch = createEventDispatcher();

	export let selectedTrack: string;
	export let selectedFeature: string;
	let wavesurfer: any;

	$: {
		updateWavePlot(audioData);
	}

	onMount(() => {
		initWavePlot();
	});

	function initWavePlot() {
		wavesurfer = WaveSurfer.create({
			container: '#' + id + '-waveform',
			waveColor: 'violet',
			progressColor: 'purple',
			height: 60,
			interact: false,
			peaks: [audioData],
			duration: duration
		});

		wavesurfer.on('ready', () => {
			wavesurfer.setTime(0);
		});

		return () => {
			if (wavesurfer) {
				wavesurfer.destroy();
			}
		};
	}

	function updateWavePlot(audioData: number[]) {
		if (wavesurfer) {
			wavesurfer.destroy();

			wavesurfer = WaveSurfer.create({
				container: '#' + id + '-waveform',
				waveColor: 'violet',
				progressColor: 'purple',
				height: 60,
				interact: false,
				peaks: [audioData],
				duration: duration
			});

			wavesurfer.on('ready', () => {
				wavesurfer.setTime(0);
			});
		}
	}

	function handleDropDownChange() {
		const data = {
			id: id,
			selectedTrack: selectedTrack,
			selectedFeature: selectedFeature
		};
		dispatch('dropdownChange', data);
	}

	function handleDeleteClick() {
		dispatch('removeFeature', id);
	}
</script>

<tr class="h-2">
	<td class="centered"
		><button type="button" class="variant-filled btn-icon btn-sm" on:click={handleDeleteClick}
			><IconSquareX></IconSquareX></button
		></td
	>
	<td class="centered">
		<select class="select" bind:value={selectedTrack} on:change={handleDropDownChange}>
			{#each trackNames as trackName}
				<option value={trackName}>{trackName}</option>
			{/each}
		</select>
	</td>
	<td class="centered">
		<select class="select" bind:value={selectedFeature} on:change={handleDropDownChange}>
			{#each featureNames as featureName}
				<option value={featureName}>{featureName}</option>
			{/each}
		</select>
	</td>
	<td class="centered"><div id={id + '-waveform'}></div></td>
</tr>

<style>
	.centered {
		text-align: center;
		vertical-align: middle;
	}
</style>
