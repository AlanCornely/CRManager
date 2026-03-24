import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from './layouts/DashboardLayout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('./views/LoginView.vue')
  },
  {
    path: '/',
    component: DashboardLayout,
    children: [
      { path: '', name: 'Dashboard', component: () => import('./views/DashboardView.vue') },
      { path: 'orders', name: 'Orders', component: () => import('./views/OrdersView.vue') },
      { path: 'customers', name: 'Customers', component: () => import('./views/CustomersView.vue') },
      { path: 'inventory', name: 'Inventory', component: () => import('./views/InventoryView.vue') },
      { path: 'finance', name: 'Finance', component: () => import('./views/FinanceView.vue') },
      { path: 'settings', name: 'Settings', component: () => import('./views/SettingsView.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('crm_authenticated') === 'true'
  if (to.name !== 'Login' && !isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
