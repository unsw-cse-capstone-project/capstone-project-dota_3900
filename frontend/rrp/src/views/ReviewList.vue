<template>
	<div class="root">
		<Header></Header>
		
		<main v-if="pageNotFound">
			<NotFound></NotFound>
		</main>
		
		<main v-else>
			<div class="book-reviews-container">
				<div class="left animation-fadein-top delay_02s">
					<h3>
						{{ book.title }} - Reviews
					</h3>
					<ul class="no-result" v-if="reviewList.length === 0">
						No Review.
					</ul>
					<ul>
						<li v-for="review in reviewList" :key="review.user_id">
							<div class="user-info">
								<router-link :to="{ name: 'UserCollection', query: {id: review.user_id}}">
									<span>{{ review.username }}</span>
								</router-link>
								<div class="ratings">
									<StarBar :rating="review.rating"></StarBar>
								</div>
								<div class="comment-datetime">
									{{ timeStamp2datetime(review.review_time) }}
								</div>
							</div>
							<span class="comment" v-html="review.review_content.replace(/\n/g, '<br />')"></span>
						</li>
					</ul>
					
					
					<div class="pages-bar" v-if="reviewList.length > 0">
						<router-link v-if="lastPage >= 1" :to="{name: 'BookReviews', query: {content: $route.query.id, page: lastPage}}">
							<div><< previous page</div>
						</router-link>
						<router-link :to="{name: 'BookReviews', query: {content: $route.query.id, page: 1}}">
							<li :class="{'selected': isCurrentPage(1)}">1</li>
						</router-link>
						<span v-if="curPageNum > 6">...</span>
						<router-link v-for="(n, key) in indexs" :key="key" :to="{name: 'BookReviews', query: {content: $route.query.id, page: n}}">
							<li :class="{'selected': isCurrentPage(n)}">{{n}}</li>
						</router-link>
						<span v-if="curPageNum < totalPageNum - 5">...</span>
						<router-link :to="{name: 'BookReviews', query: {content: $route.query.id, page: totalPageNum}}">
							<li v-if="totalPageNum != 1" :class="{'selected': isCurrentPage(totalPageNum)}">{{totalPageNum}}</li>
						</router-link>
						<router-link v-if="nextPage <= totalPageNum" :to="{name: 'BookReviews', query: {content: $route.query.id, page: nextPage}}">
							<div>next page >></div>
						</router-link>
					</div>
					
				</div>

				<div class="right animation-fadein-top delay_04s">
					<router-link :to="{name: 'Book', query: {id: book.book_id}}">
						<img :src="book.book_cover_url">
						<div class="book-title">
								{{ book.title }}
						</div>
					</router-link>
					<li>
						<span>Author: </span>
						<span>{{ book.authors }}</span>
					</li>
					<li>
						<span>Publisher: </span>
						<span>{{ book.publisher }}</span>
					</li>
					<li>
						<span>Publish date: </span>
						<span>{{ book.published_date }}</span>
					</li>
					<li>
						<span>Language: </span>
						<span>{{ book.language }}</span>
					</li>
					<li>
						<span>Category: </span>
						<span>{{book.categories}}</span>
					</li>
				</div>
			</div>
		</main>
		<Footer></Footer>
	</div>
</template>

<script>
	import API_URL from '../serviceAPI.config.js'
	import NotFound from '../components/common/NotFound.vue'
	import Header from '../components/common/Header.vue'
	import Footer from '../components/common/Footer.vue'
	import StarBar from '../components/common/StarBar.vue'
	
	export default {
		name: 'HomePage',
		data: function(){
			return {
				reviewList: [],
				book: {},
				pageNotFound: false,
				totalPageNum: 0,
				curPageNum: 0,
			}
		},
		computed: {
			indexs: function() {
				let indexs = [];
				for(let i = this.curPageNum - 4; i <= this.curPageNum + 4; i++){
					if(i > 1 && i < this.totalPageNum){
						indexs.push(i)
					}
				}
				return indexs
			},
			lastPage: function(){
				return this.curPageNum - 1
			},
			nextPage: function(){
				return this.curPageNum + 1
			}
		},
		components: {
			Header,
			Footer,
			NotFound,
			StarBar
		},
		methods: {
			getBookDetails() {
				let bookID = this.$route.query.id
				this.axios({
					method: 'get',
					url: `${API_URL}/book/${bookID}/detail`,
				}).then((res) => {
					this.book = res.data
					this.book.categories = this.book.categories.replace(/\[\'/, '').replace(/\'\]/, '')
					this.book.authors = this.book.authors.replace(/\[\'/, '').replace(/\'\]/, '').split("', '").join(", ")
					if (this.book.num_rated < 1) {
						this.book.avg_rating = 'Not enough votes'
					} else {
						this.book.avg_rating = this.book.avg_rating.toFixed(1)
					}
				}).catch((error) => {
					this.pageNotFound = true
				})
			},
			getReviews(){
				let bookID = this.$route.query.id
				let page = this.$route.query.page
				this.axios({
					method: 'get',
					url: `${API_URL}/book/review_page`,
					params: {
						book_id: bookID,
						page: page
					}
				}).then((res) => {
					this.reviewList = res.data.reviews
					this.totalPageNum = res.data.total_page_num
					console.log(this.reviewList)
				}).catch((error) => {
					this.pageNotFound = true
				})
			},
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
			isCurrentPage(num){
				return num == this.curPageNum
			},
		},
		mounted: function(){
			if(!this.$route.query.id || this.$route.query.page === undefined){
				this.pageNotFound = true
				return
			}
			this.getBookDetails()
			this.getReviews()
			this.curPageNum = this.$route.query.page
		}
	}
	
</script>

<style scoped>
	@import url("../assets/css/book_reviews.css");
	.no-result{
		margin-top: 6.25rem;
	}
</style>
