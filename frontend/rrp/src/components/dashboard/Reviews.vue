<template>
	<div class="right animation-fadein-top delay_02s">
		<div class="review-list">
			<ul>
				<li v-for="review in reviews" :key="review.review_time">
					<div>
						<router-link :to="{name: 'Book', query: {id: review.book_id}}">
							<img :src="review.book_cover_url" >
						</router-link>
					</div>
					<div class="content">
						<div class="title-operation">
							<router-link :to="{name: 'Book', query: {id: review.book_id}}">
								<span>{{review.book_title}}</span>
							</router-link>
							<div class="operation" v-if="isMyDashboard()">
								<img src="../../../../static_html/img/icon/edit.png" @click="openReveiwRatingForm(review.book_id, review.book_title, review.review_content, review.rating)" >
								<img src="../../../../static_html/img/icon/delete.png" @click="deleteReview(review.book_id, review.book_title)">
							</div>
						</div>
						<div class="rating-bar">
							<StarBar :rating="review.rating"></StarBar>
							<span v-if="review.rating === 1">Bad</span>
							<span v-if="review.rating === 2">Mediocre</span>
							<span v-if="review.rating === 3">Good</span>
							<span v-if="review.rating === 4">Great</span>
							<span v-if="review.rating === 5">Masterpiece</span>
						</div>
						<span><b>Review date: </b>{{timeStamp2datetime(review.review_time)}}</span>
						<span v-html="review.review_content.replace(/\n/g, '<br />')"></span>
					</div>
				</li>	
			</ul>
		</div>
		<ReviewRatingForm ref="reviewRatingForm" :method="'PUT'" :bookID="toEditBookID" :bookName="toEditBookTitle"></ReviewRatingForm>
	</div>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	import StarBar from '../common/StarBar.vue'
	import ReviewRatingForm from '../forms/ReviewRatingForm.vue'
	export default {
		name: 'UserReviews',
		props: ['account', 'myAccount'],
		data: function() {
			return {
				reviews: [],
			
				toEditBookID: '',
				toEditBookTitle: '',
				
				curReview: '',
				curRating: ''
			}
		},
		components: {
			StarBar,
			ReviewRatingForm
		},
		methods: {
			// translate timeStamp to datetime
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
			},
			
			// get all reviews
			getReviews(){
				this.axios.get(`${API_URL}/user/${this.$route.query.id}/reviews`).then((res) => {
					this.reviews = res.data.list
					for(let i = 0; i < this.reviews.length; i++){
						this.reviews[i].review_content = this.reviews[i].review_content
					}
				}).catch((err) => {
					console.log(error.response.data.message)
				})
			},
			
			// determine whether is my dashboard
			isMyDashboard() {
				return this.myAccount.user_id === this.account.user_id ? true : false
			},
			
			// delete current user's review
			deleteReview(bookID, bookName) {
				if(confirm(`Are you sure to remove your review and rating from \'${bookName}\'?`)){
					this.axios({
						method: 'delete',
						url: `${API_URL}/book/review`,
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						},
						params: { 
							user_id: this.$route.query.id,
							book_id: bookID
						}
					}).then((res) => {
						if(res.status === 200){
							alert('Remove successfully.')
						}
						location.reload()
					}).catch((err) => {
						console.log(err.response.data.message)
						location.reload()
					})
				}
			},
			openReveiwRatingForm(bookID, bookTitle, curReview, curRating){
				this.curRating = curRating
				this.curReview = curReview
				this.$refs['reviewRatingForm'].rating = this.curRating
				this.$refs['reviewRatingForm'].review = this.curReview
				this.toEditBookID = bookID
				this.toEditBookTitle = bookTitle
				let reviewRatingForm = document.getElementById('reviewRatingForm')
				reviewRatingForm.style.display = 'block'		
			},
		},
		mounted: function() {
			this.getReviews()
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/user_reviews.css");
</style>
