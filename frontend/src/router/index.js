import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import Admin from '../views/Admin.vue'
import User from '../views/User.vue'

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
		component: Admin
	},
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
})

export default router
