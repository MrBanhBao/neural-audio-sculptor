<script lang="ts">
	export let showModal: boolean;
	export let title: string = 'Title';
	let dialog: HTMLDialogElement;

	$: if (dialog && showModal) dialog.showModal();
</script>

<dialog
	class="card h-4/6 w-7/12 p-4"
	bind:this={dialog}
	on:close={() => (showModal = false)}
	on:click|self={() => dialog.close()}
>
	<div class="text-token flex h-full flex-col">
		<header class="card-header">
			<p class="text-3xl">{title}</p>
		</header>
		<section class="overflow-y-auto p-4">
			<slot />
		</section>
		<footer class="card-footer pt-4">
			<button class="variant-filled-secondary btn btn-sm" autofocus on:click={() => dialog.close()}
				>close</button
			>
		</footer>
	</div>
</dialog>

<style>
	section {
		flex: 1;
	}
</style>
