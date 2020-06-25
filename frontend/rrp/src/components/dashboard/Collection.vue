<template>
	<div class="right animation-fadein-top delay_02s">
		<div class="collection-list">
			<ul>
				<li v-for="collection in sortedCollections" :key="collection.id">
					<div class="head">
						<div class="info">
							<span class="collection-title" @click="closeBookList(collection.id)">{{ collection.name }}</span>
							<div class="status">
								<span>Books: {{ collection.book_num }}</span>
								<span>Finished: {{ collection.finished_num }}</span>
								<span v-if="collection.name !== 'Main collection'">Creation time: {{ timeStamp2datetime(collection.creation_time) }}</span>
							</div>
						</div>
						<div class="operation">
							<img src="../../../public/icon/edit.png" title="Edit collection name" v-if="isMyDashboard() && collection.name !== 'Main collection'"
							 @click="openModifyCollectionNameForm(collection.id, collection.name)">
							<img src="../../../public/icon/delete.png" title="Delete collection" v-if="isMyDashboard() && collection.name !== 'Main collection'"
							 @click="deleteCollection(collection.id, collection.name)">
							<img src="../../../public/icon/copy.png" title="Copy collection" v-if="$store.state.token">
							<img src="../../../public/icon/open.png" title="Open collection" @click="closeBookList(collection.id)">
						</div>
					</div>
					<div class="book-list" :id="'collection' + collection.id">
						<div class="book" v-for="book in collection.books" :key="book.collect_datetime">
							<div class="info">
								<router-link :to="{name: 'Book', query: {id: book.book_id}}">
									<img :src="book.book_cover_url">
								</router-link>
								<div class="book-detail">
									<div class="title-operation">
										<router-link :to="{name: 'Book', query: {id: book.book_id}}">
											<span><b>{{book.title}}</b></span>
										</router-link>
										<div class="operation">
											<img src="../../../public/icon/plus.png" title="Add to my collection" v-if="!isMyDashboard()">
											<img src="../../../public/icon/minus.png" title="Delete from this collection" v-if="isMyDashboard()">
											<img src="../../../public/icon/move.png" title="Move to another collection" v-if="isMyDashboard()">
											<button class="btn-default btn-style-green" v-if="isMyDashboard() && book.finish_datetime !== undefined">Finished</button>
											<button class="btn-default btn-style-wheat" v-if="isMyDashboard() && book.finish_datetime === undefined">Unfinished</button>
										</div>
									</div>
									<span><b>Author: </b>{{book.authors}}</span>
									<span><b>Description: </b>{{book.description}}</span>
									<span><b>Publisher & publication date: </b>{{book.publisher}} ({{book.published_date}})</span>
									<span><b>Category: </b>{{book.categories}}</span>
									<span><b>Collect date: </b>{{timeStamp2datetime(book.collect_datetime)}}</span>
									<span v-if="book.finish_datetime !== undefined"><b>Date read: </b>{{timeStamp2datetime(book.finish_datetime)}}</span>
								</div>
							</div>
						</div>
						<div class="no-book" v-if="collection.book_num === 0">
							<img src="../../../public/icon/hint.png">
							<span>Oops, there is no book yet!</span>
						</div>
						<div class="close-collection" @click="closeBookList(collection.id)">
							<span>Close collection</span>
						</div>
					</div>
				</li>
			</ul>

			<div class="recently-added-list">
				<div class="title">
					Recently Added Books
				</div>
				<div class="books">
					<div class="book">
						<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
						<span><b>Attack on Titan - Volume 14</b></span>
					</div>
				</div>
			</div>
		</div>
		<NewCollectionForm></NewCollectionForm>
		<ModifyCollectionNameForm :collectionID="collectionID2Modify" :collectionName="collectionName2Modify"></ModifyCollectionNameForm>
	</div>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	import NewCollectionForm from '../../components/forms/NewCollectionForm.vue'
	import ModifyCollectionNameForm from '../../components/forms/ModifyCollectionNameForm.vue'
	export default {
		name: 'UserCollection',
		props: ['account', 'myAccount'],
		data: function() {
			return {
				collections: [],
				collectionName2Modify: '',
				collectionID2Modify: '',
			}
		},
		computed:{
			sortedCollections: function(){
				let collections = this.collections.sort(function(collection1, collection2){
					if(collection2.name === 'Main collection'){
						return 1
					}
					else{
						return collection2.creation_time - collection1.creation_time
					}
				})
				collections.forEach(function(collection){
					collection.books = collection.books.sort(function(book1, book2){
						return book2.collect_datetime - book1.collect_datetime
					})
				})
				return collections
			}
		},
		components: {
			NewCollectionForm,
			ModifyCollectionNameForm,
		},
		methods: {
			isMyDashboard() {
				return this.myAccount.user_id === this.account.user_id ? true : false
			},
			
			getCollections() {
				let userID = this.$route.query.id
				this.axios({
					method: 'GET',
					url: `${API_URL}/collection`,
					params: {
						user_id: userID
					},
				}).then((res) => {
					let collections = res.data.Collections
					for (let i = 0; i < collections.length; i++) {
						let collectionID = collections[i].id
						collections[i].books = []
						this.axios.get(`${API_URL}/collection/books?collection_id=${collectionID}`).then((res) => {
							let bookIDs = res.data.books
							for (let j = 0; j < bookIDs.length; j++) {
								let bookID = bookIDs[j].book_id
								this.axios.get(`${API_URL}/book/${bookID}/detail`).then((res) => {
									let book = res.data
									book.categories = book.categories.replace(/\[\'/, '').replace(/\'\]/, '')
									book.authors = book.authors.replace(/\[\'/, '').replace(/\'\]/, '').split("', '").join(", ")
									book.collect_datetime = bookIDs[j].collect_time
									book.finish_datetime = bookIDs[j].finish_time
									collections[i].books.push(book)
								})
							}
						})
					}
					this.collections = collections
				}).catch((error) => {
					alert(error.response.data.message)
				})
			},
			timeStamp2datetime(timeStamp) {
				let datetime = new Date();
				datetime.setTime(timeStamp);
				let year = datetime.getFullYear()
				let month = datetime.getMonth() + 1
				let date = datetime.getDate()
				let hour = datetime.getHours()
				let minute = datetime.getMinutes()
				let second = datetime.getSeconds()
				if(hour < 10) hour = '0' + hour
				if(minute < 10) minute = '0' + minute
				if(second < 10) second = '0' + second
				return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second
			},
			closeBookList(collectionID){
				let bookList = document.getElementById('collection' + collectionID)
				if (bookList.style.height !== "auto") {
					bookList.style.height = "auto";
					bookList.style.top = "0rem";
					bookList.style.opacity= "1";
				} else {
					bookList.style.height = "0rem";
					bookList.style.top = "-1.25rem";
					bookList.style.opacity= "0";
				}
			},
			openNewCollectionForm(){
				let newCollectionForm = document.getElementById('newCollectionForm')
				newCollectionForm.style.display = 'block'
			},
			openModifyCollectionNameForm(collectionID, collectionName){
				let modifyCollectionNameForm = document.getElementById('modifyCollectionNameForm')
				this.collectionID2Modify = collectionID
				this.collectionName2Modify = collectionName
				modifyCollectionNameForm.style.display = 'block'
			},
			deleteCollection(collectionID, collectionName){
				if(confirm(`Are you sure to delete the collection: ${collectionName}\nYou cannot undo this operation.`)){
					this.axios.delete(`${API_URL}/collection?collection_id=${collectionID}`, {headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						}}).then((res) => {
						alert(res.data.message)
						this.getCollections()
					}).catch((error) => {
						alert(error.response.data.message)
					})
				}
			}
		},
		mounted: function() {
			this.getCollections()
		},
	}
</script>

<style scoped>
		@import url("../../assets/css/user_collection.css");
</style>
