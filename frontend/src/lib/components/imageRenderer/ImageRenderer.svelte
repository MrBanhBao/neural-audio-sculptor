<script lang="ts">
	import { IconMultiplier1x, IconMultiplier2x, IconWindowMaximize } from '@tabler/icons-svelte';
</script>

<div class="card p-4">
	<span> Information </span>
	<div class="mb-2">
		<img width="256" src="https://fakeimg.pl/512x512" alt="generated for music viz." />
	</div>
	<div>
		<button type="button" class="variant-filled btn-icon"><IconMultiplier1x /></button>
		<button type="button" class="variant-filled btn-icon"><IconMultiplier2x /></button>
		<button type="button" class="variant-filled btn-icon"><IconWindowMaximize /></button>
	</div>
</div>
