<template>
	<li v-if="review">
		<div class="user-info">
			<span>{{ review.username }}</span>
			<div class="ratings">
				<StarBar :rating="review.rating"></StarBar>
			</div>
			<div class="comment-datetime">
				{{ timeStampToDatetime(review.review_time) }}
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
		methods: {
			timeStampToDatetime(timeStamp) {
				let datetime = new Date();
				datetime.setTime(timeStamp);
				let year = datetime.getFullYear();
				let month = datetime.getMonth() + 1;
				let date = datetime.getDate();
				let hour = datetime.getHours();
				let minute = datetime.getMinutes();
				let second = datetime.getSeconds();
				return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second
			}
		}
	}
</script>

<style>
</style>
