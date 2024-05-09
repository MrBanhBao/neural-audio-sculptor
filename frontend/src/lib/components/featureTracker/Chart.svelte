<script>
	import { onMount, onDestroy } from 'svelte';
	import Chart from 'chart.js/auto';

	let chart; // Reference to the chart instance

	// Data to be plotted on the chart
	let data = {
		labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
		datasets: [
			{
				data: [65, 59, 80, 81, 56, 55, 40],
				fill: false,
				borderColor: 'rgb(75, 192, 192)',
				tension: 0.1
			}
		]
	};

	// Function to create the chart
	function createChart() {
		const ctx = document.getElementById('myChart');
		chart = new Chart(ctx, {
			type: 'line',
			data: data,
			options: {
				scales: {
					y: {
						beginAtZero: true,
						display: true,
						grid: {
							display: false
						}
					},
					x: {
						display: true,
						grid: {
							display: false
						}
					}
				},
				plugins: {
					legend: {
						display: false
					},
					grid: {
						display: false // Hide grid lines
					}
				}
			}
		});
	}

	// Create the chart when the component mounts
	onMount(createChart);

	// Destroy the chart when the component is destroyed to prevent memory leaks
	onDestroy(() => {
		if (chart) {
			chart.destroy();
		}
	});
</script>

<div>
	<canvas class="text-token" id="myChart" height="20"></canvas>
</div>
