<script lang="ts">
	import { IconWaveSine, IconWaveSawTool, IconTimeline, IconRun } from '@tabler/icons-svelte';
	import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
	import AudioTracker from '$lib/components/audioTracker/AudioTracker.svelte';
	import FeatureTracker from '$lib/components/featureTracker/FeatureTracker.svelte';

	let tabSet: number = 0;
</script>

<div class="card flex-grow overflow-y-auto p-4">
	<TabGroup>
		<Tab bind:group={tabSet} name="tab1" value={0}>
			<div class="flex items-center">
				<IconWaveSawTool /><span class="ml-1">Audio</span>
			</div>
		</Tab>
		<Tab bind:group={tabSet} name="tab2" value={1}>
			<div class="flex items-center">
				<IconTimeline /><span class="ml-1">Features</span>
			</div>
		</Tab>
		<Tab bind:group={tabSet} name="tab3" value={2}>
			<div class="flex items-center">
				<IconRun /><span class="ml-1">Movement</span>
			</div>
		</Tab>
		<!-- Tab Panels --->
		<svelte:fragment slot="panel">
			<div class="overflow-auto">
				{#if tabSet === 0}
					<AudioTracker></AudioTracker>
				{:else if tabSet === 1}
					<FeatureTracker></FeatureTracker>
				{:else if tabSet === 2}
					Future Content
				{/if}
			</div>
		</svelte:fragment>
	</TabGroup>
</div>
