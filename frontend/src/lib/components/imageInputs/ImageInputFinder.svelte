<script lang="ts">
	import { setImageInputDirectory } from '$lib/apis/stream-diffusion-api';

	async function test1() {
		let path: string = '/home/hao/Pictures/stream_diffusion/flowers';
		const response = await setImageInputDirectory({ value: path } as StringValue);
	}

	async function test2() {
		let path: string = '/home/hao/Pictures/stream_diffusion/nature_pattern';
		const response = await setImageInputDirectory({ value: path } as StringValue);
	}
</script>

<div>
	<button
		type="button"
		class="btn-m variant-filled-primary btn btn-md mr-4 rounded-full"
		on:click={test1}
	>
		Flower
	</button>

	<button
		type="button"
		class="btn-m variant-filled-primary btn btn-md mr-4 rounded-full"
		on:click={test2}
	>
		Nature
	</button>
</div>
