import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('@/views/login_view.vue')
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: () => import('@/views/tasks_view.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
