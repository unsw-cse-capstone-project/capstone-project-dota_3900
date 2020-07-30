import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
		token: localStorage.getItem('token') ? localStorage.getItem('token') : '',
  },
  mutations: {
		// store or update token into localstorage
		updateToken(state, token){
		  state.token = token
		  localStorage.setItem('token', token)
		},
		// remove token from localstorage
		clearToken(state){
		  state.token = ''
		  localStorage.removeItem('token')
		},
  },
  actions: {
  },
  modules: {
  }
})
