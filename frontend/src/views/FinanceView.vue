<template>
  <div class="animate-fade-in">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-dark m-0">Financeiro & Contabilidade</h1>
        <p class="text-slate-500 mt-1">Acompanhe receitas, despesas e saúde financeira.</p>
      </div>
      <q-btn color="primary" icon="add" label="Nova Transação" no-caps class="rounded-xl px-4 py-2" @click="openTransactionDialog" />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <q-card flat class="rounded-2xl bg-indigo-50 border-2 border-indigo-200 text-indigo-900 shadow-sm p-6">
        <div class="text-indigo-700 font-medium flex items-center gap-2">
          <q-icon name="account_balance_wallet" size="sm" /> Lucro Líquido
        </div>
        <div class="text-4xl font-bold mt-2">R$ 42.500,00</div>
        <div class="mt-4 text-sm bg-white/60 rounded-lg px-3 py-1 inline-block text-indigo-700 font-semibold border border-indigo-200">
          +12.5% vs último mês
        </div>
      </q-card>
      
      <q-card flat class="rounded-2xl bg-rose-50 border-2 border-rose-200 text-rose-900 shadow-sm p-6">
        <div class="text-rose-700 font-medium flex items-center gap-2">
          <q-icon name="money_off" size="sm" /> Total de Despesas
        </div>
        <div class="text-4xl font-bold mt-2">R$ 18.240,50</div>
        <div class="mt-4 text-sm bg-white/60 rounded-lg px-3 py-1 inline-block text-rose-700 font-semibold border border-rose-200">
          -2.4% vs último mês
        </div>
      </q-card>
    </div>

    <h2 class="text-lg font-bold text-dark mb-4">Transações Recentes</h2>
    <q-card flat class="rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <q-list separator>
        <q-item v-for="tx in transactions" :key="tx.id" class="p-4">
          <q-item-section avatar>
            <q-avatar :color="tx.type === 'income' ? 'positive' : 'negative'" text-color="white" :icon="tx.type === 'income' ? 'arrow_downward' : 'arrow_upward'" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="font-bold text-dark">{{ tx.description }}</q-item-label>
            <q-item-label caption>{{ tx.date }}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <div :class="['font-bold text-lg', tx.type === 'income' ? 'text-positive' : 'text-negative']">
              {{ tx.type === 'income' ? '+' : '-' }}R$ {{ tx.amount }}
            </div>
            <div class="text-xs text-slate-400 mt-1">{{ tx.account }}</div>
          </q-item-section>
        </q-item>
      </q-list>
    </q-card>

    <!-- New Transaction Dialog -->
    <q-dialog v-model="isTransactionDialogOpen">
      <q-card style="min-width: 450px; border-radius: 16px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 font-bold">Registrar Nova Transação</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="space-y-4 q-pt-md">
          <div class="flex gap-4">
            <q-radio v-model="txForm.type" val="income" label="Receita" color="positive" />
            <q-radio v-model="txForm.type" val="expense" label="Despesa" color="negative" />
          </div>
          <q-input outlined v-model="txForm.name" label="Nome / Título" autofocus />
          <q-input outlined v-model="txForm.description" label="Descrição da Transação" />
          <q-input outlined v-model="txForm.amount" label="Valor (R$)" type="number" step="0.01" />
          <q-select outlined v-model="txForm.account" :options="['Conta Corrente', 'Cartão Corporativo', 'Caixa Interno']" label="Conta / Destino do Valor" />
          
          <!-- #11 – Auto date/time, readonly. Fetched from API -->
          <div class="flex gap-4">
            <q-input
              outlined :model-value="txForm.date" label="Dia"
              class="flex-1" readonly bg-color="grey-2"
            >
              <template v-slot:append>
                <q-icon name="event" color="primary" />
              </template>
            </q-input>
            <q-input
              outlined :model-value="txForm.time" label="Hora"
              class="flex-1" readonly bg-color="grey-2"
            >
              <template v-slot:append>
                <q-icon v-if="loadingTime" name="hourglass_top" color="primary" class="rotating" />
                <q-icon v-else name="schedule" color="primary" />
              </template>
            </q-input>
          </div>
          <p class="text-xs text-slate-400 flex items-center gap-1">
            <q-icon name="lock" size="xs" />
            Data e hora sincronizadas automaticamente. Não editável.
          </p>
        </q-card-section>

        <q-card-actions align="right" class="text-primary p-4">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat class="bg-primary text-white" label="Salvar Transação" @click="saveTransaction" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const isTransactionDialogOpen = ref(false)
const loadingTime = ref(false)
const txForm = ref({
  type: 'expense',
  name: '',
  description: '',
  amount: '',
  account: 'Conta Corrente',
  date: '',
  time: ''
})

// #11 – Fetch current Brazil time from Local API, fallback to local Date
const fetchCurrentDateTime = async () => {
  loadingTime.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/v1/time')
    if (!res.ok) throw new Error('API error')
    const data = await res.json()
    txForm.value.date = data.date
    txForm.value.time = data.time
  } catch {
    // Fallback to local time
    const now = new Date()
    txForm.value.date = now.toLocaleDateString('pt-BR')
    txForm.value.time = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
  } finally {
    loadingTime.value = false
  }
}

const openTransactionDialog = async () => {
  txForm.value = {
    type: 'expense',
    name: '',
    description: '',
    amount: '',
    account: 'Conta Corrente',
    date: '',
    time: ''
  }
  isTransactionDialogOpen.value = true
  await fetchCurrentDateTime()
}

const transactions = ref([
  { id: 1, type: 'income', description: 'Repasse Nuvemshop - Vendas Mensais', date: '10/03/2025 10:45', amount: '8.450,00', account: 'Conta Corrente - Itaú' },
  { id: 2, type: 'expense', description: 'Infraestrutura AWS', date: '09/03/2025 14:20', amount: '340,50', account: 'Cartão Corporativo' },
  { id: 3, type: 'income', description: 'Pedido B2B Atacado #1042', date: '08/03/2025 09:12', amount: '12.500,00', account: 'Conta Corrente - Itaú' },
  { id: 4, type: 'expense', description: 'Material de Escritório - Kalunga', date: '07/03/2025 16:30', amount: '125,99', account: 'Cartão Corporativo' },
  { id: 5, type: 'expense', description: 'Anúncios Google Ads', date: '06/03/2025 11:00', amount: '1.200,00', account: 'Cartão Corporativo' },
])

const saveTransaction = () => {
  if (!txForm.value.name || !txForm.value.amount) {
    $q.notify({ message: 'Preencha o nome e o valor.', color: 'negative', icon: 'error' })
    return
  }

  const dtStr = `${txForm.value.date} ${txForm.value.time}`
  const amtStr = parseFloat(txForm.value.amount).toLocaleString('pt-BR', { minimumFractionDigits: 2 })

  transactions.value.unshift({
    id: Date.now(),
    type: txForm.value.type,
    description: txForm.value.name + (txForm.value.description ? ` - ${txForm.value.description}` : ''),
    date: dtStr,
    amount: amtStr,
    account: txForm.value.account
  })

  $q.notify({ message: 'Transação registrada com sucesso!', color: 'positive', icon: 'check' })
  isTransactionDialogOpen.value = false
}
</script>

<style scoped>
.rotating {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
