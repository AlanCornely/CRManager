<template>
  <q-layout view="lHh Lpr lFf" :class="$q.dark.isActive ? 'bg-dark-page' : 'bg-background'">
    <!-- Sidebar -->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :class="$q.dark.isActive ? 'bg-dark' : 'bg-white'"
      :width="260"
    >
      <div class="px-6 py-8 flex items-center gap-3">
        <q-icon name="view_in_ar" size="32px" color="primary" />
        <span class="text-2xl font-bold font-sans tracking-tight" :class="$q.dark.isActive ? 'text-white' : 'text-dark'">CRManager</span>
      </div>

      <q-list class="px-3 mt-4 flex-grow">
        <q-item v-for="link in links" :key="link.title" clickable v-ripple :to="link.to" exact
          active-class="bg-primary/10 text-primary rounded-lg font-medium"
          class="rounded-lg mb-1 transition-colors"
          :class="$q.dark.isActive ? 'text-slate-300' : 'text-slate-600'"
        >
          <q-item-section avatar class="min-w-0 pr-3">
            <q-icon :name="link.icon" size="22px" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-sm font-medium">{{ link.title }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>

      <div class="absolute bottom-4 left-0 w-full px-6">
        <q-separator class="mb-4" />
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium" :class="$q.dark.isActive ? 'text-slate-300' : 'text-slate-600'">Modo Escuro</span>
          <q-toggle v-model="darkMode" color="primary" @update:model-value="toggleDarkMode" />
        </div>
      </div>
    </q-drawer>

    <!-- Header with reveal-on-scroll -->
    <q-header
      reveal
      :class="$q.dark.isActive ? 'bg-dark-header text-white' : 'bg-white text-dark'"
      class="flex flex-col justify-center px-8 shadow-sm"
      style="height:64px;"
    >
      <div class="flex items-center justify-between w-full">
        <div class="flex items-center gap-4">
          <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" class="lg:hidden" :class="$q.dark.isActive ? 'text-white' : 'text-dark'"/>
        </div>
        
        <div class="flex items-center gap-4">
          <q-input
            outlined dense placeholder="Buscar..."
            :bg-color="$q.dark.isActive ? 'dark' : 'white'"
            class="w-64 hidden md:block rounded-xl border-none shadow-sm"
            :input-class="$q.dark.isActive ? 'text-white' : ''"
          >
            <template v-slot:prepend>
              <q-icon name="search" :class="$q.dark.isActive ? 'text-slate-400' : ''" />
            </template>
          </q-input>
          
          <!-- Notification button -->
          <q-btn-dropdown flat round dense no-icon-animation dropdown-icon="none">
            <template v-slot:label>
              <q-btn flat round dense icon="notifications_none"
                :class="$q.dark.isActive ? 'bg-dark text-white border border-slate-600' : 'bg-white text-secondary border border-slate-200'"
                class="rounded-full shadow-sm relative"
              >
                <q-badge color="negative" floating rounded class="text-xs">3</q-badge>
              </q-btn>
            </template>
            <q-list style="min-width: 300px" :class="$q.dark.isActive ? 'bg-dark-card' : ''">
              <q-item-label header :class="$q.dark.isActive ? 'text-slate-300' : ''">Notificações</q-item-label>
              <q-item clickable v-ripple>
                <q-item-section avatar><q-avatar icon="shopping_bag" color="primary" text-color="white" /></q-item-section>
                <q-item-section>
                  <q-item-label :class="$q.dark.isActive ? 'text-white' : ''">Novo pedido #1043</q-item-label>
                  <q-item-label caption>Há 5 minutos</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-ripple>
                <q-item-section avatar><q-avatar icon="warning" color="warning" text-color="white" /></q-item-section>
                <q-item-section>
                  <q-item-label :class="$q.dark.isActive ? 'text-white' : ''">Estoque baixo: Fone de Ouvido</q-item-label>
                  <q-item-label caption>Há 1 hora</q-item-label>
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable class="text-primary text-center" @click="router.push('/settings')">
                <q-item-section>Ver todas</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>

          <!-- Profile icon (#1 - generic icon) -->
          <q-btn-dropdown flat round dense no-icon-animation dropdown-icon="none">
            <template v-slot:label>
              <q-avatar size="40px" :color="$q.dark.isActive ? 'grey-8' : 'grey-3'" class="cursor-pointer">
                <q-icon name="account_circle" :size="'38px'" :color="$q.dark.isActive ? 'grey-4' : 'grey-7'" />
              </q-avatar>
            </template>

            <q-list :class="$q.dark.isActive ? 'bg-dark-card' : ''">
              <q-item clickable v-close-popup @click="router.push('/settings')">
                <q-item-section avatar>
                  <q-icon name="settings" size="20px" class="text-slate-500" />
                </q-item-section>
                <q-item-section :class="$q.dark.isActive ? 'text-white' : ''">Configurações</q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup @click="handleLogout" class="text-negative">
                <q-item-section avatar>
                  <q-icon name="logout" size="20px" color="negative" />
                </q-item-section>
                <q-item-section>Sair</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </div>
    </q-header>

    <!-- Page Content -->
    <q-page-container>
      <q-page class="p-8" :class="$q.dark.isActive ? 'dark-page-content' : ''">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const leftDrawerOpen = ref(false)
const route = useRoute()
const router = useRouter()
const darkMode = ref(false)

onMounted(() => {
  darkMode.value = $q.dark.isActive
})

function toggleDarkMode(val) {
  $q.dark.set(val)
}

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const handleLogout = () => {
  localStorage.removeItem('crm_authenticated')
  router.push('/login')
}

const links = [
  { title: 'Dashboard', icon: 'space_dashboard', to: '/' },
  { title: 'Pedidos', icon: 'shopping_bag', to: '/orders' },
  { title: 'Clientes', icon: 'people_alt', to: '/customers' },
  { title: 'Inventário', icon: 'inventory_2', to: '/inventory' },
  { title: 'Financeiro', icon: 'account_balance_wallet', to: '/finance' }
]
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
