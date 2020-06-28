<template>
	<header :class="{'opacity-background': isHome}">
		<div class="left">
			<router-link :to="{name: 'Home'}">
				<div class="title">「 Read Recommendation Pro」</div>
			</router-link>
			<div class="search" v-if="isHome !== true">
				<input class="search_bar" type="text" placeholder="Book title / Author / ISBN" v-model="searchContent">
				<button class="search_btn" @click.prevent="goToSearchPage()">
					Search
				</button>
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
			goToSearchPage(){
				if(this.searchContent !== ''){
					this.$router.push({name: 'SearchResult', query: {content: this.searchContent, page: 1}})
				}
				else{
					alert('search content cannot be empty.')
				}
			}
		},
		mounted: function(){
			// get User info from token
			this.getAccountInfo()
		},
		watch: {
			'$route' (){
				location.reload()
			}
		}
	}
</script>

<style>
</style>
