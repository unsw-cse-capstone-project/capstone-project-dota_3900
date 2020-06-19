import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
		token: localStorage.getItem('token') ? localStorage.getItem('token') : '',
  },
  mutations: {
		updateToken(state, token){
		  state.token = token
		  localStorage.setItem('token', token)
		},
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
