<template>
	<div class="root">
		<Header></Header>

		<main v-if="pageNotFound">
			<NotFound></NotFound>
		</main>

		<main v-else>
			<div class="search-results-list">
				<div v-if="$route.query.content !== ''" class="search-title">
					Search result for "{{$route.query.content}}":
				</div>
				<div class="filter">
					<span>Filter:</span>
					<span style="margin-right: 0.25rem;">Rating: from </span>
					<select v-model="filter.ratingFrom">
						<option value="0">--</option>
						<option value="1" v-if="filter.ratingTo >= 1 || filter.ratingTo == 0">1</option>
						<option value="2" v-if="filter.ratingTo >= 2 || filter.ratingTo == 0">2</option>
						<option value="3" v-if="filter.ratingTo >= 3 || filter.ratingTo == 0">3</option>
						<option value="4" v-if="filter.ratingTo >= 4 || filter.ratingTo == 0">4</option>
						<option value="5" v-if="filter.ratingTo >= 5 || filter.ratingTo == 0">5</option>
					</select>
					<span style="margin-right: 0.375rem;"> to </span>
					<select v-model="filter.ratingTo">
						<option value="0">--</option>
						<option value="1" v-if="filter.ratingFrom <= 1 || filter.ratingFrom == 0">1</option>
						<option value="2" v-if="filter.ratingFrom <= 2 || filter.ratingFrom == 0">2</option>
						<option value="3" v-if="filter.ratingFrom <= 3 || filter.ratingFrom == 0">3</option>
						<option value="4" v-if="filter.ratingFrom <= 4 || filter.ratingFrom == 0">4</option>
						<option value="5" v-if="filter.ratingFrom <= 5 || filter.ratingFrom == 0">5</option>
					</select>
					<span style="margin-left: 2rem;">Category:</span>
					<select v-model="filter.category">
						<option value="all">All</option>
						<option v-for="(value, key) in categoryList" :key="key" :value="value">{{value}}</option>
					</select>
					<button @click="applyFilter()" class="btn-default btn-style-orange" style="font-size: 0.75rem; padding: 0.25rem 1rem; margin-left: 1rem;">Apply</button>
				</div>
				<ul class="no-result" v-if="!hasSearchResult">
					No Search Result.
				</ul>
				<ul v-for="book in searchResult" :key="book.id" v-else>
					<li>
						<!-- <li v-for="book from searchResult"> -->
						<div class="info">
							<router-link :to="{name: 'Book', query: {id: book.id}}">
								<img :src="book.book_cover_url">
							</router-link>
							<div class="book-detail">
								<div class="title-operation">
									<router-link :to="{name: 'Book', query: {id: book.id}}">
										<span><b>{{book.title}}</b></span>
									</router-link>
									<div class="operation">
										<img src="../../public/icon/star.png">
										<span v-if="book.average === null">--</span>
										<span v-else>{{book.average}}</span>
										<button class="btn-default btn-style-orange" v-if="$store.state.token" @click="openAddBookForm(book.id, book.title)">Add to collection</button>
										<button class="btn-default btn-style-softgreen" v-if="$store.state.token && !book.bookStatus.read" @click="openMarkReadForm(book.id, book.title)">Mark as read</button>
										<button class="btn-default btn-style-softwheat" v-if="$store.state.token && book.bookStatus.read" @click="markAsUnread(book.id)">Mark as unread</button>
									</div>
								</div>
								<span><b>Author: </b>{{plainAuthors(book.authors)}}</span>
								<span><b>Description: </b>{{book.description}}</span>
								<span><b>Publisher & publication date: </b>{{book.publisher}} ({{book.published_date}})</span>
								<span><b>Category: </b>{{plainCategories(book.categories)}}</span>
							</div>
						</div>
					</li>
				</ul>

				<div class="pages-bar" v-if="searchResult.length > 0">
					<router-link v-if="lastPage >= 1" :to="{name: 'SearchResult', query: {content: $route.query.content, page: lastPage, ratingFrom: $route.query.ratingFrom, ratingTo: $route.query.ratingTo, category: $route.query.category}}">
						<div><< previous page</div>
					</router-link>
					<router-link :to="{name: 'SearchResult', query: {content: $route.query.content, page: 1, ratingFrom: $route.query.ratingFrom, ratingTo: $route.query.ratingTo, category: $route.query.category}}">
						<li :class="{'selected': isCurrentPage(1)}">1</li>
					</router-link>
					<span v-if="curPageNum > 6">...</span>
					<router-link v-for="(n, key) in indexs" :key="key" :to="{name: 'SearchResult', query: {content: $route.query.content, page: n, ratingFrom: $route.query.ratingFrom, ratingTo: $route.query.ratingTo, category: $route.query.category}}">
						<li :class="{'selected': isCurrentPage(n)}">{{n}}</li>
					</router-link>
					<span v-if="curPageNum < totalPageNum - 5">...</span>
					<router-link :to="{name: 'SearchResult', query: {content: $route.query.content, page: totalPageNum, ratingFrom: $route.query.ratingFrom, ratingTo: $route.query.ratingTo, category: $route.query.category}}">
						<li v-if="totalPageNum != 1" :class="{'selected': isCurrentPage(totalPageNum)}">{{totalPageNum}}</li>
					</router-link>
					<router-link v-if="nextPage <= totalPageNum" :to="{name: 'SearchResult', query: {content: $route.query.content, page: nextPage, ratingFrom: $route.query.ratingFrom, ratingTo: $route.query.ratingTo, category: $route.query.category}}">
						<div>next page >></div>
					</router-link>
				</div>
			</div>
			
			<AddBookForm :myAccountID="myAccount.user_id" :toMoveBookID="toAddBookID" :toMoveBookName="toAddBookName"></AddBookForm>
			<MarkReadForm :bookID="toMarkReadBookID" :bookName="toMarkReadBookName" @updateData="getSearchResult"></MarkReadForm>

		</main>

		<Footer></Footer>
	</div>
