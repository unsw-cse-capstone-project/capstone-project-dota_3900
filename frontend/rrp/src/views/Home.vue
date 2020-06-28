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
					<button class="btn-default btn-style-wheat" @click.prevent="goToSearchPage()">Search</button>
				</div>
				<div class="categories-list">
					<div class="popular-books">
						<div class="title">The Most Popular Books</div>
						<ul>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
							<li>
								<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
								<span><b>Attack on Titan - Volume 14</b></span>
							</li>
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
			searchContent: ''
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
		}
	}
}
</script>

<style scoped>
	@import url("../assets/css/search.css");
</style>
