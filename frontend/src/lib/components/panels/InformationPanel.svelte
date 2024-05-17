<script lang="ts">
	import { IconWaveSawTool, IconTimeline, IconRun } from '@tabler/icons-svelte';
	import { TabGroup, Tab } from '@skeletonlabs/skeleton';
	import AudioTracker from '$lib/components/audioTracker/AudioTracker.svelte';
	import FeatureTracker from '$lib/components/featureTracker/FeatureTracker.svelte';
	import PoseEstimationPanel from '../poseEstimation/PoseEstimationPanel.svelte';
	let tabSet: number = 0;
</script>

<div class="card flex-grow overflow-y-auto p-4">
	<TabGroup>
		<Tab bind:group={tabSet} name="tab1" value={0}>
			<div class="flex items-center">
				<IconWaveSawTool /><span class="ml-1 font-bold">Audio</span>
			</div>
		</Tab>
		<Tab bind:group={tabSet} name="tab2" value={1}>
			<div class="flex items-center">
				<IconTimeline /><span class="ml-1 font-bold">Features</span>
			</div>
		</Tab>
		<Tab bind:group={tabSet} name="tab3" value={2}>
			<div class="flex items-center">
				<IconRun /><span class="ml-1 font-bold">Movement</span>
			</div>
		</Tab>
		<!-- Tab Panels --->
		<svelte:fragment slot="panel">
			<div class="overflow-auto">
				<div class:hidden={!(tabSet === 0)}>
					<AudioTracker></AudioTracker>
				</div>
				<div class:hidden={!(tabSet === 1)}>
					<FeatureTracker></FeatureTracker>
				</div>
				<div class:hidden={!(tabSet === 2)}>
					<PoseEstimationPanel></PoseEstimationPanel>
				</div>
			</div>
		</svelte:fragment>
	</TabGroup>
</div>

<style>
	.hidden {
		visibility: hidden;
	}
</style>
