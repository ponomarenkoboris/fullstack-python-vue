import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import axios from 'axios'
import { SERVER_URL, endpoints, getCSRFTokenHeader } from "@/utils"
Vue.use(VueRouter)

const routes = [
	{
		path: '/',
		name: 'Main',
		component: Main
	},
	{
		path: '/worker',
		name: 'Worker',
		component: () => import(/* webpackChunkName: "user" */'../views/Worker.vue')
	},
	{
		path: '/manager',
		name: 'Manager',
		component: () => import(/* webpackChunkName: "admin" */'../views/Manager.vue'),
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

router.beforeEach((to, _, next) => {
	if (to.path !== '/') {
		const email = localStorage.getItem('worker_email') || localStorage.getItem('user_email')
		const config = { withCredentials: true, headers: getCSRFTokenHeader() }
		axios.post(SERVER_URL + endpoints.refresh, { email }, config)
			.then(response => {
				if (response.status === 200) next()
				else next('/')
			})
			.catch(() => {
				next('/')
			})
	} else {
		next()
	}
})

export default router
