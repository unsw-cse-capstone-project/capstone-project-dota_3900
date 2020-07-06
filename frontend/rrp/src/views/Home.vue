<template>
	<div>
		<Header :isHome="true"></Header>

		<main>
			<div class="search-mainpage">
				<div class="slogan">
					Read · Recommend · Review.
				</div>
				<div class="search-bar">
					<input type="text" placeholder="Book name / Author / ISBN" v-model="searchContent">
					<button type="submit" class="btn-default btn-style-wheat" @click="goToSearchPage()">Search</button>
				</div>
				<div class="categories-list">
					<div class="popular-books">
						<div class="title">The Most Popular Books (Random now)</div>
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
							<li>Fiction - 2528</li>
							<li>Juvenile Fiction - 522</li>
							<li>Biography & Autobiography - 382</li>
							<li>History - 214</li>
							<li>Philosophy - 132</li>
							<li>Religion - 112</li>
							<li>Comics & Graphic Novels - 110</li>
							<li>Drama - 103</li>
							<li>Literary Criticism - 96</li>
							<li>Business & Economics - 80</li>
							<li>Juvenile Nonfiction - 74</li>
							<li>Science - 80</li>
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
		}
	},
	methods:{
		goToSearchPage(){
			if(this.searchContent !== ''){
				this.$router.push({name: 'SearchResult', query: {content: this.searchContent, page: 1}})
			}
			else{
				alert('search content cannot be empty.')
			}
		},
		getPopularBooks(){
			this.axios({
				method: 'get',
				url: `${API_URL}/book/most_popular`,
			}).then((res) => {
				this.popularBooks = res.data.books
			}).catch((error) => {
				console.log(error.response.data.message)
				this.pageNotFound = true
			})
		},
	},
	mounted: function(){
		this.getPopularBooks()
	}
}
</script>

<style scoped>
	@import url("../assets/css/search.css");
</style>
