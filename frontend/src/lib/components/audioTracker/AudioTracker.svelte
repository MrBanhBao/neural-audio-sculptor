<script lang="ts">
	import { onMount } from 'svelte';
	import { audioMetaData, config } from '$lib/stores/store';
	import AudioTrack from './AudioTrack.svelte';

	const trackNames = ['main', 'vocals', 'drums', 'bass', 'piano', 'other'];
	const extension = '.wav';
	let tracks: WaveSurferTrack[];

	function createWaveSurferTrackArray(audioMetaData) {
		console.log('load meta trackers');
		if (audioMetaData.file_name != undefined) {
			tracks = trackNames.map((trackName) => createWaveSurferTrackInfo(trackName));
			console.log(tracks);
		} else {
			// empty tracks
			tracks = trackNames.map((trackName) => {
				return { name: trackName, active: false, url: '' };
			});
		}
	}

	function createWaveSurferTrackInfo(trackName: string): WaveSurferTrack {
		if (trackName === 'main') {
			const url = $audioMetaData.path;
			return { name: trackName, active: true, url: url };
		} else {
			const cache_dir = $config.backend.cache_dir;
			const dirName = $audioMetaData?.file_name?.replace(/\.[^/.]+$/, '');
			const url = `${cache_dir}/${dirName}/${trackName + extension}`;
			return { name: trackName, active: false, url: url };
		}
	}

	$: {
		createWaveSurferTrackArray($audioMetaData);
	}
</script>

<div class="card min-w-80 flex-grow">
	<div class="table-container">
		<table class="table table-interactive">
			<thead>
				<tr>
					<th class="table-cell-fit">Active</th>
					<th class="table-cell-fit">Name</th>
					<th class="">Waveplot</th>
				</tr>
			</thead>
			<tbody>
				{#each tracks as track (track)}
					<AudioTrack
						name={track.name}
						active={track.active}
						url={track.url}
						sampleRate={$audioMetaData.sample_rate}
					/>
				{/each}
			</tbody>
		</table>
	</div>
</div>
