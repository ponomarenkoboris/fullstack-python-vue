import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'

Vue.use(VueRouter)

const routes = [
	{
		path: '/',
		name: 'Main',
		component: Main
	},
	{
		path: '/user',
		name: 'User',
		component: () => import(/* webpackChunkName: "user" */'../views/User.vue')
	},
	{
		path: '/admin',
		name: 'Admin',
		component: () => import(/* webpackChunkName: "admin" */'../views/Admin.vue'),
		children: [
			{
				path: 'quiz-maker/',
				name: 'QuizMaker',
				component: () => import(/* webpackChunkName: "admin/quiz-maker" */'../components/QuizMaker.vue')
			},
			{
				path: 'full-statistic/',
				name: 'Statistic',
				component: () => import(/* webpackChunkName: "admin/statistic" */'../components/Statistic.vue')
			},
			{
				path: 'questions-groups/',
				name: 'QuestionGroups',
				component: () => import(/* webpackChunkName: "admin/questions-groups" */'../components/QuestionsGroups.vue')
			}
		]
	},
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
})

export default router
