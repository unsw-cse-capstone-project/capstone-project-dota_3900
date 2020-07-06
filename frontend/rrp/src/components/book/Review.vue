<template>
	<li v-if="review">
		<div class="user-info">
			<span>{{ review.username }}</span>
			<div class="ratings">
				<StarBar :rating="review.rating"></StarBar>
			</div>
			<div class="comment-datetime">
				{{ timeStamp2datetime(review.review_time) }}
			</div>
		</div>
		<span class="comment" v-html="review.review_content.replace(/\n/g, '<br />')"></span>
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
		methods:{
			timeStamp2datetime(timeStamp) {
				let datetime = new Date();
				datetime.setTime(timeStamp);
				let year = datetime.getFullYear()
				let month = datetime.getMonth() + 1
				let date = datetime.getDate()
				let hour = datetime.getHours()
				let minute = datetime.getMinutes()
				let second = datetime.getSeconds()
				if (hour < 10) hour = '0' + hour
				if (minute < 10) minute = '0' + minute
				if (second < 10) second = '0' + second
				return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second
			}
		}
	}
</script>

<style>
</style>
