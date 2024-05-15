<script lang="ts">
	import {
		getWsFeatureInfos,
		getSpeedFeatureInfos,
		setSpeedFeatureInfo,
		setWsFeatureInfo
	} from '$lib/apis/stylegan-api';
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
		maxFactorValue={10}
		stepSize={0.01}
		showId={false}
	></FeatureMapper>

	<FeatureMapper
		parameterName={'WS'}
		getFeatureMapFunction={getWsFeatureInfos}
		setFeatureMapFunction={setWsFeatureInfo}
		columnNames={['Name', 'Active', 'Track', 'Feature', 'Factor']}
		{trackNames}
		{featureNames}
		maxFactorValue={10}
		stepSize={0.01}
		showId={true}
	></FeatureMapper>
</div>
