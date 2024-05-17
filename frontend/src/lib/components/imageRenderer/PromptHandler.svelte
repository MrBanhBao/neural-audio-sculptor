<script lang="ts">
	import { getPrompt, setPrompt } from '$lib/apis/stream-diffusion-api';
	import { onMount } from 'svelte';

	let currentPrompt: string = '';
	let placeholder: string = 'Please enter a prompt.';

	async function fetchPrompt() {
		const response = await getPrompt();
		const data = await response.json();

		return data;
	}

	onMount(async () => {
		currentPrompt = await fetchPrompt();
		console.log(currentPrompt);
	});

	async function applyPrompt() {
		const response = setPrompt({ value: currentPrompt } as StringValue);
		console.log(response);
	}

	async function handleKeydown(event) {
		if (event.key === 'Enter') {
			event.preventDefault();
			applyPrompt();
		}
	}
</script>

<label class="label">
	<span>Prompt:</span>
	<textarea
		class="textarea"
		rows="4"
		{placeholder}
		on:keydown={handleKeydown}
		bind:value={currentPrompt}
	/>
</label>
<button class="variant-filled btn btn-sm" on:click={applyPrompt}>Apply</button>
