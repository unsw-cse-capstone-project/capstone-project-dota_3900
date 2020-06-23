<template>
	<div>
		<img :src="drawStar(1)">
		<img :src="drawStar(2)">
		<img :src="drawStar(3)">
		<img :src="drawStar(4)">
		<img :src="drawStar(5)">
	</div>
</template>

<script>
	
	export default {
		name: 'StarBar',
		props: ['rating'],
		
		methods:{
			drawStar(curStar){
				if(this.rating - curStar >= -0.3){
					return "/icon/star.png"
				}
				else if(this.rating - curStar >= -0.7){
					return "/icon/half-star.png"
				}
				else{
					return "/icon/no-star.png"
				}
			}
		}
	}
</script>


<style>
</style>
