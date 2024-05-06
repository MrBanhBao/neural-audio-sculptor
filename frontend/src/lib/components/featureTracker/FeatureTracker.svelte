<script lang="ts">
	import { audioMetaData, currentFrame, isPlaying, config } from '$lib/stores/store';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { getFeaturesFile } from '$lib/apis/audio-api';

	const MAX_RETRIES: number = 50;
	let retryCount: number = 0;
	let featureData = null;
	let retryTimeout = null;
	let loading = false;

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
				console.log(featureData);
				if (retryTimeout) {
					clearTimeout(retryTimeout);
				}
			} catch (err) {
				if (retryCount < MAX_RETRIES) {
					retryCount++;
					retryTimeout = setTimeout(fetchAudioFeatures, 2500);
				} else {
					clearTimeout(retryTimeout);
				}
			}
		}
	}

	audioMetaData.subscribe((audioMetaData) => {
		retryCount = 0;
		featureData = null;
		fetchAudioFeatures();
	});
</script>

<div class="card p-4">
	{#if loading}
		<ProgressRadial />
	{:else if featureData != null}
		yes
	{:else}
		Waiting for loading audio data.
	{/if}
</div>
