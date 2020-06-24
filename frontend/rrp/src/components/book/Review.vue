<template>
	<li v-if="review">
		<div class="user-info">
			<span>{{ review.username }}</span>
			<div class="ratings">
				<StarBar :rating="review.rating"></StarBar>
			</div>
			<div class="comment-datetime">
				{{ review.review_time }}
			</div>
		</div>
		<div class="comment">
			{{ review.review_content }}
		</div>
	</li>
</template>

<script>
	import StarBar from '../common/StarBar.vue'
	export default {
		name: 'BookReview',
		props: ['review'],
		components: {
			StarBar,
		},
	}
</script>

<style>
</style>
