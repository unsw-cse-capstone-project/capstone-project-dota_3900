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
						<ul>
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
								<li>
									<div class="head">
										<div class="info">
											<span>Main Collection</span>
											<div class="status">
												<span>Books: 5</span>
												<span>Finished: 2</span>
												<span>creation-time: 2020-02-02</span>
											</div>
										</div>
										<div class="operation">
											<img src="../../public/icon/edit.png" title="Edit collection name">
											<img src="../../public/icon/delete.png" title="Delete collection">
											<img src="../../public/icon/copy.png" title="Copy collection">
											<img src="../../public/icon/open.png" title="Open collection" id="open-book-list">
										</div>
									</div>
									<div class="book-list" id="main-collection-book-list">
										<div class="book">
											<div class="info">
												<img src="http://books.google.com/books/content?id=HjI0BgAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api">
												<div class="book-detail">
													<div class="title-operation">
														<span><b>Attack on Titan: Vol 13</b></span>
														<div class="operation">
															<img src="../../public/icon/plus.png" title="Add to my collection">
															<img src="../../public/icon/minus.png" title="Delete from this collection">
															<img src="../../public/icon/move.png" title="Move to another collection">
															<button class="btn-default btn-style-green">Finished</button>
														</div>
													</div>
													<span><b>Author: </b>Hajime Isayama</span>
													<span><b>Description: </b>NO SAFE PLACE LEFT At great cost to the Garrison and the Survey Corps,
														Commander Erwin has managed to recover Eren from the Titans who tried to carry him off. But during the
														battle, Eren manifested yet another power he doesn't understand. As Eren and Krista find new enemies,
														the Survey Corps faces threats from both inside and outside the walls. And what will happen to Ymir, now
														that she has decided to make herself the Titans' prize?</span>
													<span><b>Publisher & publication date: </b>Kodansha Comics (2014-07-11)</span>
													<span><b>Category: </b>Comic</span>
													<span><b>Collect date: </b>2020-06-11</span>
													<span><b>Date read: </b>2020-06-11</span>
												</div>
											</div>
										</div>
										<div class="close-collection" id="close-tab">
											<span>Close collection</span>
										</div>
									</div>
								</li>

								<li>
									<div class="head">
										<div class="info">
											<span>My Sci-fi Collection</span>
											<div class="status">
												<span>Books: 0</span>
												<span>Finished: 0</span>
												<span>creation-time: 2020-02-02</span>
											</div>
										</div>
										<div class="operation">
											<img src="../../public/icon/edit.png" title="Edit collection name">
											<img src="../../public/icon/delete.png" title="Delete collection">
											<img src="../../public/icon/copy.png" title="Copy collection">
											<img src="../../public/icon/open.png" title="Open collection" id="open-book-list">
										</div>
									</div>
									<div class="book-list" id="book-list2">
										<div class="no-book">
											<img src="img/icon/hint.png">
											<span>Oops, there is no book yet!</span>
										</div>
										<div class="close-collection" id="close-tab2">
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
				pageNotFound: false
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
				if (this.$route.query.id === undefined){
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
				if(this.$store.state.token){
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
			isMyDashboard(){
				return this.myAccount.user_id === this.account.user_id ? true : false
			},
		},
		mounted: function() {
			this.getAccountsInfo()
		}
	}
</script>

<style scoped>
	@import url("../assets/css/dashboard_common.css");
	@import url("../assets/css/user_collection.css");
</style>
