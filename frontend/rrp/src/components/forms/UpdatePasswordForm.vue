<template>
	<div class="modal" id="updatePasswordForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Update Password<br />
				</div>
				<div class="row">
					<span>New email address</span>
					<input type="text" placeholder="Enter new email address" v-model="newEmail" required>
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
				newPassword: ''
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
				if(this.newPassword === ''){
					alert('New email address cannot be an empty string.')
					return
				}
				this.axios({
					method: 'PUT',
					url: `${API_URL}/user/email`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					data: {
						password: this.newPassword
					}
				}).then((res) => {
					alert(res.data.message)
					location.reload()
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

