<template>
	<div class="right animation-fadein-top delay_02s">
		<div class="already-read-list">
			<ul>
				<li v-if="!hasBookFlag">
					<div class="year-month">
						<div class="year">
							{{year}}
						</div>
						<div class="month">
							{{translateMonthToText(month)}}
						</div>
					</div>
					<div class="num_books">
						<img src="../../../public/icon/copy.png" >
						<span>0</span>
					</div>	
					<div class="no-book">
						<div>
							<p>No book read in this month.</p>
							<p>"Reading for wisdom like gymnastics to the body."</p>
							<p>-- Thomas Alva Edison (1847-1931)</p>
						</div>
					</div>
				</li>
				
				<li v-for="yearMonth in timeline">
					<div class="year-month">
						<div class="year">
							{{yearMonth.year}}
						</div>
						<div class="month">
							{{translateMonthToText(yearMonth.month)}}
						</div>
					</div>
					<div class="num_books">
						<img src="../../../public/icon/copy.png" >
						<span>{{yearMonth.books.length}} / -</span>
					</div>	
<!-- 					<div class="finish-goal">
						<img src="../../../public/icon/trues-active.png" title="You have reached monthly goal!" >
					</div> -->
						<div class="books">
							<router-link v-for="book in yearMonth.books" :key="book.book_id" :to="{name: 'Book', query: {id: book.book_id}}">
								<div class="book">
									<img :src="book.book_cover_url" >
									<span><b>{{book.book_title}}</b></span>
								</div>
							</router-link>
						</div>
				</li>
				
				<div class="start-decoration">
					<span>Start!</span>
				</div>
				
			</ul>
		</div>
	</div>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	export default {
		name: 'ReadHistory',
		props: ['account', 'myAccount'],
		data: function() {
			return {
				timeline: [],
				year: '',
				month: '',
				hasBookFlag: true,
			}
		},
		methods:{
			isMyDashboard() {
				return this.myAccount.user_id === this.account.user_id ? true : false
			},
			getReadHistory() {
				this.axios({
					method: 'get',
					url: `${API_URL}/collection/read_history`,
					params: { 
						user_id: this.$route.query.id
					}
				}).then((res) => {
					let books = res.data.books
					books = books.sort(function(book1, book2){
						return book2.finish_time - book1.finish_time
					})
					let timeline = []
					for(let i = 0; i < books.length; i++){
						books[i].finish_time = this.timeStamp2yearMonth(books[i].finish_time)
						let yearMonth = books[i].finish_time.split('-')
						let year = parseInt(yearMonth[0])
						let month = parseInt(yearMonth[1])
						if(timeline.length === 0 || timeline[timeline.length - 1].year !== year || timeline[timeline.length - 1].month !== month){
							timeline.push({
								year: parseInt(year), month: parseInt(month), books:[]
							})
						}
						timeline[timeline.length - 1].books.push(books[i])
					}
					this.timeline = timeline
					console.log(this.timeline)
					this.hasBookInCurMonth()
				}).catch((err) => {
					console.log(error.response.data.message)
				})
			},
			timeStamp2yearMonth(timeStamp) {
				let datetime = new Date();
				datetime.setTime(timeStamp);
				let year = datetime.getFullYear()
				let month = datetime.getMonth() + 1
				return year + "-" + month
			},
			hasBookInCurMonth(){
				let datetime = new Date();
				datetime.setTime((new Date()).getTime());
				let year = datetime.getFullYear()
				let month = datetime.getMonth() + 1
				console.log(this.timeline)
				if(this.timeline.length !== 0 && this.timeline[0].year === year && this.timeline[0].month === month){
					this.hasBookFlag = true
				}else{
					this.year = year
					this.month = month
					this.hasBookFlag = false
				}
				console.log(this.hasBookFlag)
			},
			translateMonthToText(month){
				let monthText = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
				return monthText[month - 1]
			}
		},
		mounted: function() {
			this.getReadHistory()
		}
	}
</script>

<style>
	@import url("../../assets/css/user_read_history.css");
</style>
