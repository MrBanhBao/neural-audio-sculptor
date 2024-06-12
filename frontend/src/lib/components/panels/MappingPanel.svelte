<script lang="ts">
	import { IconTransform, IconTimeline, IconRun } from '@tabler/icons-svelte';
	import { TabGroup, Tab } from '@skeletonlabs/skeleton';
	import { currentGenerator } from '$lib/stores/store';
	import TransformController from '../transformControllers/TransformController.svelte';
	import StlyeMappingController from '../featureMapping/StyleMappingController.svelte';
	import DiffusionMappingController from '../featureMapping/DiffusionMappingController.svelte';

	let tabSet: number = 0;
	let generator = $currentGenerator;

	currentGenerator.subscribe((value) => {
		generator = value;
	});
</script>

<div class="card flex-grow overflow-y-auto p-4">
	<TabGroup>
		<Tab bind:group={tabSet} name="tab1" value={0}>
			<div class="flex items-center">
				<IconTransform /><span class="ml-1 font-bold">Speed & Details</span>
			</div>
		</Tab>
		<Tab bind:group={tabSet} name="tab2" value={1}>
			<div class="flex items-center">
				<IconTransform /><span class="ml-1 font-bold">Transformation</span>
			</div>
		</Tab>
		<!-- Tab Panels --->
		<svelte:fragment slot="panel">
			<div class="overflow-auto">
				<div class:hidden={!(tabSet === 0)}>
					{#if generator === 'StyleGan'}
						<StlyeMappingController></StlyeMappingController>
					{:else if generator === 'StreamDiffusion'}
						<DiffusionMappingController></DiffusionMappingController>
					{:else}
						<p>Current Generator is not known.</p>
					{/if}
				</div>
				<div class:hidden={!(tabSet === 1)}>
					<TransformController></TransformController>
				</div>
			</div>
		</svelte:fragment>
	</TabGroup>
</div>
