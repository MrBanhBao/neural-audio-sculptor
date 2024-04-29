<script lang="ts">
	import '../app.postcss';
	import { AppShell } from '@skeletonlabs/skeleton';
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import { onMount } from 'svelte';
	import yaml from 'js-yaml';
	import { config } from '$lib/stores/store';

	onMount(async () => {
		const response = await fetch('config.yaml');
		const text = await response.text();
		const configObj = yaml.load(text) as Config;
		config.set(configObj);
	});
</script>

<AppShell>
	<svelte:fragment slot="header"><Header></Header></svelte:fragment>
	<!-- (sidebarLeft) -->
	<!-- (sidebarRight) -->
	<!-- (pageHeader) -->
	<!-- Router Slot -->
	<slot />
	<!-- ---- / ---- -->
	<!-- (pageFooter) -->
	<svelte:fragment slot="footer"><Footer></Footer></svelte:fragment>
</AppShell>
