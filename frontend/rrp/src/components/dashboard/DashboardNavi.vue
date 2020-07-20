<template>
	<div class="left">
		<ul>
			<router-link :to="{name: 'UserCollection', query: {id: $route.query.id}}">
				<li :class="{selected: $route.name === 'UserCollection'}">
					<img src="../../../public/icon/Collection.png">
					<span>Collections</span>
					<div>{{tags.collections_num}}</div>
				</li>
			</router-link>
			<router-link :to="{name: 'UserMonthlyGoal', query: {id: $route.query.id}}">
				<li :class="{selected: $route.name === 'UserMonthlyGoal'}">
					<img src="../../../public/icon/goal.png">
					<span>Monthly Goal</span>
					<div style="font-size: 0.6875rem;" v-if="parseInt(tags.MonthlyGoal_num) > 0">{{parseInt(tags.MonthlyGoal_num)}}%</div>
					<div style="font-size: 0.6875rem;" v-else>-- %</div>
				</li>
			</router-link>
			<router-link :to="{name: 'UserReadHistory', query: {id: $route.query.id}}">
				<li :class="{selected: $route.name === 'UserReadHistory'}">
					<img src="../../../public/icon/already-read.png">
					<span>Read History</span>
					<div>{{tags.ReadHistory_num}}</div>
				</li>
			</router-link>
			<router-link :to="{name: 'UserReviews', query: {id: $route.query.id}}">
				<li :class="{selected: $route.name === 'UserReviews'}">
					<img src="../../../public/icon/my-reviews.png">
					<span>Reviews</span>
					<div>{{tags.MyReview_num}}</div>
				</li>
			</router-link>
		</ul>
		<ul v-if="isMyDashboard()" class="animation-fadein-top delay_06s">
			<li @click="openUpdateEmailForm()">
				<img src="../../../public/icon/modify-email.png">
				<span>Update Email</span>
			</li>
			<li @click="openUpdatePasswordForm()">
				<img src="../../../public/icon/modify-password.png">
				<span>Update Password</span>
			</li>
		</ul>
		
		<UpdateEmailForm :currentEmail="myAccount.email"></UpdateEmailForm>
		<UpdatePasswordForm></UpdatePasswordForm>	
	</div>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	import UpdateEmailForm from '../forms/UpdateEmailForm.vue'
	import UpdatePasswordForm from '../forms/UpdatePasswordForm.vue'
	export default {
		name: 'DashboardNavi',
		props: ['account', 'myAccount'],
		data: function() {
			return {
				tags: {
				  collections_num: 0,
				  ReadHistory_num: 0,
				  MyReview_num: 0
				}
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
			getTags(){
				let userID = this.$route.query.id
				this.axios.get(`${API_URL}/user/${userID}/dashboard_tags`).then((res) => {
					this.tags = res.data
				}).catch((error) => {
					console.log(error.response.data.message)
					this.clearForm()
				})
			}
		},
		mounted: function(){
			this.getTags()
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/dashboard_common.css");
</style>
