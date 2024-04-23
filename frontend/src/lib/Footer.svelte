<script lang="ts">
	import { AppBar } from '@skeletonlabs/skeleton';
</script>

<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead">(icon)</svelte:fragment>
	(Foooooooter)
	<svelte:fragment slot="trail">(action)</svelte:fragment>
</AppBar>
