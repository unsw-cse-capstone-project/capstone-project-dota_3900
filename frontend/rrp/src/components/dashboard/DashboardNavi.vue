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
			<li>
				<img src="../../../public/icon/modify-email.png">
				<span>Modify Email</span>
			</li>
			<li>
				<img src="../../../public/icon/modify-password.png">
				<span>Update Password</span>
			</li>
		</ul>
	</div>
</template>

<script>
	export default {
		name: 'DashboardNavi',
		props: ['account', 'myAccount'],
		data: function() {
			return {
			}
		},
		methods: {
			isMyDashboard() {
				return this.myAccount.user_id === this.account.user_id ? true : false
			},
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/dashboard_common.css");
</style>
