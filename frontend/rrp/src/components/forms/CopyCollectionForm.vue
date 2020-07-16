<template>
	<div class="modal" id="copyCollectionForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Copy Collection
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
		name: 'CopyCollectionForm',
		props: ['collection_id'],
		data: function() {
			return{
				collectionName: ''
			}
		},
		methods:{
			closeForm(){
				let newCollectionForm = document.getElementById('copyCollectionForm')
				newCollectionForm.style.display = 'none'
				this.clearForm()
			},
			clearForm(){
				this.collectionName = ''
			},
			submit(){
				if(this.collectionName === ''){
					alert('Please input a collection name.')
					return
				}
				this.axios({
					method: 'GET',
					url: `${API_URL}/collection/copy`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					params: {
						new_collection_name: this.collectionName,
						collection_id: this.collection_id
					}
				}).then((res) => {
					alert(res.data.message)
					this.clearForm()
					this.closeForm()
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