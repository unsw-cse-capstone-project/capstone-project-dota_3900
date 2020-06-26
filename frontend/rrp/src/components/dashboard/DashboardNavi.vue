<template>
	<div class="left">
		<ul>
			<li :class="{selected: $route.name === 'UserCollection'}">
				<img src="../../../public/icon/Collection.png">
				<span>Collections</span>
				<div>2</div>
			</li>
			<li>
				<img src="../../../public/icon/goal.png">
				<span>Monthly Goal</span>
				<div>1</div>
			</li>
			<li>
				<img src="../../../public/icon/already-read.png">
				<span>Read History</span>
				<div>11</div>
			</li>
			<li>
				<img src="../../../public/icon/my-reviews.png">
				<span>My Reviews</span>
				<div>2</div>
			</li>
		</ul>
		<ul v-if="isMyDashboard()">
			<li @click="openUpdateEmailForm()">
				<img src="../../../public/icon/modify-email.png">
				<span>Update Email</span>
			</li>
			<li @click="openUpdatePasswordForm()">
				<img src="../../../public/icon/modify-password.png">
				<span>Update Password</span>
			</li>
			
			<UpdateEmailForm :currentEmail="myAccount.email"></UpdateEmailForm>
			<UpdatePasswordForm></UpdatePasswordForm>
		</ul>
		
		
	</div>
</template>

<script>
	import UpdateEmailForm from '../forms/UpdateEmailForm.vue'
	import UpdatePasswordForm from '../forms/UpdatePasswordForm.vue'
	export default {
		name: 'DashboardNavi',
		props: ['account', 'myAccount'],
		data: function() {
			return {
			}
		},
		components:{
			UpdateEmailForm,
			UpdatePasswordForm,
		},
		methods: {
			isMyDashboard() {
				return this.myAccount.user_id === this.account.user_id ? true : false
			},
			openUpdateEmailForm(){
				let updateEmailForm = document.getElementById('updateEmailForm')
				updateEmailForm.style.display = 'block'
			},
			openUpdatePasswordForm(){
				let updateEmailForm = document.getElementById('updatePasswordForm')
				updateEmailForm.style.display = 'block'
			},
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/dashboard_common.css");
</style>
