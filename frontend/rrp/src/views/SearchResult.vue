<template>
	<div class="root">
		<Header></Header>

		<main v-if="pageNotFound">
			<NotFound></NotFound>
		</main>

		<main v-else>
			<div class="search-results-list">
				<div class="search-title">
					Search result for "{{$route.query.content}}":
				</div>
				<ul v-for="book in searchResult" :key="book.id">
					<li>
						<!-- <li v-for="book from searchResult"> -->
						<div class="info">
							<img :src="book.book_cover_url">
							<div class="book-detail">
								<div class="title-operation">
									<span><b>{{book.title}}</b></span>
									<div class="operation">
										<img src="../../public/icon/star.png">
										<span v-if="book.average == 0">--</span>
										<span v-else>{{book.average}}</span>
										<button class="btn-default btn-style-orange">Add to collection</button>
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

				<div class="pages-bar">
					<router-link v-if="lastPage >= 1" :to="{name: 'SearchResult', query: {content: $route.query.content, page: lastPage}}">
						<div><< previous page</div>
					</router-link>
					<router-link :to="{name: 'SearchResult', query: {content: $route.query.content, page: 1}}">
						<li :class="{'selected': isCurrentPage(1)}">1</li>
					</router-link>
					<span v-if="curPageNum > 6">...</span>
					<router-link v-for="n in indexs" :to="{name: 'SearchResult', query: {content: $route.query.content, page: n}}">
						<li :class="{'selected': isCurrentPage(n)}">{{n}}</li>
					</router-link>
					<span v-if="curPageNum < totalPageNum - 5">...</span>
					<router-link :to="{name: 'SearchResult', query: {content: $route.query.content, page: totalPageNum}}">
						<li :class="{'selected': isCurrentPage(totalPageNum)}">{{totalPageNum}}</li>
					</router-link>
					<router-link v-if="nextPage <= totalPageNum" :to="{name: 'SearchResult', query: {content: $route.query.content, page: nextPage}}">
						<div>next page >></div>
					</router-link>
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
	export default {
		name: 'HomePage',
		components: {
			Header,
			Footer,
			NotFound
		},
		computed: {
			indexs: function() {
				var indexs = [];
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
				if (content === '' || page === '') {
					this.pageNotFound = true
					return
				}
				this.axios({
					method: 'get',
					url: `${API_URL}/book/search_page`,
					params: {
						search_content: content,
						page: page
					}
				}).then((res) => {
					this.searchResult = res.data.result
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
			}
		},
		mounted: function() {
			this.getUserInfo()
			this.getSearchResult()
		}
	}
</script>

<style>
	@import url("../assets/css/search_result.css");
</style>
