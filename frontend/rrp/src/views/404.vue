<template>
	<div class="root">
		<Header></Header>
		<main>
			<NotFound></NotFound>
		</main>
		<Footer></Footer>
	</div>
</template>

<script>
	import Header from '../components/common/Header.vue'
	import Footer from '../components/common/Footer.vue'
	import NotFound from '../components/common/NotFound.vue'
	export default {
		name: 'NotFoundPage',
		components: {
			Header,
			Footer,
			NotFound,
		},
	}
</script>

<style scoped>
	@import url("../assets/css/common.css");
</style>
