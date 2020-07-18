import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import BookDetail from '../views/BookDetail.vue'
import NotFoundPage from '../views/404.vue'
import Dashboard from '../views/Dashboard.vue'
import SearchResult from '../views/SearchResult.vue'
import UserSearchResult from '../views/SearchResultUser.vue'
import BookReviews from '../views/ReviewList.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/book',
    name: 'Book',
    component: BookDetail,
  },
	{
		path: '/user',
		alias: '/user/collection',
		name: 'UserCollection',
		component: Dashboard
	},
	{
		path: '/user/monthly_goal',
		name: 'UserMonthlyGoal',
		component: Dashboard
	},
	{
		path: '/user/read_history',
		name: 'UserReadHistory',
		component: Dashboard
	},
	{
		path: '/user/reviews',
		name: 'UserReviews',
		component: Dashboard
	},
	{
		path: '/book/reviews',
		name: 'BookReviews',
		component: BookReviews
	},
	{
		path: '/search',
		name: 'SearchResult',
		component: SearchResult
	},
	{
		path: '/user-search',
		name: 'UserSearchResult',
		component: UserSearchResult
	},
	{
		path: '*',
		name: '404Page',
		component: NotFoundPage
	}
]

const router = new VueRouter({
  routes
})

export default router