</template>

<script>
	import API_URL from '../serviceAPI.config.js'
	import NotFound from '../components/common/NotFound.vue'
	import Header from '../components/common/Header.vue'
	import Footer from '../components/common/Footer.vue'
	import AddBookForm from '../components/forms/AddBookForm.vue'
	import MarkReadForm from '../components/forms/MarkReadForm.vue'
	export default {
		name: 'HomePage',
		components: {
			Header,
			Footer,
			NotFound,
			AddBookForm,
			MarkReadForm
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
		data: function() {
			return {
				searchResult: [],
				totalPageNum: '',
				curPageNum: '',
				pageBarNums: [],

				myAccount: {
					user_id: '',
					username: '',
					email: '',
					admin: ''
				},
				pageNotFound: false,
				
				isReadList: {},
				
				toAddBookID: '',
				toAddBookName: '',
				
				toMarkReadBookID: '',
				toMarkReadBookName: '',
				
				hasSearchResult: true,
				
				filter: {
					ratingFrom: 0,
					ratingTo: 0,
					category: 'all',
				},
				
				categoryList: ['Fiction', 'Juvenile Fiction', 'Biography & Autobiography', 'History', 'Philosophy', 'Religion',
				 'Comics & Graphic Novels', 'Drama', 'Literary Criticism', 'Business & Economics', 'Juvenile Nonfiction', 'Science',
				 'Literary Collections', 'Poetry', 'Social Science', 'Performing Arts', 'Humor', 'Psychology', 'Self-Help', 'Cooking']
			}
		},
		methods: {
			getUserInfo() {
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
					}).catch((error) => {
						this.$store.commit('clearToken')
					})
				}
			},
			getSearchResult() {
				let content = this.$route.query.content
				let page = this.$route.query.page
				let query = {}
				query.search_content = content
				query.page = page
				if(this.$route.query.ratingFrom !== undefined){
					query.rating_from = this.$route.query.ratingFrom
				}
				if(this.$route.query.ratingTo !== undefined){
					query.rating_to = this.$route.query.ratingTo
				}
				if(this.$route.query.category !== undefined){
					query.category = this.$route.query.category
				}
				console.log(query)
				this.axios({
					method: 'get',
					url: `${API_URL}/book/search_page`,
					params: query
				}).then((res) => {
					for(let i = 0; i < res.data.result.length; i++){
						res.data.result[i].bookStatus = {read: false, review: false}
						if (this.$store.state.token) {
							this.axios({
								method: 'get',
								url: `${API_URL}/book/read_review_check`,
								headers: {
									'Content-Type': 'application/json',
									'AUTH-TOKEN': this.$store.state.token
								},
								params: {
									book_id: res.data.result[i].id
								}
							}).then((resp) => {
								res.data.result[i].bookStatus = resp.data
							}).catch((error) => {
								console.log(error.response.data.message)
							})
						}
					}
					this.searchResult = res.data.result
					if(this.searchResult.length == 0){
						this.hasSearchResult = false
					}
					this.curPageNum = res.data.current_page
					this.totalPageNum = res.data.total_page_num
				}).catch((error) => {
					console.log(error.response.data.message)
					this.pageNotFound = true
				})
			},
			plainCategories(categories) {
				return categories.replace(/\[\'/, '').replace(/\'\]/, '')
			},
			plainAuthors(authors) {
				return authors.replace(/\[\'/, '').replace(/\'\]/, '').split("', '").join(", ")
			},
			isCurrentPage(num){
				return num == this.curPageNum
			},
			openMarkReadForm(bookID, bookName){
				this.toMarkReadBookID = bookID
				this.toMarkReadBookName = bookName
				let reviewRatingForm = document.getElementById('markReadForm')
				reviewRatingForm.style.display = 'block'
			},
			markAsUnread(bookID) {
				if (confirm('Are you sure to mark this book as Unread?\nYour review and ratings for this book(if exist) will be removed.')) {
					this.axios({
						method: 'post',
						url: `${API_URL}/book/unread`,
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						},
						params: {
							book_id: bookID
						}
					}).then((res) => {
						this.getSearchResult()
					}).catch((error) => {
						console.log(error.response.data.message)
					})
				}
			},
			openAddBookForm(bookID, bookName) {
				this.toAddBookID = bookID
				this.toAddBookName = bookName
				let addBookForm = document.getElementById('addBookForm')
				addBookForm.style.display = 'block'
			},
			applyFilter(){
				let query  = {}
				query.content = this.$route.query.content
				query.page = "1"
				if(this.filter.ratingFrom != 0){
					query.ratingFrom = this.filter.ratingFrom
				}
				if(this.filter.ratingTo != 0){
					query.ratingTo = this.filter.ratingTo
				}
				if(this.filter.category != 'all'){
					query.category = this.filter.category
				}
				if(query.ratingFrom != this.$route.query.ratingFrom || query.ratingTo != this.$route.query.ratingTo || query.category != this.$route.query.category){
					this.$router.push({name: 'SearchResult', query: query})
				}
				else{
					alert('No new filter applied.')
				}
			}
		},
		created: function() {
			if(this.$route.query.ratingFrom !== undefined){
				if(this.$route.query.ratingFrom <= 5 && this.$route.query.ratingFrom >= 0){
					this.filter.ratingFrom = this.$route.query.ratingFrom
				}
			}
			if(this.$route.query.ratingTo!== undefined){
				if(this.$route.query.ratingTo <= 5 && this.$route.query.ratingTo >= 0){
					this.filter.ratingTo = this.$route.query.ratingTo
				}
			}
			if(this.filter.ratingTo < this.filter.ratingFrom && this.filter.ratingTo != 0 && this.filter.ratingFrom != 0){
				this.pageNotFound = true
				return
			}
			if(this.$route.query.category !== undefined){
				this.filter.category = this.$route.query.category
			}
			if(this.$route.query.category != undefined){
				this.filter.category = this.$route.query.category
			}
			this.getUserInfo()
			this.getSearchResult()
		}
	}
</script>

<style scoped>
	@import url("../assets/css/search_result.css");
	.filter{
		margin-top: 0.625rem;
		font-size: 0.875rem;
	}
	.filter span{
		margin-left: 0.625rem;
	}
	.filter span:nth-child(1){
		margin-left: 0rem;
		margin-right: 0.625rem;
	}
	.filter select{
		border: none;
		border-bottom: 0.0625rem #333333 solid;
		background: none;
	}
</style>
