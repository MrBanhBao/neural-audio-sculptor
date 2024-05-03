<script lang="ts">
	import { currentFrame } from '$lib/stores/store';
	import WaveSurfer from 'wavesurfer.js';
	import { onMount } from 'svelte';
	import { SlideToggle } from '@skeletonlabs/skeleton';
	import { getAudioFile } from '$lib/apis/audio-api';

	export let name: string;
	export let active: boolean = false;
	export let url: string = '';
	export let sampleRate: number = 44100;

	let wavesurfer: any;

	onMount(() => {
		initWavePlot();
	});

	function initWavePlot() {
		wavesurfer = WaveSurfer.create({
			container: '#' + name + '-waveform',
			waveColor: 'violet',
			progressColor: 'purple',
			interact: false,
			peaks: [[0]],
			duration: 1
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

	$: time = Math.ceil($currentFrame / sampleRate);

	$: {
		updateTime(time);
	}

	$: {
		updateWavePlot(url);
	}

	$: console.log(url);

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

			wavesurfer.on('ready', () => {
				wavesurfer.setTime(0);
			});
		}
	}
</script>

<tr class="h-2">
	<td class="centered"><SlideToggle name="slide" bind:checked={active}></SlideToggle></td>
	<td class="centered">{name}</td>
	<td class="centered"><div id={name + '-waveform'}></div></td>
</tr>

<style>
	.centered {
		text-align: center;
		vertical-align: middle;
	}
</style>
