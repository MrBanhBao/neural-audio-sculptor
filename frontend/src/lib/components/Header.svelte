<script lang="ts">
	import { AppBar } from '@skeletonlabs/skeleton';
	import { LightSwitch } from '@skeletonlabs/skeleton';
</script>

<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead">
		<!-- (icon) -->
	</svelte:fragment>
	<p class="text-xl font-bold">Neural Audio Sculptor</p>
	<svelte:fragment slot="trail"><LightSwitch></LightSwitch></svelte:fragment>
</AppBar>
