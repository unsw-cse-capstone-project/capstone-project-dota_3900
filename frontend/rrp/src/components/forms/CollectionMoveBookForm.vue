<template>
	<div class="modal" id="collectionMoveBookForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Move Book to Another Collection<br />
					<span>Current book name: {{toMoveBookName}}</span>
				</div>
				<div class="row">
					<span>Move to Collection: </span>
					<select v-model="toMoveCollectionID">
						<option value="">Choose collection</option>
						<option v-for="collection in myCollections" :key="collection.id" :value="collection.id" v-if="collection.id !== curCollectionID">{{collection.name}}</option>
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
		name: 'CollectionMoveBookForm',
		props: ['toMoveBookName', 'myAccountID', 'toMoveBookID', 'curCollectionID'],
		data: function() {
			return{
				toMoveCollectionID: '',
				myCollections:[],
			}
		},
		methods:{
			closeForm(){
				let newCollectionForm = document.getElementById('collectionMoveBookForm')
				newCollectionForm.style.display = 'none'
			},
			clearForm(){
				this.toMoveCollectionID = ''
			},
			submit(){
				if(this.toMoveCollectionID === ""){
					return
				}
				this.axios({
					method: 'put',
					url: `${API_URL}/collection/books`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					params: {
						old_collection_id: this.curCollectionID,
						new_collection_id: this.toMoveCollectionID,
						book_id: this.toMoveBookID,
					},
				}).then((res) => {
					alert(res.data.message)
					this.clearForm()
					this.closeForm()
				}).catch((error) => {
					alert(error.response.data.message)
				})
				this.$parent.getCollections()
				this.$parent.getRecentlyAddedBooks()
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