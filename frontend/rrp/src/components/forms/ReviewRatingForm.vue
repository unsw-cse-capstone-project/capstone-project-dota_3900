<template>
	<div class="modal" id="reviewRatingForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Book Review<br />
					<span>Book name: {{bookName}}</span>
				</div>
				<div class="row">
					<span>Review: </span><br />
					<textarea type="text" placeholder="Input your review" v-model="review"></textarea>

				</div>
				<div class="row">
					<span>Rating: </span>
					<select v-model="rating">
						<option value="">please rating</option>
						<option :value="1">1 - Bad</option>
						<option :value="2">2 - Mediocre</option>
						<option :value="3">3 - Good</option>
						<option :value="4">4 - Great</option>
						<option :value="5">5 - Masterpiece</option>
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
		props: ['method', 'bookID', 'bookName'],
		data: function() {
			return {
				rating: '',
				review: '',
			}
		},
		methods: {
			closeForm() {
				this.clearForm()
				let newCollectionForm = document.getElementById('reviewRatingForm')
				newCollectionForm.style.display = 'none'
			},
			clearForm() {
				this.rating = ''
				this.review = ''
			},
			submit() {
				if(this.rating === '' || this.review === ''){
					alert('Review and rating cannot be empty.')
					return
				}
				this.axios({
					method: this.method,
					url: `${API_URL}/book/review`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					data: {
						"book_id": this.bookID,
						"rating": this.rating,
						"content": this.review
					}
				}).then((res) => {
					if (res.status === 200) {
						if(this.method.toLowerCase() === 'put'){
							alert('Update review and rating successfully.')
						}
						else{
							alert('Add review and rating successfully.')
						}
					}
					location.reload()
				}).catch((err) => {
					location.reload()
				})
			}
		}
	}
</script>

<style>
</style>
