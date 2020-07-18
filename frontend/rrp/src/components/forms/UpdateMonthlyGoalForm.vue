<template>
	<div class="modal" id="updateMonthlyGoalForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Set / Update Monthly goal
				</div>
				<div class="row">
					<span>New monthly goal</span>
					<input type="text" placeholder="Enter the number of books you want to read per month." v-model="newMonthlyGoal" required>
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
		name: 'UpdateMonthlyGoalForm',
		data: function() {
			return{
				newMonthlyGoal: ''
			}
		},
		methods:{
			closeForm(){
				let newCollectionForm = document.getElementById('updateMonthlyGoalForm')
				newCollectionForm.style.display = 'none'
				this.clearForm()
			},
			clearForm(){
				this.newMonthlyGoal = ''
			},
			submit(){
				if(this.newMonthlyGoal === ''){
					alert('Please fill in all blanks.')
					return
				}
				if(this.newMonthlyGoal >= 0){
					this.axios({
						method: 'POST',
						url: `${API_URL}/goal`,
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						},
						params: {
							goal: parseInt(this.newMonthlyGoal)
						}
					}).then((res) => {
						alert('Update monthly goal successfully.')
						this.closeForm()
						location.reload()
					}).catch((error) => {
						alert(error.response.data.message)
						this.clearForm()
					})
				}else{
					alert('Invalid monthly goal.\nMonthly goal must be a non-negative integer.')
				}
			}
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/form.css");
</style>