import Vue from 'vue'
import Vuex, { Store } from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    name: 'Boris'
  },
  mutations: {
    changeName(state, count) {
      state.name += ` ${count}`
    }
  },
  actions: {
  },
  modules: {
  }
})
