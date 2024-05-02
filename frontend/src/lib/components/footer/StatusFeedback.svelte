<script lang="ts">
	import { IconCheck, IconCircleX, IconLineDotted } from '@tabler/icons-svelte';
	import { statusFeedback } from '$lib/stores/store';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	function setTimer() {
		if ($statusFeedback.status == 'successfull' || $statusFeedback.status == 'failed') {
			setTimeout(() => {
				statusFeedback.set({ status: 'idle' } as StatusFeedback);
			}, 3000);
		}
	}

	$: setTimer($statusFeedback);
</script>

<div class="flex items-center">
	{#if $statusFeedback.status === 'idle'}
		<IconLineDotted class="text-surface-500"></IconLineDotted>
	{:else if $statusFeedback.status === 'pending'}
		<ProgressRadial class="mr-2" width="w-5" />:
		<span class="pt-0.5">{$statusFeedback.message}</span>
	{:else if $statusFeedback.status === 'failed'}
		<IconCircleX class="text-error-500"></IconCircleX>:
		<span class="pt-0.5">{$statusFeedback.message}</span>
	{:else if $statusFeedback.status === 'successfull'}
		<IconCheck class="text-success-500"></IconCheck>:
		<span class="pt-0.5">{$statusFeedback.message}</span>
	{/if}
</div>
