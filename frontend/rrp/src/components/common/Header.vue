<template>
	<header :class="{'opacity-background': isHome}">
		<div class="left">
			<router-link :to="{name: 'Home'}">
				<div class="title">「 Read Recommendation Pro」</div>
			</router-link>
			<div class="search" v-if="isHome !== true">
				<select class="selection" v-model="searchMode">
					<option value="books" style="background-color: purple;">Books</option>
					<option value="users" style="background-color: purple;">Users</option>
				</select>
				<input class="search_bar" type="text" placeholder="Book title / Author / ISBN" v-model="searchContent" id="headerSearchArea">
				<button class="search_btn" @click.prevent="goToBookSearchPage()" v-if="searchMode === 'books'">Search</button>
				<button class="search_btn" @click.prevent="goToUserSearchPage()" v-if="searchMode === 'users'">Search</button>
			</div>
		</div>
		
		<div class="right" v-if="$store.state.token">
			<router-link :to="{name: 'UserCollection', query: {id: account.user_id}}">
				<span>{{ account.username }} - Dashboard</span>
			</router-link>
			
			<span> | </span>
			<span @click="logout">Logout</span>
		</div>
		<div class="right" v-else>
			<span @click="openLoginForm">Login</span>
			<span> | </span>
			<span @click="openRegisterForm">Register</span>
		</div>
		
		<LoginForm></LoginForm>
		<RegisterForm></RegisterForm>
		
	</header>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	import LoginForm from '../forms/LoginForm.vue'
	import RegisterForm from '../forms/RegisterForm.vue'
	export default {
		name: 'Header',
		props: ['isHome'],
		data: function() {
			return {
				account:{
					user_id: '',
					username: '',
					email: '',
					admin: ''
				},
				searchContent: '',
				searchMode: 'books'
			}
		},
		components:{
			LoginForm,
			RegisterForm
		},
		methods:{
			openLoginForm(){
				let loginForm = document.getElementById('loginForm')
				loginForm.style.display = "block"
			},
			openRegisterForm(){
				let registerForm = document.getElementById('registerForm')
				registerForm.style.display = "block"
			},
			logout(){
			  if(confirm('Are you sure to logout?')){
			    this.$store.commit('clearToken')
					this.clearAccountInfo()
					this.$router.push({name: 'Home'})
			  }
			},
			
			// get current_account info
			getAccountInfo(){
				if(this.$store.state.token){
					this.axios({
					  method: 'get',
					  url: `${API_URL}/user/detail`,
						headers: {
						  'Content-Type': 'application/json',
						  'AUTH-TOKEN': this.$store.state.token
						}
					}).then((res)=>{
						this.account = res.data
					}).catch((error)=>{
					  alert(error.response.data.message)
						this.$store.commit('clearToken')
						this.clearAccountInfo()
						location.reload()
					})
				}
			},
			
			clearAccountInfo(){
				this.account = {
					user_id: '',
					username: '',
					email: '',
					admin: ''
				}
			},
			
			// Execute when search button is pressed
			goToBookSearchPage(){
				if(this.searchContent !== ''){
					this.$router.push({name: 'SearchResult', query: {content: this.searchContent, page: 1}})
				}
				else{
					alert('search content cannot be empty.')
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
		},
		mounted: function(){
			// get User info from token
			this.getAccountInfo()
		},
		watch: {
			'$route' (){
				location.reload()
			},
			searchMode(){
				let searchArea = document.getElementById('headerSearchArea')
				if(this.searchMode === 'books'){
					searchArea.setAttribute('placeholder', 'Book name / Author / ISBN')
				}
				else if(this.searchMode === 'users'){
					searchArea.setAttribute('placeholder', 'User name / ID / Email')
				}	
			}
		}
	}
</script>

<style scoped>
	.selection{
		color: white;
		font-weight: bold;
		border: none;
		background: none;
		font-size: 0.875rem;
		margin-top: 0.125rem;
		cursor: pointer;
		padding: 0.5rem;
		margin-left: -1rem;
		margin-right: 0.5rem;
		margin-left: 0.625rem;
	}
</style>
