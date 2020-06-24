<template>
	<div class="root">
		<Header ref="topbar"></Header>

		<!-- 404 page if there is no book_id in query -->
		<main v-if="pageNotFound">
			<NotFound></NotFound>
		</main>

		<main v-else>
			<div class="user-dashboard">
				<div class="top">
					<div class="title" v-if="isMyDashboard()">
						My dashboard - {{ account.username }}
					</div>
					<div class="title" v-else>
						User page - {{ account.username }}
					</div>
					<button class="btn-default btn-style-white animation-fadein-top delay_04s" v-if="isMyDashboard()">New Collection</button>

				</div>
				<div class="content">
					<div class="left">
						<ul>
							<li class="selected">
								<img src="../../public/icon/Collection.png">
								<span>Collections</span>
								<div>2</div>
							</li>
							<li>
								<img src="../../public/icon/goal.png">
								<span>Monthly Goal</span>
								<div>1</div>
							</li>
							<li>
								<img src="../../public/icon/already-read.png">
								<span>Read History</span>
								<div>11</div>
							</li>
							<li>
								<img src="../../public/icon/my-reviews.png">
								<span>My Reviews</span>
								<div>2</div>
							</li>
						</ul>
						<ul v-if="isMyDashboard()">
							<li>
								<img src="../../public/icon/modify-email.png">
								<span>Modify Email</span>
							</li>
							<li>
								<img src="../../public/icon/modify-password.png">
								<span>Update Password</span>
							</li>
						</ul>
					</div>

					<div class="right animation-fadein-top delay_02s">
						<div class="collection-list">
							<ul>
								<li v-for="collection in collections" :key="collection.id">
									<div class="head">
										<div class="info">
											<span>{{ collection.name }}</span>
											<div class="status">
												<span>Books: {{ collection.book_num }}</span>
												<span>Finished: {{ collection.finished_num }}</span>
												<span>creation-time: {{ timeStamp2datetime(collection.creation_time) }}</span>
											</div>
										</div>
										<div class="operation">
											<img src="../../public/icon/edit.png" title="Edit collection name" v-if="isMyDashboard()">
											<img src="../../public/icon/delete.png" title="Delete collection" v-if="isMyDashboard()">
											<img src="../../public/icon/copy.png" title="Copy collection">
											<img src="../../public/icon/open.png" title="Open collection" @click="closeBookList(collection.id)">
										</div>
									</div>
									<div class="book-list" :id="'collection' + collection.id" >
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
															<img src="../../public/icon/plus.png" title="Add to my collection" v-if="!isMyDashboard()">
															<img src="../../public/icon/minus.png" title="Delete from this collection" v-if="isMyDashboard()">
															<img src="../../public/icon/move.png" title="Move to another collection" v-if="isMyDashboard()">
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
											<img src="../../public/icon/hint.png">
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
					</div>
				</div>
			</div>
		</main>

		<Footer></Footer>
	</div>
</template>

<script>
	import API_URL from '../serviceAPI.config.js'
	import Header from '../components/common/Header.vue'
	import Footer from '../components/common/Footer.vue'
	import NotFound from '../components/common/NotFound.vue'
	export default {
		name: 'UserCollection',
		data: function() {
			return {
				myAccount: {
					user_id: '',
					username: '',
					email: '',
					admin: ''
				},
				account: {
					user_id: '',
					username: '',
					email: '',
					admin: ''
				},
				pageNotFound: false,
				collections: [],
			}
		},
		computed: {
			sortedCollection: function(){
				return this.collections.forEach(function(collection){
					collection.books.sort(function(book1, book2){
						return parseFloat(book2.collect_datetime)- parseFloat(book1.collect_datetime)
					})
				})
			}
		},
		components: {
			Header,
			Footer,
			NotFound
		},
		methods: {
			getAccountsInfo() {
				// if there is no user id in query -> 404
				if (this.$route.query.id === undefined) {
					this.pageNotFound = true
					return
				}
				// get page owner's info
				let userID = this.$route.query.id
				this.axios({
					method: 'get',
					url: `${API_URL}/user/${userID}/detail`,
				}).then((res) => {
					this.account = res.data
				}).catch((error) => {
					alert(error.response.data.message)
					this.pageNotFound = true
					return
				})
				// get my info (if exists)
				if (this.$store.state.token) {
					this.axios({
						method: 'get',
						url: `${API_URL}/user/detail`,
						headers: {
							'Content-Type': 'application/json',
							'AUTH-TOKEN': this.$store.state.token
						}
					}).then((res) => {
						this.myAccount = res.data
					}).catch((error) => {
						this.pageNotFound = true
						return
					})
				}
			},
			isMyDashboard() {
				return this.myAccount.user_id === this.account.user_id ? true : false
			},
			getCollections() {
				let userID = this.$route.query.id
				this.axios.get(`${API_URL}/collection?user_id=${userID}`).then((res) => {
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
					collections.forEach(function(collection){
						collection.books = collection.books.sort(function(book1, book2){
							return book1.collect_datetime.parseFloat() - book2.collect_datetime.parseFloat()
						})
					})
					this.collections = collections
				}).catch((error) => {
					alert(error.response.data.message)
				})
			},
			getCollectionBooks(collectionID) {
				this.axios.get(`${API_URL}/collection/books?collection_id=${collectionID}`).then((res) => {
					console.log(res)
					return res
				}).catch((error) => {
					alert(error)
				})
			},
			timeStamp2datetime(timeStamp) {
				var datetime = new Date();
				datetime.setTime(timeStamp);
				var year = datetime.getFullYear();
				var month = datetime.getMonth() + 1;
				var date = datetime.getDate();
				var hour = datetime.getHours();
				var minute = datetime.getMinutes();
				var second = datetime.getSeconds();
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
			}
		},
		mounted: function() {
			this.getAccountsInfo()
			this.getCollections()
		},
	}
</script>

<style scoped>
	@import url("../assets/css/dashboard_common.css");
	@import url("../assets/css/user_collection.css");
</style>
