<script lang="ts">
	import { IconCheck, IconCircleX, IconLineDotted } from '@tabler/icons-svelte';
	import { AppBar } from '@skeletonlabs/skeleton';
	import { statusFeedback } from '$lib/stores/store';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import StatusFeedback from '$lib/components/footer/StatusFeedback.svelte';
</script>

<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead">
		<StatusFeedback></StatusFeedback>
	</svelte:fragment>
	(Foooooooter)
	<svelte:fragment slot="trail">(action)</svelte:fragment>
</AppBar>
