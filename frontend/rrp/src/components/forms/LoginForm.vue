<template>
	<div class="modal" id="loginForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Login
				</div>
				<div class="row">
					<span>Username:</span>
					<input type="text" placeholder="Enter username" v-model="account.username" required>
				</div>
				<div class="row">
					<span>Password:</span>
					<input type="password" placeholder="Enter password" v-model="account.password" required>
				</div>
<!-- 				<div class="row">
					<span>Confirm Password:</span>
					<input type="password" placeholder="re-enter password">
				</div>
				<div class="row">
					<span>Option bar1：</span>
					<select>
						<option value="">--</option>
						<option>111</option>
						<option>222</option>
					</select>
					<span>Status：</span>
					<select>
						<option value="true">Enable</option>
						<option value="false">Disable</option>
					</select>
				</div> -->
			</div>

			<div class="container2">
				<button type="submit" class="btn-green" @click.prevent="submit">Login</button>
				<button type="button" class="btn-red" @click.prevent="closeForm">Cancel</button>
			</div>
		</form>
	</div>
</template>

<script>
	import {mapMutations} from 'vuex'
	import API_URL from '../../serviceAPI.config.js'
	export default {
		name: 'LoginForm',
		data: function() {
			return{
				account: {
					username: '',
					password: ''
				}
			}
		},
		methods:{
			...mapMutations(['updateToken']),
			submit(){
				if(this.account.username === '' || this.account.password === ''){
					alert("Please fill in all blanks.")
					return
				}
				this.axios({
				  method: 'post',
				  url: `${API_URL}/token`,
				  data: this.account
				}).then((res)=>{
				  this.updateToken(res.data.token)
					alert("Login successfully")
					location.reload()
				}).catch((error)=>{
				  alert(error.response.data.message)
					this.clearForm()
				})
			},
			closeForm(){
				let loginForm = document.getElementById('loginForm')
				loginForm.style.display = 'none'
				this.clearForm()
			},
			clearForm(){
				this.account.username = ''
				this.account.password = ''
			},
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/form.css");
</style>