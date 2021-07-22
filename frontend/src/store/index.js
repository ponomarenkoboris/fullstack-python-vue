import Vue from 'vue'
import Vuex, { Store } from 'vuex'
import { quizList } from '../testData.js'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		quizList: quizList
	},
	mutations: {
		writeAnswer(state, { quizIndex, question, answer }) {
			state.quizList[quizIndex].questions.forEach(quest => { if (quest.id === question.id) quest.answer = answer })
		}
	},
	actions: {
	},
	modules: {
	}
})
