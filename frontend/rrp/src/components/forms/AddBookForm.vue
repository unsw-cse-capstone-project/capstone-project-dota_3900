<template>
	<div class="modal" id="addBookForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Add Book to Collection<br />
					<span>Current book name: {{toMoveBookName}}</span>
				</div>
				<div class="row">
					<span>Add to Collection: </span>
					<select v-model="toMoveCollectionID">
						<option value="">Choose collection</option>
						<option v-for="collection in myCollections" :key="collection.id" :value="collection.id">{{collection.name}}</option>
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
		name: 'AddBookForm',
		props: ['toMoveBookName', 'myAccountID', 'toMoveBookID'],
		data: function() {
			return{
				toMoveCollectionID: '',
				myCollections:[],
			}
		},
		methods:{
			closeForm(){
				let newCollectionForm = document.getElementById('addBookForm')
				newCollectionForm.style.display = 'none'
			},
			clearForm(){
				this.toMoveCollectionID = '',
				this.myCollections = []
			},
			submit(){
				if(this.toMoveCollectionID === ""){
					alert('Please select a collection')
					return
				}		
				this.axios({
					method: 'POST',
					url: `${API_URL}/collection/books`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					params: {
						collection_id: this.toMoveCollectionID,
						book_id: this.toMoveBookID,
					},
				}).then((res) => {
					alert(res.data.message)
					this.clearForm()
					this.closeForm()
				}).catch((error) => {
					alert(error.response.data.message)
				})
			},
			getMyCollections(){
				this.axios({
					method: 'get',
					url: `${API_URL}/collection`,
					params: { user_id: this.myAccountID }
				}).then((res) => {
					this.myCollections = res.data.Collections // id, name
				}).catch((error) => {
					console.log(error.response.data.message)
					this.clearForm()
				})
			},
		},
		watch: {
			myAccountID: function(){
				this.getMyCollections()
			},
			toMoveBookID: function(){
				this.getMyCollections()
			}
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/form.css");
</style>