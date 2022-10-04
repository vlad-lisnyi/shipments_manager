import { createRouter, createWebHistory } from 'vue-router'
import ShipmentsView from '../views/Shipments.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: ShipmentsView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
