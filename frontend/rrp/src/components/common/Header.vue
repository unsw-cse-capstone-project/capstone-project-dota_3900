<template>
	<header :class="{'opacity-background': isHome}">
		<div class="left">
			<div class="title">
				「 Read Recommendation Pro」
			</div>
			<div class="search" v-if="isHome === false">
				<input class="search_bar" type="text" placeholder="Book title / Author / ISBN">
				<button class="search_btn">
					Search
				</button>
			</div>
		</div>
		
		<div class="right" v-if="$store.state.token">
			<span>{{ account.username }}</span>
			<span> | </span>
			<span @click="logout">logout</span>
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
				}
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
					location.reload()
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
		},
		created: function(){
			// get User info from token
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
				})
			}
		}
	}
</script>

<style>
</style>
