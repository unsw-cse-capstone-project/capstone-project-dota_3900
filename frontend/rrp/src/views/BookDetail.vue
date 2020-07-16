<template>
	<div class="root">
		<Header></Header>

		<!-- 404 page if there is no book_id in query -->
		<main v-if="pageNotFound">
			<NotFound></NotFound>
		</main>

		<main v-else>
			<div class="book-bar animation-fadein-top delay_02s">
				<div class="left">
					<img :src="book.book_cover_url">
				</div>
				<div class="right">
					<h6>ISBN: {{ book.ISBN13 }}</h6>
					<h2>{{ book.title }}</h2>
					<ul>
						<li>
							<span>Authors: </span>
							<span>{{ book.authors }}</span>
						</li>
						<li id="desc">
							<span>Description: </span>
							<span>{{ book.description }}</span>
							<div class="more" id="view-more"> <span @click="showAllText()">more >></span> </div>
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
							<span><b>{{ book.avg_rating }}</b> ({{ book.num_rated }} votes)</span>
							<span style="font-size: 0.75rem; color:#888888">Rating from google books: {{book.google_rating}} ({{book.google_ratings_count}}
								votes)</span>
						</div>
					</div>
					<div class="operation-bar" v-if="$store.state.token">
						<button class="btn-default btn-style-orange" style="background-color: orangered; color: white;" @click="openAddBookForm(book.book_id, book.title)">Add to collection</button>
						<button class="btn-default btn-style-softgreen" v-if="!bookStatus.read" @click="openMarkReadForm(book.book_id, book.title)">Mark as read</button>
						<button class="btn-default btn-style-softwheat" v-if="bookStatus.read" @click="markAsUnread()">Mark as unread</button>
						<button class="btn-default btn-style-blue" v-if="bookStatus.read && !bookStatus.review" @click="openAddReviewForm('POST')">Write a review</button>
						<button class="btn-default btn-style-blue" v-if="bookStatus.read && bookStatus.review" @click="openAddReviewForm('PUT')">Modify review</button>
						<button class="btn-default btn-style-orange" v-if="bookStatus.read && bookStatus.review" @click="deleteReview(book.book_id, book.title)">Delete review</button>
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
						<img src="http://books.google.com/books/content?id=Opf3yeQixwQC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../../public/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="http://books.google.com/books/content?id=Opf3yeQixwQC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../../public/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="http://books.google.com/books/content?id=Opf3yeQixwQC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../../public/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="http://books.google.com/books/content?id=Opf3yeQixwQC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../../public/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="http://books.google.com/books/content?id=Opf3yeQixwQC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../../public/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
					<li>
						<img src="http://books.google.com/books/content?id=Opf3yeQixwQC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api">
						<span>Attack on titan</span>
						<div class="rating">
							<img src="../../public/icon/star.png">
							<span>4.3</span>
						</div>
					</li>
				</ul>
			</div>
		</main>

		<AddBookForm :myAccountID="myAccount.user_id" :toMoveBookID="toAddBookID" :toMoveBookName="toAddBookName"></AddBookForm>
		<ReviewRatingForm ref="reviewRatingForm" :method="reviewRatingMethod" :bookID="book.book_id" :oldRating="myRating"></ReviewRatingForm>
		<MarkReadForm :bookID="toMarkReadBookID" :bookName="toMarkReadBookName" @updateData="getBookStatus" ></MarkReadForm>
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
	import AddBookForm from '../components/forms/AddBookForm.vue'
	import ReviewRatingForm from '../components/forms/ReviewRatingForm.vue'
	import MarkReadForm from '../components/forms/MarkReadForm.vue'
	export default {
		name: 'BookDetail',
		data: function() {
			return {
				myAccount: {
					user_id: '',
					username: '',
					email: '',
					admin: ''
				},
				myReview: '',
				myRating: '',
				bookStatus: {
					read: false,
					review: false
				},
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
				pageNotFound: false,

				toAddBookID: '',
				toAddBookName: '',
				
				reviewRatingMethod: '',
				
				toMarkReadBookID: '',
				toMarkReadBookName: '',
			}
		},
		components: {
			Header,
			Footer,
			NotFound,
			StarBar,
			Review,
			AddBookForm,
			ReviewRatingForm,
			MarkReadForm,
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
			showAllText() {
				let desc = document.getElementById('desc')
				let more = document.getElementById('view-more')
				if (desc.offsetHeight >= 112) {
					desc.style.maxHeight = 'none'
					desc.style.overflow = 'none'
					more.style.display = 'none'
				}
			},
			openAddBookForm(bookID, bookName) {
				this.toAddBookID = bookID
				this.toAddBookName = bookName
				let addBookForm = document.getElementById('addBookForm')
				addBookForm.style.display = 'block'
			},
			getAccountsInfo() {
				// get my info (if exists)
				if (this.$store.state.token) {
					this.axios({
						method: 'get',
						url: `${API_URL}/user/detail`,
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						}
					}).then((res) => {
						this.myAccount = res.data
						this.axios({
								method: 'get',
								url: `${API_URL}/book/review`,
								params: {
									book_id: this.$route.query.id,
									user_id: this.myAccount.user_id
								}
							}).then((resp) => {
								if(resp.data.reviews.length > 0){
									this.myReview = resp.data.reviews[0].review_content
									this.myRating = resp.data.reviews[0].rating
								}
							}).catch((error1) => {
								console.log(error1.response.data.message)
							})
					}).catch((error) => {
						this.$store.commit('clearToken')
					})
				}
			},
			getBookStatus() {
				if (this.$store.state.token) {
					this.axios({
						method: 'get',
						url: `${API_URL}/book/read_review_check`,
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						},
						params: {
							book_id: this.$route.query.id,
						}
					}).then((res) => {
						this.bookStatus = res.data
					}).catch((error) => {
						console.log(error.response.data.message)
					})
				}
			},
			markAsUnread() {
				if (confirm('Are you sure to mark this book as Unread?\nYour review and ratings for this book(if exist) will be removed.')) {
					this.axios({
						method: 'post',
						url: `${API_URL}/book/unread`,
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						},
						params: {
							book_id: this.$route.query.id,
						}
					}).then((res) => {
						this.getBookStatus()
						this.getBookDetails()
						this.myRating = ''
						this.myReview = ''
					}).catch((error) => {
						console.log(error.response.data.message)
					})
				}
			},
			openAddReviewForm(method){
				this.reviewRatingMethod = method
				this.$refs['reviewRatingForm'].review = this.myReview
				this.$refs['reviewRatingForm'].rating = this.myRating
				let reviewRatingForm = document.getElementById('reviewRatingForm')
				reviewRatingForm.style.display = 'block'
			},
			openMarkReadForm(bookID, bookName){
				this.toMarkReadBookID = bookID
				this.toMarkReadBookName = bookName
				let reviewRatingForm = document.getElementById('markReadForm')
				reviewRatingForm.style.display = 'block'
			},
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
							user_id: this.myAccount.user_id,
							book_id: bookID
						}
					}).then((res) => {
						if(res.status === 200){
							alert('Remove successfully.')
						}
						location.reload()
					}).catch((err) => {
						console.log(error.response.data.message)
						location.reload()
					})
				}
			},
		},
		created: function() {
			this.getAccountsInfo()
			this.getBookDetails()
			this.getBookStatus()
		},
	}
</script>

<style scoped>
	@import url("../assets/css/common.css");
	@import url("../assets/css/book_page.css");
</style>
