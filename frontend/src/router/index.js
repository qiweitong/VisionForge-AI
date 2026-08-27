import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import Home from '../views/Home.vue'
import History from '@/views/History.vue'
import Dashboard from '@/views/Dashboard.vue'
import Realtime from '@/views/Realtime.vue'
import ModelManager from '@/views/ModelManager.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: "Home",
        component: Home
      },
      {
        path: "history",
        name: "History",
        component: History
      },
      {
        path: "dashboard",
        name: "Dashboard",
        component: Dashboard
      },
      {
        path: "realtime",
        name: "Realtime",
        alias:"camera",
        component: Realtime
      },
      {
        path: "model",
        name: "ModelManager",
        component: ModelManager
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
