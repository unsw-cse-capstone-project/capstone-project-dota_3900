<template>
	<div class="modal" id="registerForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Register
				</div>
				<div class="row">
					<span>Username:</span>
					<input type="text" placeholder="Enter username (4 - 12 characters)" v-model="account.username">
				</div>
				<div class="row">
					<span>Password:</span>
					<input type="password" placeholder="Enter password (8 - 32 characters, at least one letter)" v-model="account.password">
				</div>
				<div class="row">
					<span>Confirm Password:</span>
					<input type="password" placeholder="Re-enter password" v-model="confirmPassword">
				</div>
				<div class="row">
					<span>Email:</span>
					<input type="text" placeholder="Enter email" v-model="account.email">
				</div>
			</div>

			<div class="container2">
				<button type="" class="btn-green" @click.prevent="submit">Register</button>
				<button type="button" class="btn-red" @click.prevent="closeForm">Cancel</button>
			</div>
		</form>
	</div>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	export default {
		name: 'RegisterForm',
		data: function() {
			return{
				account: {
					username: '',
					password: '',
					email: ''
				},
				confirmPassword: ''
			}
		},
		methods:{
			submit(){
				if(this.account.username === '' || this.account.password === '' || this.account.email === '' || this.confirmPassword === ''){
					alert("Please fill in all blanks.")
					return
				}
				if(this.account.password !== this.confirmPassword){
					alert('Two input password must be consistent.')
					this.account.password = ''
					this.confirmPassword = ''
					return
				}
				if(!this.validateEmail(this.account.email)){
					alert('Invalid Email address.')
					this.account.email = ''
					return
				}
				this.account.email = String(this.account.email).toLowerCase()
				this.axios({
				  method: 'post',
				  url: `${API_URL}/user`,
				  data: this.account
				}).then((res)=>{
					alert("Register successfully, please log in")
					this.closeForm()
				}).catch((error)=>{
				  alert(error.response.data.message)
					this.clearForm()
				})
			},
			closeForm(){
				let registerForm = document.getElementById('registerForm')
				registerForm.style.display = 'none'
				this.clearForm()
			},
			clearForm(){
				this.account.username = ''
				this.account.password = ''
				this.account.email = ''
				this.confirmPassword = ''
			},
			
			// validate email format
			validateEmail(email){
				var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
				return re.test(String(email).toLowerCase())
			}
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/form.css");
</style>