<template>
	<div class="modal" id="modifyCollectionNameForm">
		<form class="modal-content animation-fadein-top">
			<div class="container1">
				<div class="title">
					Modify Collection Name<br />
					<span>Current name: {{collectionName}}</span>
				</div>
				<div class="row">
					<span>New collection name:</span>
					<input type="text" placeholder="Enter new collection name" v-model="newName" required>
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
	import {mapMutations} from 'vuex'
	import API_URL from '../../serviceAPI.config.js'
	export default {
		name: 'ModifyCollectionNameForm',
		props: ['collectionID', 'collectionName'],
		data: function() {
			return{
				newName: ''
			}
		},
		methods:{
			...mapMutations(['updateToken']),
			closeForm(){
				let newCollectionForm = document.getElementById('modifyCollectionNameForm')
				newCollectionForm.style.display = 'none'
				this.clearForm()
			},
			clearForm(){
				this.newName = ''
			},
			submit(){
				if(this.newName === ''){
					alert('New collection name cannot be an empty string.')
				}
				this.axios({
					method: 'PUT',
					url: `${API_URL}/collection`,
					headers: {
						'Content-Type': 'application/json',
						'AUTH-TOKEN': this.$store.state.token
					},
					params: {
						collection_id: this.collectionID,
						new_name: this.newName
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