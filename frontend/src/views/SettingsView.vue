<template>
  <div class="animate-fade-in max-w-5xl">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-dark m-0">Configurações</h1>
      <p class="text-slate-500 mt-1">Configure seu perfil pessoal e preferências do sistema.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
      <!-- Sidebar Settings Navigation -->
      <div class="md:col-span-1">
        <q-list class="bg-transparent">
          <q-item clickable v-ripple @click="currentTab = 'profile'" :class="currentTab === 'profile' ? 'bg-primary/10 text-primary font-medium' : 'text-slate-600'" class="rounded-lg mb-1 transition-colors">
            <q-item-section avatar><q-icon name="person" /></q-item-section>
            <q-item-section>Perfil</q-item-section>
          </q-item>
          <q-item clickable v-ripple @click="currentTab = 'security'" :class="currentTab === 'security' ? 'bg-primary/10 text-primary font-medium' : 'text-slate-600'" class="rounded-lg mb-1 transition-colors">
            <q-item-section avatar><q-icon name="security" /></q-item-section>
            <q-item-section>Segurança</q-item-section>
          </q-item>
          <q-item clickable v-ripple @click="currentTab = 'notifications'" :class="currentTab === 'notifications' ? 'bg-primary/10 text-primary font-medium' : 'text-slate-600'" class="rounded-lg mb-1 transition-colors">
            <q-item-section avatar><q-icon name="notifications" /></q-item-section>
            <q-item-section>Notificações</q-item-section>
          </q-item>
          <q-item clickable v-ripple @click="currentTab = 'appearance'" :class="currentTab === 'appearance' ? 'bg-primary/10 text-primary font-medium' : 'text-slate-600'" class="rounded-lg mb-1 transition-colors">
            <q-item-section avatar><q-icon name="palette" /></q-item-section>
            <q-item-section>Aparência</q-item-section>
          </q-item>
        </q-list>
      </div>

      <!-- Settings Forms Area -->
      <div class="md:col-span-3">
        <!-- PROFILE TAB -->
        <q-card v-if="currentTab === 'profile'" flat class="rounded-2xl border border-slate-200 shadow-sm p-6 animate-fade-in">
          <h2 class="text-lg font-bold text-dark mb-4">Informações Pessoais</h2>
          <div class="flex items-center gap-6 mb-6">
            <q-avatar size="80px" class="border-4 border-slate-100 relative group overflow-hidden cursor-pointer" @click="filePicker.pickFiles()">
              <img :src="profile.avatarUrl">
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <q-icon name="photo_camera" color="white" size="24px" />
              </div>
            </q-avatar>
            <div>
              <q-btn outline color="primary" label="Mudar Avatar" no-caps class="rounded-lg" @click="filePicker.pickFiles()" />
              <q-file v-show="false" ref="filePicker" accept="image/*" @update:model-value="onAvatarSelected" />
              <p class="text-xs text-slate-400 mt-2">Formatos suportados: JPG, PNG (Max. 2MB)</p>
            </div>
          </div>

          <q-form @submit.prevent="saveSettings" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <q-input outlined v-model="profile.firstName" label="Nome" />
              <q-input outlined v-model="profile.lastName" label="Sobrenome" />
            </div>
            <q-input outlined v-model="profile.email" label="Endereço de E-mail" type="email" />
            <q-select outlined v-model="profile.role" :options="['Administrador', 'Gerente', 'Colaborador']" label="Cargo / Função" readonly />

            <div class="flex justify-end pt-4">
              <q-btn type="submit" color="primary" label="Salvar Perfil" class="rounded-xl px-6" no-caps />
            </div>
          </q-form>
        </q-card>

        <!-- SECURITY TAB -->
        <q-card v-if="currentTab === 'security'" flat class="rounded-2xl border border-slate-200 shadow-sm p-6 animate-fade-in">
          <h2 class="text-lg font-bold text-dark mb-4">Segurança e Senha</h2>
          
          <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl mb-6 flex justify-between items-center">
            <div>
              <div class="font-bold text-dark">Autenticação em Dois Fatores (2FA)</div>
              <div class="text-sm text-slate-500">Adiciona uma camada extra de segurança à sua conta.</div>
            </div>
            <q-toggle v-model="security.twoFactor" color="positive" @update:model-value="toggle2FA" />
          </div>

          <h3 class="text-base font-bold text-dark mb-4">Mudar Senha</h3>
          <q-form @submit.prevent="changePassword" class="space-y-4 max-w-md">
            <q-input outlined v-model="security.currentPassword" label="Senha Atual" type="password" />
            <q-input outlined v-model="security.newPassword" label="Nova Senha" type="password" />
            <q-input outlined v-model="security.confirmPassword" label="Confirmar Nova Senha" type="password" />
            <div class="pt-2">
              <q-btn type="submit" color="primary" label="Atualizar Senha" class="rounded-xl px-6" no-caps />
            </div>
          </q-form>
        </q-card>

        <!-- NOTIFICATIONS TAB -->
        <q-card v-if="currentTab === 'notifications'" flat class="rounded-2xl border border-slate-200 shadow-sm p-6 animate-fade-in">
          <h2 class="text-lg font-bold text-dark mb-4">Preferências de Alerta</h2>
          
          <div class="space-y-3 mb-8 max-w-md">
            <q-checkbox v-model="notifications.orders" label="Novos Pedidos (Email & Push)" color="primary" />
            <q-checkbox v-model="notifications.stock" label="Estoque Baixo (Email & Push)" color="primary" />
            <q-checkbox v-model="notifications.marketing" label="Novidades do Sistema (Apenas Email)" color="primary" />
          </div>

          <h3 class="text-base font-bold text-dark mb-4 pt-4 border-t border-slate-100">Histórico de Notificações</h3>
          <q-list separator class="border border-slate-100 rounded-xl overflow-hidden">
            <q-item v-for="(n, index) in notificationHistory" :key="index" class="p-4 bg-slate-50">
              <q-item-section avatar>
                <q-avatar :icon="n.icon" :color="n.color" text-color="white" size="md" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="font-bold text-dark">{{ n.title }}</q-item-label>
                <q-item-label caption>{{ n.description }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <span class="text-xs text-slate-400">{{ n.time }}</span>
              </q-item-section>
            </q-item>
          </q-list>
          <div class="mt-4 flex justify-center">
            <q-btn outline color="slate-400" label="Limpar Histórico" no-caps @click="clearNotifications" v-if="notificationHistory.length > 0" />
            <div v-else class="text-slate-400 text-center py-4">Nenhuma notificação recente.</div>
          </div>
        </q-card>

        <!-- APPEARANCE TAB -->
        <q-card v-if="currentTab === 'appearance'" flat class="rounded-2xl border border-slate-200 shadow-sm p-6 animate-fade-in">
          <h2 class="text-lg font-bold text-dark mb-4">Personalização de Tema</h2>
          
          <div class="mb-6">
            <h3 class="text-sm font-bold text-slate-600 mb-3">Cor Principal (Primária)</h3>
            <div class="flex gap-4">
              <button v-for="color in themeColors" :key="color.hex" 
                      @click="setPrimaryColor(color.hex)"
                      class="w-12 h-12 rounded-full shadow-sm border-2 border-transparent hover:scale-110 transition-transform flex items-center justify-center text-white"
                      :style="`background-color: ${color.hex}; ${appPrimaryColor === color.hex ? 'border-color: #1e293b;' : ''}`">
                <q-icon v-if="appPrimaryColor === color.hex" name="check" size="20px" />
              </button>
            </div>
            <p class="text-xs text-slate-500 mt-2">Selecione uma cor para padronizar botões e destaques no sistema.</p>
          </div>
          
          <q-separator class="my-6" />
          
          <div>
            <h3 class="text-sm font-bold text-slate-600 mb-3">Modo Visual</h3>
            <div class="flex gap-4">
              <q-btn :outline="!$q.dark.isActive" :color="$q.dark.isActive ? 'primary' : 'slate-600'" icon="light_mode" label="Claro" no-caps class="w-32" @click="$q.dark.set(false)" />
              <q-btn :outline="$q.dark.isActive" :color="$q.dark.isActive ? 'slate-600' : 'primary'" icon="dark_mode" label="Escuro" no-caps class="w-32" @click="$q.dark.set(true)" />
            </div>
          </div>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar, setCssVar } from 'quasar'

