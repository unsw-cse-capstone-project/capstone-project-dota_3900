<template>
	<div>
		<Header :isHome="true"></Header>

		<main>
			<div class="search-mainpage">
				<div class="slogan">
					Read · Recommend · Review.
				</div>
				<div class="search-bar">
					<select class="selection" v-model="searchMode">
						<option value="books" style="background-color: purple;">Books</option>
						<option value="users" style="background-color: purple;">Users</option>
					</select>
					<input type="text" placeholder="Book name / Author / ISBN" v-model="searchContent" id="HomePageSearchArea">
					<button type="submit" class="btn-default btn-style-wheat" @click="goToBookSearchPage()" v-if="searchMode === 'books'">Search</button>
					<button type="submit" class="btn-default btn-style-wheat" @click="goToUserSearchPage()" v-if="searchMode === 'users'">Search</button>
				</div>
				<div class="categories-list">
					<div class="popular-books">
						<div class="title">The Most Popular Books</div>
						<ul>
							<router-link v-for="book in popularBooks" :key="book.id" :to="{name: 'Book', query: {id: book.id}}">
								<li>
									<img :src="book.book_cover_url">
									<span><b>{{book.title}}</b></span>
								</li>
							</router-link>
						</ul>
					</div>

					<div class="categories">
						<div class="title">
							The Most Popular Categories
						</div>
						<ul>
							<li v-for="category in categories" :key="category.category" @click="goToSearchPage(category.category)">{{category.category}} - {{category.book_num}}</li>
						</ul>
					</div>
				</div>
			</div>
		</main>

		<Footer></Footer>

	</div>
</template>

<script>
import API_URL from '../serviceAPI.config.js'
import Header from '../components/common/Header.vue'
import Footer from '../components/common/Footer.vue'
export default {
	name: 'HomePage',
	components: {
		Header,
		Footer
	},
	data: function() {
		return {
			searchContent: '',
			popularBooks: [],
			searchMode: 'books',
			categories: []
		}
	},
	methods:{
		goToBookSearchPage(){
			if(this.searchContent !== ''){
				this.$router.push({name: 'SearchResult', query: {content: this.searchContent, page: 1}})
			}
			else{
				alert('Search content cannot be empty.')
			}
		},
		goToUserSearchPage(){
			if(this.searchContent !== ''){
				this.$router.push({name: 'UserSearchResult', query: {content: this.searchContent}})
			}
			else{
				alert('Search content cannot be empty.')
			}
		},
		getPopularBooks(){
			this.axios({
				method: 'get',
				url: `${API_URL}/book/most_popular_book`,
			}).then((res) => {
				this.popularBooks = res.data.books
			}).catch((error) => {
				console.log(error.response.data.message)
			})
		},
		getPopularCategories(){
			this.axios({
				method: 'get',
				url: `${API_URL}/book/most_popular_categories`,
			}).then((res) => {
				this.categories = res.data.categories
			}).catch((error) => {
				console.log(error.response.data.message)
			})
		},
		goToSearchPage(category){
			this.$router.push({name: 'SearchResult', query: {content: this.searchContent, page: 1, category: category}})
		}
	},
	mounted: function(){
		this.getPopularBooks()
		this.getPopularCategories()
	},
	watch: {
		searchMode(){
			let searchArea = document.getElementById('HomePageSearchArea')
			if(this.searchMode === 'books'){
				searchArea.setAttribute('placeholder', 'Book name / Author / ISBN')
			}
			else if(this.searchMode === 'users'){
				searchArea.setAttribute('placeholder', 'User name / ID / Email')
			}	
		}
	},
}
</script>

<style scoped>
	@import url("../assets/css/search.css");
	.selection{
		color: white;
		font-weight: bold;
		border: none;
		background: none;
		font-size: 1rem;
		margin-top: 0.125rem;
		cursor: pointer;
		padding: 0.5rem;
		margin-left: -1rem;
		margin-right: 1rem;
	}
</style>
