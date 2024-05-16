<script lang="ts">
	import { getTransform3dFeatureInfos, setTransform3dFeatureInfo } from '$lib/apis/api';
	import { getTrackAndFeatureNames } from '$lib/apis/audio-api';
	import { onMount } from 'svelte';
	import FeatureMap from '$lib/components/featureMapping/FeatureMap.svelte';

	let transform3DMapInfos: FeatureMapInfo[] = [];
	let trackNames: string[] = [];
	let featureNames: string[] = [];

	async function getTransform3DFeatureMapInfos() {
		const response = await getTransform3dFeatureInfos();
		const data = await response.json();
		return data;
	}

	async function getTrackAndFeatureNameList() {
		const response = await getTrackAndFeatureNames();
		const data = await response.json();
		return data;
	}

	onMount(async () => {
		transform3DMapInfos = await getTransform3DFeatureMapInfos();
		const trackAndFeatLists = await getTrackAndFeatureNameList();
		trackNames = trackAndFeatLists.trackNames;
		featureNames = trackAndFeatLists.featureNames;
	});
</script>

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
		{#each transform3DMapInfos as info (info.id)}
			<FeatureMap
				endpointFunction={setTransform3dFeatureInfo}
				featureMapInfo={info}
				trackOptions={trackNames}
				featureOptions={featureNames}
				showId={true}
				maxFactorValue={2}
				stepSize={0.001}
			></FeatureMap>
		{/each}
	</tbody>
</table>
