<script lang="ts">
	import FeatureMap from './FeatureMap.svelte';
	import { onMount } from 'svelte';

	export let parameterName: string;
	export let getFeatureMapFunction: Function;
	export let setFeatureMapFunction: Function;
	export let columnNames: string[];
	export let trackNames: string[];
	export let featureNames: string[];
	export let maxFactorValue: number = 10;
	export let stepSize: number = 0.01;
	export let showId: boolean = false;

	let featureMapInfos: FeatureMapInfo[] = [];

	async function fetchFeatureMaps() {
		const response = await getFeatureMapFunction();
		const data = await response.json();
		return data;
	}
	onMount(async () => {
		featureMapInfos = await fetchFeatureMaps();
	});
</script>

<div class="card flex-grow p-4">
	<span>{parameterName}:</span>
	<table class="table table-hover">
		<thead>
			<tr>
				{#each columnNames as columnName}
					<th>{columnName}</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each featureMapInfos as info (info.id)}
				<FeatureMap
					endpointFunction={setFeatureMapFunction}
					featureMapInfo={info}
					trackOptions={trackNames}
					featureOptions={featureNames}
					{maxFactorValue}
					{stepSize}
					{showId}
				></FeatureMap>
			{/each}
		</tbody>
	</table>
</div>
