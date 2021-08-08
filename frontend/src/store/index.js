import Vue from 'vue'
import Vuex, { Store } from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		statisticList: ['dldld', 'statistic', 'statistic']
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
