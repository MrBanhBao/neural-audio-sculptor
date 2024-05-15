<script lang="ts">
	import { SlideToggle } from '@skeletonlabs/skeleton';

	export let endpointFunction: Function;
	export let featureMapInfo: FeatureMapInfo;
	export let trackOptions: string[];
	export let featureOptions: string[];
	export let showId: boolean = false;
	export let maxFactorValue: number = 5;
	export let stepSize: number = 0.1;

	let selectedTrack: string = featureMapInfo.track_name;
	let selectedFeature: string = featureMapInfo.feature_name;

	async function onchange() {
		const response = await endpointFunction(featureMapInfo);
	}
</script>

<tr>
	{#if showId}
		<td class="centered">{featureMapInfo.id}</td>
	{/if}
	<td class="centered">
		<SlideToggle name="slide" bind:checked={featureMapInfo.active} on:change={onchange}
		></SlideToggle>
	</td>
	<td class="centered">
		<select class="select" bind:value={featureMapInfo.track_name} on:change={onchange}>
			{#each trackOptions as trackOption}
				<option value={trackOption}>{trackOption}</option>
			{/each}
		</select>
	</td>
	<td class="centered">
		<select class="select" bind:value={featureMapInfo.feature_name} on:change={onchange}>
			{#each featureOptions as featureOption}
				<option value={featureOption}>{featureOption}</option>
			{/each}
		</select>
	</td>
	<td class="centered">
		<div class="flex flex-col items-center">
			<input
				class="mt-4"
				type="range"
				bind:value={featureMapInfo.factor}
				min="0"
				max={maxFactorValue}
				step={stepSize}
				on:input={onchange}
			/>
			<span>{featureMapInfo.factor}</span>
		</div>
	</td>
</tr>

<style>
	.centered {
		text-align: center;
		vertical-align: middle;
	}
</style>
