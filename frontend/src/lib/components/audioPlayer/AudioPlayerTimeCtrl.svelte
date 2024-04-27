<script lang="ts">
	let currentFrame = 50;
	let numberOfFrames = 100;

	let currentTimeStamp = '--:--';
	let endTimeStamp = '--:--';
</script>

<div class="time-control-container flex flex-col">
	<input
		class="mt-4"
		type="range"
		bind:value={currentFrame}
		min="0"
		max={numberOfFrames}
		step="1"
	/>
	<div class="time-container flex flex-row justify-between">
		<span>{currentTimeStamp}</span>
		<span>{endTimeStamp}</span>
	</div>
</div>
