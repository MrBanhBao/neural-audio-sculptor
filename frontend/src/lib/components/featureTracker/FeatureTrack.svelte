<script lang="ts">
	import { onMount } from 'svelte';
	import { currentFrame, config } from '$lib/stores/store';
	import { createEventDispatcher } from 'svelte';
	import { IconSquareX } from '@tabler/icons-svelte';
	import { setCurrentFrame } from '$lib/apis/audio-api';
	import WaveSurfer from 'wavesurfer.js';

	export let id: string = 'test';
	export let height: number = 60;
	export let trackNames: string[] = ['main', 'vocals', 'drums', 'bass', 'piano', 'other'];
	export let featureNames: string[] = ['rme', 'energy', 'pitch'];
	export let audioData: number[] = [0];
	export let selectedTrack: string;
	export let selectedFeature: string;

	const dispatch = createEventDispatcher();
	const hopLength: number = $config.audio.hop_length;
	let wavesurfer: any;

	$: {
		updateWavePlot(audioData);
	}

	$: time = Math.ceil($currentFrame / hopLength);

	$: {
		updateTime(time);
	}

	function updateTime(time: number) {
		if (wavesurfer) {
			wavesurfer.setTime(time);
		}
	}

	onMount(() => {
		initWavePlot();
	});

	function initWavePlot() {
		wavesurfer = WaveSurfer.create({
			container: '#' + id + '-waveform',
			waveColor: 'violet',
			progressColor: 'purple',
			height: height,
			interact: true,
			peaks: [audioData],
			duration: audioData.length,
			sampleRate: 1,
			barAlign: 'bottom',
			dragToSeek: true
		});

		wavesurfer.on('ready', () => {
			wavesurfer.setTime(time);
		});

		wavesurfer.on('interaction', async (newTime) => {
			let frame = Math.ceil(newTime * hopLength);
			const response = await setCurrentFrame({ value: frame } as NumberValue);
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
				height: height,
				interact: true,
				peaks: [audioData],
				duration: audioData.length,
				sampleRate: 1,
				dragToSeek: true,
				barAlign: 'bottom'
			});

			wavesurfer.on('ready', () => {
				wavesurfer.setTime(time);
			});

			wavesurfer.on('interaction', async (newTime) => {
				let frame = Math.ceil(newTime * hopLength);
				const response = await setCurrentFrame({ value: frame } as NumberValue);
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
