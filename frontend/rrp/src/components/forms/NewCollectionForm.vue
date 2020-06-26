<template>
	<div class="modal" id="newCollectionForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Create New Collection
				</div>
				<div class="row">
					<span>New collection name:</span>
					<input type="text" placeholder="Enter new collection name" v-model="collectionName" required>
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
		name: 'NewCollectionForm',
		data: function() {
			return{
				collectionName: ''
			}
		},
		methods:{
			closeForm(){
				let newCollectionForm = document.getElementById('newCollectionForm')
				newCollectionForm.style.display = 'none'
				this.clearForm()
			},
			clearForm(){
				this.collectionName = ''
			},
			submit(){
				if(this.collectionName === ''){
					alert('Collection name cannot be an empty string.')
				}
				this.axios({
					method: 'POST',
					url: `${API_URL}/collection`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					params: {
						collection_name: this.collectionName
					}
				}).then((res) => {
					alert(res.data.message)
					location.reload()
				}).catch((error) => {
					alert(error.response.data.message)
					this.clearForm()
				})
			}
		}
	}
</script>

<style scoped>
	@import url("../../assets/css/form.css");
</style>