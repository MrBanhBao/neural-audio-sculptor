<script lang="ts">
	import { IconMultiplier1x, IconMultiplier2x, IconWindowMaximize } from '@tabler/icons-svelte';

	let imgSrc = 'https://fakeimg.pl/512x512';
	const imgs = [
		'https://fastly.picsum.photos/id/559/200/300.jpg?hmac=lNV_-XwwjsYJn2cX4Pq7EFx4GA57ekwh_ZoR1dc09H0',
		'https://fastly.picsum.photos/id/360/200/200.jpg?hmac=uO4zEvFVrZ6_pBuLc0DuGdgwe5g3FiJCd7bGsr2lhCo',
		'https://fastly.picsum.photos/id/727/200/200.jpg?hmac=3t3XFTDKvF4DdvtTj-t8IMm5uwdlyzdECQmn87m3qk0'
	];
	let winRef: Window | null = null;

	function openImage() {
		const features = 'width=512,height=512';
		winRef = window.open('Test', '_blank');

		const content = `
            <style>
                body {
                    background-color: black;
                    margin: 0;
                    padding: 0;
                }

                .image-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
            </style>
            <div class="image-container">
                <img id="image" src=${imgSrc} alt="Image" style="width: auto; height: 100%;">
            </div>`;
		winRef?.document.write(content);
	}

	function test() {
		const randomIndex = Math.floor(Math.random() * imgs.length);
		imgSrc = imgs[randomIndex];
	}

	function updateImage(newImg: string) {
		if (winRef) {
			winRef.document.getElementById('image').src = newImg; // Update directly
		}
	}

	$: {
		updateImage(imgSrc);
	}
</script>

<div class="card min-w-[400px] max-w-[400px] p-4">
	<span> Information </span>
	<div class="mb-2">
		<img width="360" src={imgSrc} alt="generated for music viz." />
	</div>
	<div>
		<button type="button" class="variant-filled btn-icon"><IconMultiplier1x /></button>
		<button type="button" class="variant-filled btn-icon"><IconMultiplier2x /></button>
		<button type="button" class="variant-filled btn-icon" on:click={openImage}
			><IconWindowMaximize /></button
		>
	</div>
</div>
