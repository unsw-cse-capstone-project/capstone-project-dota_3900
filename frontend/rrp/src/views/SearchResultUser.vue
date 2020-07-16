<template>
	<div class="root">
		<Header></Header>

<!-- 		<main v-if="pageNotFound">
			<NotFound></NotFound>
		</main> -->

		<main>
			<div class="search-results-list">
				<div class="search-title">
					Search for user - "{{$route.query.content}}":
				</div>
				<ul class="no-result" v-if="noResult">
					No Search Result.
				</ul>
				<ul v-else>
					<li v-for="user in searchResult" :key="user.id">
						<div class="info">
							<span class="span-id"><b>ID: {{user.id}}</b></span>
							<div class="book-detail">
								<router-link :to="{name: 'UserCollection', query: {id: user.id}}">
									<span><b>{{user.username}}</b></span>
								</router-link>
								<span><b>email: </b>{{user.email}}</span>
							</div>
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
	import NotFound from '../components/common/NotFound.vue'
	import Header from '../components/common/Header.vue'
	import Footer from '../components/common/Footer.vue'
	export default {
		name: 'SearchResultUser',
		components: {
			Header,
			Footer,
			NotFound,
		},
		data: function() {
			return {
				searchResult: [],
				noResult: false,
			}
		},
		methods: {
			getSearchResult(){
				if(this.$route.query.content === undefined || this.$route.query.content === ''){
					this.noResult = true
					return
				}
				this.axios({
					method: 'get',
					url: `${API_URL}/user/search_page`,
					params: {
						search_content: this.$route.query.content,
					}
				}).then((res) => {
					this.searchResult = res.data.result
					if(this.searchResult.length === 0){
						this.noResult = true
					}
				}).catch((error) => {
					this.noResult = true
					console.log(error.response.data.message)
				})
			}
		},
		mounted: function() {
			this.getSearchResult()
		}
	}
</script>

<style scoped>
	@import url("../assets/css/search_result.css");
	.span-id {
		font-size: 0.75rem; padding: 0.5rem 1rem; border-radius: 0.25rem; background-color: floralwhite; color: mediumvioletred;
	}
	li {
		width: 62.5rem;
	}
</style>
