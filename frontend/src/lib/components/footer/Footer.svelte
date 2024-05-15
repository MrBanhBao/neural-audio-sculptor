<script lang="ts">
	import { AppBar } from '@skeletonlabs/skeleton';
	import StatusFeedback from '$lib/components/footer/StatusFeedback.svelte';
	import GeneratorChange from './GeneratorChange.svelte';
</script>

<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead">
		<StatusFeedback></StatusFeedback>
	</svelte:fragment>
	(Foooooooter)
	<svelte:fragment slot="trail"><GeneratorChange/></svelte:fragment>
</AppBar>
