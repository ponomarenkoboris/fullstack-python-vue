import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import Admin from '../views/Admin.vue'
import User from '../views/User.vue'
import QuizMaker from '../components/QuizMaker.vue'
import Statistic from '../components/Statistic.vue'

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
		component: User
	},
	{
		path: '/admin',
		name: 'Admin',
		component: Admin,
		children: [
			{
				path: 'quiz-maker',
				name: 'QuizMaker',
				component: QuizMaker
			},
			{
				path: 'full-statistic',
				name: 'Statistic',
				component: Statistic
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
