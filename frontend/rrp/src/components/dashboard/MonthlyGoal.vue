<template>
	<div class="right animation-fadein-top delay_02s">
		<div class="monthly-goal">
			<div class="info-list">	
				<div class="info-box">
					<div class="title">
							This month, I want to read...
					</div>
					<div class="content">
						<img src="../../../public/icon/target.png" >
						<div class="number">
							<span v-if="info.target !== 0">{{info.target}}</span>
							<span v-else>--</span>
							<span style="margin-left: 0.3125rem;">Book(s)</span>
						</div>
					</div>
				</div>
				
				<div class="info-box">
					<div class="title">
							I finished ... of this monthly goal
					</div>
					<div class="content">
						<img src="../../../public/icon/books.png" >
						<div class="number">
							<span v-if="info.target !== 0">{{parseInt(info.finish_ratio)}}</span>
							<span v-if="info.target === 0">--</span>
							<span style="margin-left: 0.3125rem;">%</span>
						</div>
					</div>
				</div>
			
				
				<div class="info-box">
					<div class="title">
							I have reached monthly goal for...
					</div>
					<div class="content">
						<img src="../../../public/icon/success.png" >
						<div class="number">
							<span>{{info.reach_goal_num}}</span>
							<span style="margin-left: 0.3125rem;">Time(s)</span>
						</div>
					</div>
				</div>
			</div>
			
			<ul>
				<li>
					<div class="year-month">
						<div class="year">
							2020
						</div>
						<div class="month">
							Jul
						</div>
					</div>
					<div class="num_books">
						<img src="../../../public/icon/copy.png" >
						<span>{{info.finish_num}}</span>
					</div>	
					<div v-if="info.finish_book.length === 0" class="no-book">
						<div>
							<p>No book read in this month.</p>
							<p>You can mark a book as read by search a book.</p>
						</div>
					</div>
					<div v-else class="books">
						<router-link  v-for="book in info.finish_book" :key="book.book_id" :to="{name: 'Book', query: {id: book.book_id}}">
							<div class="book">
								<span><b>Fin: </b>{{timeStamp2yearMonthDay(book.finish_time)}}</span>
								<img :src="book.book_cover_url" >
								<span><b>{{book.book_title}}</b></span>
							</div>
						</router-link>
					</div>
				</li>
			</ul>
		</div>
		<UpdateMonthlyGoalForm></UpdateMonthlyGoalForm>
	</div>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	import UpdateMonthlyGoalForm from '../forms/UpdateMonthlyGoalForm.vue'
	export default {
		name: 'UserMonthlyGoal',
		data: function(){
			return {
				info: {
					  target: 0,
					  finish_ratio: 0,
					  finish_num: 0,
					  reach_goal_num: 0,
						finish_book: [],
				},
			}
		},
		components:{
			UpdateMonthlyGoalForm,
		},
		methods: {
			// get all monthly_goal infos for current dashboard belonger
			getInfo(){
				this.axios({
					method: 'get',
					url: `${API_URL}/goal`,
					params: {
						user_id: this.$route.query.id
					}
				}).then((res) => {
					this.info = res.data
				}).catch((error) => {
					console.log(error.response.data.message)
				})
			},
			
			// translate timeStamp to year-month-day format
			timeStamp2yearMonthDay(timeStamp) {
				let datetime = new Date();
				datetime.setTime(timeStamp);
				let year = datetime.getFullYear()
				let month = datetime.getMonth() + 1
				let date = datetime.getDate()
				return year + "-" + month + "-" + date
			},
			
			openUpdateMonthlyGoalForm(){
				let updateMonthlyGoalForm = document.getElementById('updateMonthlyGoalForm')
				updateMonthlyGoalForm.style.display = 'block'
			}
		},
		mounted: function(){
			this.getInfo()
		}
	}
</script>

<style>
	@import url("../../assets/css/user_monthly_goal.css");
</style>
