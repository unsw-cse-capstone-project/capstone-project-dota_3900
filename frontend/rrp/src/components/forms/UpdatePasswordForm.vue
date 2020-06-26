<template>
	<div class="modal" id="updatePasswordForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Update Password<br />
				</div>
				<div class="row">
					<span>Current password</span>
					<input type="password" placeholder="Enter current password" v-model="oldPassword" required>
				</div>
				<div class="row">
					<span>New password</span>
					<input type="password" placeholder="Enter new password" v-model="newPassword" required>
				</div>
			</div>
	
			<div class="container2">
				<button type="submit" class="btn-green" @click.prevent="submit()">Submit</button>
				<button type="button" class="btn-red" @click.prevent="closeForm()">Cancel</button>
			</div>
		</form>
	</div>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	export default {
		name: 'UpdatePasswordForm',
		data: function() {
			return{
				oldPassword: '',
				newPassword: '',
			}
		},
		methods:{
			closeForm(){
				let newPasswordForm = document.getElementById('updatePasswordForm')
				newPasswordForm.style.display = 'none'
				this.clearForm()
			},
			clearForm(){
				this.newPassword = ''
			},
			submit(){
				if(this.newPassword === '' || this.oldPassword === ''){
					alert('Please fill all blanks')
					return
				}
				if(this.newPassword === this.oldPassword){
					alert('Two passwords cannot be the same.')
					return
				}
				this.axios({
					method: 'PUT',
					url: `${API_URL}/user/password`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					data: {
						old_password: this.oldPassword,
						new_password: this.newPassword
					}
				}).then((res) => {
					console.log(res)
					if(res.status === 200){
						alert(res.data.message + '\nPlease login again.')
						this.$store.commit('clearToken')
						location.reload()
						return
					}else{
						alert(res.data.message)
						this.clearForm()
					}
				}).catch((error) => {
					console.log(error.response.data.message)
					this.clearForm()
				})
			},
		}
	}
</script>

<style>
</style>

