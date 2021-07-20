import Vue from 'vue'
import Vuex, { Store } from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		email: ''
	},
	mutations: {
		changeEmail(state, email) {
			state.email = email
			localStorage.setItem('user_email', email)
		}
	},
	actions: {
	},
	modules: {
	}
})
