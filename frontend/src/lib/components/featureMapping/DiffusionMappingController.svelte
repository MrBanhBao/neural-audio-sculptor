<script lang="ts">
	import {
		getSpeedFeatureInfos,
		setSpeedFeatureInfo,
		getLatentFeatureInfos,
		setLatentFeatureInfo
	} from '$lib/apis/stream-diffusion-api';

	import { getTrackAndFeatureNames } from '$lib/apis/audio-api';
	import { onMount } from 'svelte';
	import FeatureMapper from './FeatureMapper.svelte';
	let trackNames: string[] = [];
	let featureNames: string[] = [];

	async function getTrackAndFeatureNameList() {
		const response = await getTrackAndFeatureNames();
		const data = await response.json();
		return data;
	}

	onMount(async () => {
		const trackAndFeatLists = await getTrackAndFeatureNameList();
		trackNames = trackAndFeatLists.trackNames;
		featureNames = trackAndFeatLists.featureNames;
	});
</script>

<div class="flex justify-evenly">
	<FeatureMapper
		parameterName={'Speed'}
		getFeatureMapFunction={getSpeedFeatureInfos}
		setFeatureMapFunction={setSpeedFeatureInfo}
		columnNames={['Active', 'Track', 'Feature', 'Factor']}
		{trackNames}
		{featureNames}
		maxFactorValue={100}
		stepSize={1}
		showId={false}
	></FeatureMapper>

	<FeatureMapper
		parameterName={'Latent'}
		getFeatureMapFunction={getLatentFeatureInfos}
		setFeatureMapFunction={setLatentFeatureInfo}
		columnNames={['Name', 'Active', 'Track', 'Feature', 'Factor']}
		{trackNames}
		{featureNames}
		maxFactorValue={5}
		stepSize={0.001}
		showId={true}
	></FeatureMapper>
</div>
