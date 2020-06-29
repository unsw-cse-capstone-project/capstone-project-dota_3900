<template>
	<div class="modal" id="markReadForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Mark Book as Read<br />
					<span>Current book name: {{bookName}}</span>
				</div>
				<div class="row">
					<span>Set read date: Year: </span>
					<select style="margin-right: 0.5rem;" v-model="year">
						<option  v-for="(bias, index) in curYearTo1970" :key="index" :value="1969 + bias">{{1969 + bias}}</option>
					</select>
					<span>Month: </span>
					<select v-model="month">
						<option v-for="month in 12">{{month}}</option>
					</select>
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
		name: 'MarkReadForm',
		props: ['bookID', 'bookName'],
		data: function() {
			return{
				year: '',
				month: '',
			}
		},
		computed: {
			curYearTo1970: function(){
				let datetime = new Date();
				datetime.setTime((new Date()).getTime());
				let year = datetime.getFullYear()
				return year - 1969
			},
		},
		methods:{
			closeForm(){
				this.getcurYearMonth()
				let newCollectionForm = document.getElementById('markReadForm')
				newCollectionForm.style.display = 'none'
			},
			submit(){
				this.axios({
					method: 'post',
					url: `${API_URL}/book/read`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					params: {
						book_id: this.$route.query.id,
						year: this.year,
						month: this.month
					}
				}).then((res) => {
					alert("Mark as read successfully")
					location.reload()
				}).catch((error) => {
					console.log(error.response.data.message)
				})
			},
			getcurYearMonth(){
				let datetime = new Date();
				datetime.setTime((new Date()).getTime());
				this.year = datetime.getFullYear()
				this.month = datetime.getMonth() + 1
			},
		},
		created: function() {
			this.getcurYearMonth()
		}
	}
</script>

<style>
	@import url("../../assets/css/form.css");
</style>
