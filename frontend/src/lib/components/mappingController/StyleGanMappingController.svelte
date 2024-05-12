<script lang="ts">
	import {
		getWsFeatureInfos,
		getSpeedFeatureInfos,
		setSpeedFeatureInfo,
		setWsFeatureInfo
	} from '$lib/apis/stylegan-api';
	import { getTrackAndFeatureNames } from '$lib/apis/audio-api';
	import { onMount } from 'svelte';
	import FeatureMap from './FeatureMap.svelte';

	let speedFeatureMapInfos: FeatureMapInfo[] = [];
	let wsFeatureMapInfos: FeatureMapInfo[] = [];
	let trackNames: string[] = [];
	let featureNames: string[] = [];

	async function getSpeedFeatureMapInfos() {
		const response = await getSpeedFeatureInfos();
		const data = await response.json();
		return data;
	}

	async function getWsFeatureMapInfos() {
		const response = await getWsFeatureInfos();
		const data = await response.json();
		return data;
	}

	async function getTrackAndFeatureNameList() {
		const response = await getTrackAndFeatureNames();
		const data = await response.json();
		return data;
	}

	onMount(async () => {
		speedFeatureMapInfos = await getSpeedFeatureMapInfos();
		wsFeatureMapInfos = await getWsFeatureMapInfos();
		const trackAndFeatLists = await getTrackAndFeatureNameList();
		trackNames = trackAndFeatLists.trackNames;
		featureNames = trackAndFeatLists.featureNames;
		console.log(trackNames);
		console.log(featureNames);
	});
</script>

<div class="card p-4">
	<span>Speed:</span>
	<table class="table table-hover">
		<thead>
			<tr>
				<th>Active</th>
				<th>Track</th>
				<th>Feature</th>
				<th>Factor</th>
			</tr>
		</thead>
		<tbody>
			{#each speedFeatureMapInfos as info (info.id)}
				<FeatureMap
					endpointFunction={setSpeedFeatureInfo}
					featureMapInfo={info}
					trackOptions={trackNames}
					featureOptions={featureNames}
				></FeatureMap>
			{/each}
		</tbody>
	</table>
</div>

<div class="card p-4">
	<span>WS:</span>
	<table class="table table-hover">
		<thead>
			<tr>
				<th>Name</th>
				<th>Active</th>
				<th>Track</th>
				<th>Feature</th>
				<th>Factor</th>
			</tr>
		</thead>
		<tbody>
			{#each wsFeatureMapInfos as info (info.id)}
				<FeatureMap
					endpointFunction={setWsFeatureInfo}
					featureMapInfo={info}
					trackOptions={trackNames}
					featureOptions={featureNames}
					showId={true}
					maxFactorValue={10}
				></FeatureMap>
			{/each}
		</tbody>
	</table>
</div>
