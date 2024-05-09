<script lang="ts">
	import { IconSquareX, IconSquarePlus } from '@tabler/icons-svelte';
	import { audioMetaData, currentFrame, isPlaying, config } from '$lib/stores/store';
	import { v4 as uuidv4 } from 'uuid';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { getFeaturesFile } from '$lib/apis/audio-api';
	import FeatureTrack from '$lib/components/featureTracker/FeatureTrack.svelte';

	const MAX_RETRIES: number = 50;
	const defaultTrackName = 'main';
	const defaultFeatureName = 'rms';

	let retryCount: number = 0;
	let featureData: Object | null = null;
	let retryTimeout: NodeJS.Timeout | null = null;
	let loading = false;

	let trackNames: string[];
	let featureNames: string[];

	let featureTrackItems: FeatureTrackInfo[] | null = null;

	audioMetaData.subscribe(() => {
		retryCount = 0;
		featureData = null;
		fetchAudioFeatures();
	});

	async function fetchAudioFeatures() {
		if ($audioMetaData.file_name != undefined) {
			try {
				loading = true;
				console.log('Try number: ', retryCount);
				const cache_dir = $config.backend.cache_dir;
				const dirName = $audioMetaData?.file_name?.replace(/\.[^/.]+$/, '');
				const path = `${cache_dir}/${dirName}/features.json`;

				const response = await getFeaturesFile(path);
				if (!response.ok) {
					throw new Error('Failed to fetch data');
				}
				featureData = await response.json();
				loading = false;
				getTrackAndFeatureNames(featureData);
				initFeatureTrackItems();
				updateItems();
				// Todo: create initial featureTrackItems
				if (retryTimeout) {
					clearTimeout(retryTimeout);
				}
			} catch (err) {
				if (retryCount < MAX_RETRIES) {
					retryCount++;
					retryTimeout = setTimeout(fetchAudioFeatures, 2500);
				} else {
					if (retryTimeout) {
						clearTimeout(retryTimeout);
					}
				}
			}
		}
	}

	function getTrackAndFeatureNames(featureData: Object) {
		trackNames = Object.keys(featureData);
		featureNames = Object.keys(featureData[trackNames[0]]);
	}

	function initFeatureTrackItems() {
		console.log(featureTrackItems);
		if (featureTrackItems == null) {
			console.log('kikikiki');
			const data1 = {
				id: 'i' + uuidv4(),
				selectedTrack: 'main',
				selectedFeature: 'rms'
			} as FeatureTrackInfo;

			const data2 = {
				id: 'i' + uuidv4(),
				selectedTrack: 'vocals',
				selectedFeature: 'pitch'
			} as FeatureTrackInfo;

			const data3 = {
				id: 'i' + uuidv4(),
				selectedTrack: 'drums',
				selectedFeature: 'energy'
			} as FeatureTrackInfo;

			const data4 = {
				id: 'i' + uuidv4(),
				selectedTrack: 'bass',
				selectedFeature: 'tempo'
			} as FeatureTrackInfo;

			const data5 = {
				id: 'i' + uuidv4(),
				selectedTrack: 'piano',
				selectedFeature: 'pitch'
			} as FeatureTrackInfo;

			const data6 = {
				id: 'i' + uuidv4(),
				selectedTrack: 'other',
				selectedFeature: 'rms'
			} as FeatureTrackInfo;
			featureTrackItems = [data1, data2, data3, data4, data5, data6];
		}
	}

	function updateItems() {
		if (featureTrackItems != null) {
			const updatedItems = featureTrackItems.map((item) => {
				const selectedTrack = item.selectedTrack;
				const selectedFeature = item.selectedFeature;
				item.audioData = featureData[selectedTrack][selectedFeature];

				return item;
			});
			console.log('dasds');
			featureTrackItems = updatedItems;
		}
	}

	function addItem() {
		const newItem = {
			id: 'x' + uuidv4(),
			selectedTrack: defaultTrackName,
			selectedFeature: defaultFeatureName,
			audioData: featureData[defaultTrackName][defaultFeatureName]
		} as FeatureTrackInfo; // Todo: change
		featureTrackItems = [...featureTrackItems, newItem];
	}

	function removeItem(e: Event) {
		const deleteId = e.detail;
		featureTrackItems = featureTrackItems.filter((item) => item.id !== deleteId);
	}

	function updateItem(e: Event) {
		const info = e.detail;
		const index: number = featureTrackItems.findIndex((item) => item.id == info.id);
		let el: FeatureTrackInfo = featureTrackItems[index];
		el.selectedTrack = info.selectedTrack;
		el.selectedFeature = info.selectedFeature;
		el.audioData = featureData[info.selectedTrack][info.selectedFeature];

		featureTrackItems[index] = el;
	}

	// Todo: create TrackNames array, with initial values. {id: , data}
	// this is going to be used to loop the rows
	// on change will add data props of featureData
</script>

{#if loading}
	<ProgressRadial />
{:else if featureData != null}
	<div class="table-container max-h-full">
		<table class="table table-interactive table-auto">
			<thead>
				<tr>
					<th class="table-cell-fit"
						><button
							type="button"
							class="btn-s variant-filled-primary btn rounded-full"
							on:click={addItem}
						>
							<span><IconSquarePlus></IconSquarePlus></span>
						</button></th
					>
					<th class="w-40">Track</th>
					<th class="w-40">Feature</th>
					<th class="">Featureplot</th>
				</tr>
			</thead>
			<tbody>
				{#each featureTrackItems as item (item.id)}
					<FeatureTrack
						id={item.id}
						{trackNames}
						{featureNames}
						selectedTrack={item.selectedTrack}
						selectedFeature={item.selectedFeature}
						audioData={item.audioData}
						on:removeFeature={removeItem}
						on:dropdownChange={updateItem}
					></FeatureTrack>
				{/each}
			</tbody>
		</table>
	</div>
{:else}
	Waiting for loading audio data.
{/if}
