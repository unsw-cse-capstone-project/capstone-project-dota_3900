<template>
	<div class="modal" id="updateEmailForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Update Email<br />
					<span>Current email: {{currentEmail}}</span>
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
		name: 'UpdateEmailForm',
		props:['currentEmail'],
		data: function() {
			return{
				newEmail: ''
			}
		},
		methods:{
			closeForm(){
				let newCollectionForm = document.getElementById('updateEmailForm')
				newCollectionForm.style.display = 'none'
				this.clearForm()
			},
			clearForm(){
				this.newEmail = ''
			},
			submit(){
				if(this.newEmail === ''){
					alert('New email address cannot be an empty string.')
					return
				}
				if(!this.validateEmail(this.newEmail)){
					alert('Invalid Email address.')
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
						email: this.newEmail
					}
				}).then((res) => {
					alert(res.data.message)
					location.reload()
				}).catch((error) => {
					console.log(error.response.data.message)
					this.clearForm()
				})
			},
			validateEmail(email){
				var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
				return re.test(String(email).toLowerCase())
			}
		}
	}
</script>

<style>
</style>
