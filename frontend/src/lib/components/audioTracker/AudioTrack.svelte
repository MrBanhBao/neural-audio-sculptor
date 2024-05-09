<script lang="ts">
	import { currentFrame, statusFeedback } from '$lib/stores/store';
	import WaveSurfer from 'wavesurfer.js';
	import { onMount } from 'svelte';
	import { SlideToggle } from '@skeletonlabs/skeleton';
	import { getAudioFile, setSelectedAudioTrack, setCurrentFrame } from '$lib/apis/audio-api';

	export let name: string;
	export let height: number = 60;
	export let active: boolean = false;
	export let url: string = '';
	export let sampleRate: number = 44100;

	let wavesurfer: any;

	onMount(() => {
		initWavePlot();
	});

	$: time = Math.ceil($currentFrame / sampleRate);

	$: {
		updateTime(time);
	}

	$: {
		updateWavePlot(url);
	}

	function initWavePlot() {
		wavesurfer = WaveSurfer.create({
			container: '#' + name + '-waveform',
			waveColor: 'violet',
			progressColor: 'purple',
			interact: false,
			peaks: [[0]],
			height: height,
			duration: 1,
			dragToSeek: true
		});

		wavesurfer.on('ready', () => {
			wavesurfer.setTime(time);
		});

		return () => {
			if (wavesurfer) {
				wavesurfer.destroy();
			}
		};
	}

	function updateTime(time: number) {
		if (wavesurfer) {
			wavesurfer.setTime(time);
		}
	}

	async function updateWavePlot(url: string) {
		if (wavesurfer || url != '') {
			const response = await getAudioFile(url);
			url = response.url;

			wavesurfer.load(url);

			wavesurfer.toggleInteraction(true);

			wavesurfer.on('ready', () => {
				wavesurfer.setTime(time);
			});

			wavesurfer.on('interaction', async (newTime) => {
				let frame = Math.ceil(newTime * sampleRate);
				const response = await setCurrentFrame({ value: frame } as NumberValue);
			});
		}
	}

	async function handleChange(event) {
		const state = event.target.checked;
		const message = `Set audio track: ${name} to ${state}.`;
		statusFeedback.set({ status: 'pending', message: message });
		const selectedAudioTrack: SelectedAudioTrack = { name: name, active: state };

		const response = await setSelectedAudioTrack(selectedAudioTrack);
		if (response?.ok) {
			console.log(response);
			statusFeedback.set({
				status: 'successfull',
				message: message
			});
		} else {
			console.log('failed');
			statusFeedback.set({
				status: 'failed',
				message: message
			});
		}
	}
</script>

<tr class="h-2">
	<td class="centered"
		><SlideToggle name="slide" bind:checked={active} on:change={handleChange}></SlideToggle></td
	>
	<td class="centered">{name}</td>
	<td class="centered"><div id={name + '-waveform'}></div></td>
</tr>

<style>
	.centered {
		text-align: center;
		vertical-align: middle;
	}
</style>
