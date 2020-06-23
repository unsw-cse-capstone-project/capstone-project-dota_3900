<template>
	<div class="root">
		<Header></Header>

		<!-- 404 page if there is no book_id in query -->
		<main v-if="PageNotFound">
			<NotFound></NotFound>
		</main>

		<main v-else>
			<div class="book-bar animation-fadein-top delay_02s">
				<div class="left">
					<img :src="book.book_cover_url" >
				</div>
				<div class="right">
					<h6>ISBN: {{ book.ISBN13 }}</h6>
					<h2>{{ book.title }}</h2>
					<ul>
						<li>
							<span>Authors: </span>
							<span>{{ book.authors }}</span>
						</li>
						<li>
							<span>Description: </span>
							<span>{{ book.description }}</span>
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
					</ul>
					<div class="rating-bar">
						<span>Rating: </span>
						<div class="star-bar">
							<StarBar :rating="book.avg_rating"></StarBar>
							<span>{{ book.avg_rating }} ({{ book.num_rated }} votes)</span>
							<span style="font-size: 0.75rem; color:#888888">Rating from google books: {{book.google_rating}} ({{book.google_ratings_count}} votes)</span>
						</div>
					</div>
					<div class="operation-bar">
						<button class="btn-default btn-style-orange">Add to collection</button>
						<button class="btn-default btn-style-green">Finished reading</button>
						<button class="btn-default btn-style-wheat">Write a review</button>
						<span> <<< Unfinished part</span>
					</div>
				</div>
			</div>

			<div class="content-bar animation-fadein-top delay_04s">
				<div class="title">
					「 Book reviews」
				</div>
				<div class="comment-list">
					<ul id="review-preview">
						<Review :review="book.review_preview[0]"></Review>
						<Review :review="book.review_preview[1]"></Review>
						<Review :review="book.review_preview[2]"></Review>
					</ul>
					<div class="show-more">
						Show all {{ book.num_rated }} comments >
					</div>
				</div>
			</div>

			<div class="content-bar animation-fadein-top delay_06s">
				<div class="title">「 Recommend similar books for you」</div>
				<ul class="book_list">
					<li>
						<img src="../assets/img/s33646692.jpg">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../assets/img/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="../assets/img/s33646692.jpg">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../assets/img/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="../assets/img/s33646692.jpg">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../assets/img/icon/star.png">
							<span>--</span>
						</div>
					</li>
					<li>
						<img src="../assets/img/s33646692.jpg">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../assets/img/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="../assets/img/s33646692.jpg">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../assets/img/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="../assets/img/s33646692.jpg">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../assets/img/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
				</ul>
			</div>
		</main>

		<Footer></Footer>
	</div>
</template>

<script>
	import API_URL from '../serviceAPI.config.js'
	import Header from '../components/common/Header.vue'
	import Footer from '../components/common/Footer.vue'
	import NotFound from '../components/common/NotFound.vue'
	import StarBar from '../components/common/StarBar.vue'
	import Review from '../components/book/Review.vue'
	export default {
		name: 'BookDetail',
		data: function() {
			return {
				book: {
					"book_id": '',
					"title": '',
					"authors": [],
					"publisher": '',
					"published_date": '',
					"description": '',
					"ISBN13": '',
					"categories": [],
					"google_rating": '',
					"google_ratings_count": '',
					"book_cover_url": '',
					"language": '',
					"avg_rating": '',
					"num_rated": '',
					"review_preview": []
				},
				PageNotFound: false
			}
		},
		components: {
			Header,
			Footer,
			NotFound,
			StarBar,
			Review
		},
		methods: {
			getBookDetails(){
				let book_id = this.$route.query.id
				this.axios({
				  method: 'get',
				  url: `${API_URL}/book/${book_id}/detail`,
				}).then((res)=>{
					this.book = res.data
					this.book.categories = this.book.categories.replace(/\[\'/, '').replace( /\'\]/, '')
					this.book.authors = this.book.authors.replace(/\[\'/, '').replace( /\'\]/, '').split("', '").join(", ")
					if(this.book.num_rated < 10){
						this.book.avg_rating = 'Not enough votes'
					}
				}).catch((error)=>{
					this.PageNotFound = true
				})
			},
			buildStars(rating){
				let noStar = document.createElement(img)
				noStar.src = "../assets/img/icon/no-star.png"
				if (1){
					for(let i = 0; i < 5; i++){
						this.appendChild(noStar)
					}
				}
			},
		},
		created: function() {
			this.getBookDetails()
		}
	}
</script>

<style scoped>
	@import url("../assets/css/common.css");
	@import url("../assets/css/book_page.css");
</style>