const $q = useQuasar()
const currentTab = ref('profile')
const filePicker = ref(null)

const profile = ref({
  avatarUrl: 'https://cdn.quasar.dev/img/avatar3.jpg',
  firstName: 'Admin',
  lastName: 'User',
  email: 'admin@crmanager.com',
  role: 'Administrador'
})

const security = ref({
  twoFactor: false,
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const notifications = ref({
  orders: true,
  stock: true,
  marketing: false
})

const notificationHistory = ref([
  { title: 'Novo pedido #1043', description: 'Cliente TechSolutions realizou uma compra no valor de R$4.500', icon: 'shopping_bag', color: 'primary', time: 'Há 5 minutos' },
  { title: 'Estoque Baixo', description: 'O item "Hub USB-C 10-em-1" atingiu o estoque mínimo crítico.', icon: 'warning', color: 'warning', time: 'Há 1 hora' },
  { title: 'Acesso Detectado', description: 'Novo login realizado a partir de um Mac OS.', icon: 'security', color: 'info', time: 'Ontem às 14:02' },
])

const themeColors = [
  { name: 'Indigo (Padrão)', hex: '#4f46e5' },
  { name: 'Cyan', hex: '#06b6d4' },
  { name: 'Emerald', hex: '#10b981' },
  { name: 'Rose', hex: '#f43f5e' },
  { name: 'Amber', hex: '#f59e0b' }
]
const appPrimaryColor = ref('#4f46e5')

const saveSettings = () => {
  $q.notify({ message: 'Perfil atualizado com sucesso!', color: 'positive', icon: 'check_circle' })
}

const changePassword = () => {
  if (security.value.newPassword !== security.value.confirmPassword) {
    $q.notify({ message: 'As senhas não coincidem.', color: 'negative', icon: 'error' })
    return
  }
  $q.notify({ message: 'Senha alterada com sucesso!', color: 'positive', icon: 'vpn_key' })
  security.value.currentPassword = ''
  security.value.newPassword = ''
  security.value.confirmPassword = ''
}

const toggle2FA = (val) => {
  const msg = val ? 'Autenticação 2FA ativada.' : 'Autenticação 2FA desativada.'
  $q.notify({ message: msg, color: val ? 'positive' : 'warning', icon: 'security' })
}

const clearNotifications = () => {
  notificationHistory.value = []
  $q.notify({ message: 'Histórico de notificações limpo.', color: 'info', icon: 'clear_all' })
}

const onAvatarSelected = (file) => {
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      profile.value.avatarUrl = e.target.result
    }
    reader.readAsDataURL(file)
    $q.notify({ message: 'Avatar atualizado!', color: 'positive', icon: 'image' })
  }
}

const setPrimaryColor = (hex) => {
  appPrimaryColor.value = hex
  setCssVar('primary', hex)
  $q.notify({ message: 'Cor primária aplicada!', color: 'positive', icon: 'palette' })
}
</script>
