<script lang="ts">
	import { setSpeedFeatureInfo } from '$lib/apis/stylegan-api';

	export let featureMapInfo: FeatureMapInfo;
	export let trackOptions: string[];
	export let featureOptions: string[];
	export let showId: boolean = false;
	export const maxFactorValue: number = 5;

	let selectedTrack: string = featureMapInfo.track_name;
	let selectedFeature: string = featureMapInfo.feature_name;

	async function onchange() {
		console.log(featureMapInfo);
		const response = await setSpeedFeatureInfo(featureMapInfo);
		console.log(await response.json());
	}
</script>

<div class="flex flex-row justify-center">
	<div>
		<input type="checkbox" bind:checked={featureMapInfo.active} on:change={onchange} />
	</div>
	<div>
		<select class="select" bind:value={featureMapInfo.track_name} on:change={onchange}>
			{#each trackOptions as trackOption}
				<option value={trackOption}>{trackOption}</option>
			{/each}
		</select>
	</div>
	<div>
		<select class="select" bind:value={featureMapInfo.feature_name} on:change={onchange}>
			{#each featureOptions as featureOption}
				<option value={featureOption}>{featureOption}</option>
			{/each}
		</select>
	</div>
	<div class="flex flex-col items-center">
		<input
			class="mt-4"
			type="range"
			bind:value={featureMapInfo.factor}
			min="0"
			max={maxFactorValue}
			step="0.1"
			on:input={onchange}
		/>
		<span>{featureMapInfo.factor}</span>
	</div>
</div>
