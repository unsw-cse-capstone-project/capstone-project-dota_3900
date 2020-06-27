<template>
	<div class="right animation-fadein-top delay_02s">
		<div class="collection-list">
			<ul>
				<li v-for="collection in sortedCollections" :key="collection.id">
					<div class="head">
						<div class="info">
							<span class="collection-title" @click="closeBookList(collection.id)">{{ collection.name }}</span>
							<div class="status">
								<span>Books: {{ collection.books.length }}</span>
								<span>Finished: {{ countReadBooks(collection.books) }}</span>
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
											<img src="../../../public/icon/plus.png" title="Add to my collection" v-if="!isMyDashboard() && $store.state.token" @click="openCollectionAddBookForm(book.book_id, book.title)">
											<img src="../../../public/icon/minus.png" title="Delete from this collection" v-if="isMyDashboard()" @click="removeBookFromCollection(collection.id, collection.name, book.book_id, book.title)" >
											<img src="../../../public/icon/move.png" title="Move to another collection" v-if="isMyDashboard()" @click="openCollectionMoveBookForm(collection.id, book.book_id, book.title)">
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
					<router-link v-for="recentBook in recentlyAddedBooks" :key="recentBook.book_id" :to="{name: 'Book', query: {id: recentBook.book_id}}">
						<div class="book">
							<span>{{timeStamp2datetime(recentBook.latest)}}</span>
							<img :src="recentBook.book_cover_url">
							<span><b>{{recentBook.title}}</b></span>
						</div>
					</router-link>
				</div>
			</div>

		</div>
		<NewCollectionForm></NewCollectionForm>
		<ModifyCollectionNameForm :collectionID="collectionID2Modify" :collectionName="collectionName2Modify"></ModifyCollectionNameForm>
		<CollectionMoveBookForm :myAccountID="myAccount.user_id" :toMoveBookID="toMoveBookID" :toMoveBookName="toMoveBookName" :curCollectionID="curCollectionID"></CollectionMoveBookForm>
		<AddBookForm :myAccountID="myAccount.user_id" :toMoveBookID="toAddBookID" :toMoveBookName="toAddBookName"></AddBookForm>
	</div>
</template>

<script>
	import API_URL from '../../serviceAPI.config.js'
	import NewCollectionForm from '../../components/forms/NewCollectionForm.vue'
	import ModifyCollectionNameForm from '../../components/forms/ModifyCollectionNameForm.vue'
	import CollectionMoveBookForm from '../forms/CollectionMoveBookForm.vue'
	import AddBookForm from '../forms/AddBookForm.vue'
	
	export default {
		name: 'UserCollection',
		props: ['account', 'myAccount'],
		data: function() {
			return {
				collections: [],
				collectionName2Modify: '',
				collectionID2Modify: '',
				recentlyAddedBooks: [],
				
				toMoveBookID: '',
				toMoveBookName: '',
				curCollectionID: '',
				
				toAddBookID: '',
				toAddBookName: '',
			}
		},
		computed: {
			sortedCollections: function() {
				let collections = this.collections
				collections.forEach(function(collection) {
					collection.books = collection.books.sort(function(book1, book2) {
						return book2.collect_datetime - book1.collect_datetime
					})
				})
				return collections
			}
		},
		components: {
			NewCollectionForm,
			ModifyCollectionNameForm,
			CollectionMoveBookForm,
			AddBookForm,
		},
		methods: {
			countReadBooks(books){
				let count = 0
				for(let i = 0; i < books.length; i++){
					if(books[i].finish_datetime){
						count++
					}
				}
				return count
			},
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
					console.log(error.response.data.message)
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
				if (hour < 10) hour = '0' + hour
				if (minute < 10) minute = '0' + minute
				if (second < 10) second = '0' + second
				return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second
			},
			closeBookList(collectionID) {
				let bookList = document.getElementById('collection' + collectionID)
				if (bookList.style.height !== "auto") {
					bookList.style.height = "auto";
					bookList.style.top = "0rem";
					bookList.style.opacity = "1";
				} else {
					bookList.style.height = "0rem";
					bookList.style.top = "-1.25rem";
					bookList.style.opacity = "0";
				}
			},
			openNewCollectionForm() {
				let newCollectionForm = document.getElementById('newCollectionForm')
				newCollectionForm.style.display = 'block'
			},
			openModifyCollectionNameForm(collectionID, collectionName) {
				let modifyCollectionNameForm = document.getElementById('modifyCollectionNameForm')
				this.collectionID2Modify = collectionID
				this.collectionName2Modify = collectionName
				modifyCollectionNameForm.style.display = 'block'
			},
			deleteCollection(collectionID, collectionName) {
				if (confirm(`Are you sure to delete the collection: ${collectionName}\nYou cannot undo this operation.`)) {
					this.axios.delete(`${API_URL}/collection?collection_id=${collectionID}`, {
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						}
					}).then((res) => {
						alert(res.data.message)
						location.reload()
					}).catch((error) => {
						console.log(error.response.data.message)
						this.getCollections()
						this.getRecentlyAddedBooks()
					})

				}
			},
			getRecentlyAddedBooks() {
				let userID = this.$route.query.id
				this.axios({
					method: 'GET',
					url: `${API_URL}/collection/recently_added`,
					params: {
						user_id: userID,
					},
				}).then((res) => {
					this.recentlyAddedBooks = res.data.books
				}).catch((error) => {
					console.log(error.response.data.message)
				})
			},
			removeBookFromCollection(collectionID, CollectionName, bookID, bookName){
				if(confirm(`Are you sure to remove \'${bookName}\' from \'${CollectionName}\' collection?`)){
					this.axios({
						method: 'DELETE',
						url: `${API_URL}/collection/books`,
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						},
						params: {
							collection_id: collectionID,
							book_id: bookID,
						},
					}).then((res) => {
						alert(res.data.message)
						this.getCollections()
						this.getRecentlyAddedBooks()
					}).catch((error) => {
						console.log(error.response.data.message)
						this.getCollections()
						this.getRecentlyAddedBooks()
					})
				}
			},
			openCollectionMoveBookForm(curCollectionID, bookID, bookName){
				this.toMoveBookID = bookID
				this.toMoveBookName = bookName
				this.curCollectionID = curCollectionID
				let collectionMoveBookForm = document.getElementById('collectionMoveBookForm')
				collectionMoveBookForm.style.display = 'block'
			},
			openCollectionAddBookForm(bookID, bookName){
				this.toAddBookID = bookID
				this.toAddBookName = bookName
				let collectionAddBookForm = document.getElementById('addBookForm')
				collectionAddBookForm.style.display = 'block'
			}
		},
		mounted: function() {
			this.getCollections()
			this.getRecentlyAddedBooks()
		},
	}
</script>

<style scoped>
	@import url("../../assets/css/user_collection.css");
</style>
