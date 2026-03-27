<template>
  <div class="animate-fade-in">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-dark m-0">Relação de Clientes</h1>
        <p class="text-slate-500 mt-1">Gerencie perfis, histórico e permissões.</p>
      </div>
      <q-btn color="primary" icon="person_add" label="Adicionar Cliente" no-caps class="rounded-xl px-4 py-2" @click="openCreateDialog" />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <q-card flat class="rounded-2xl border border-slate-200 shadow-sm p-4">
        <div class="text-slate-500 font-medium">Total de Clientes</div>
        <div class="text-3xl font-bold text-dark mt-2">{{ customers.length }}</div>
      </q-card>
      <q-card flat class="rounded-2xl border border-slate-200 shadow-sm p-4">
        <div class="text-slate-500 font-medium">Ativos este Mês</div>
        <div class="text-3xl font-bold text-primary mt-2">{{ activeThisMonth }}</div>
      </q-card>
      <q-card flat class="rounded-2xl border border-slate-200 shadow-sm p-4">
        <div class="text-slate-500 font-medium">Gasto Médio</div>
        <div class="text-3xl font-bold text-dark mt-2">{{ averageSpent }}</div>
      </q-card>
    </div>

    <q-card flat class="rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <q-card-section class="p-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
        <q-input outlined dense v-model="search" placeholder="Buscar por nome ou e-mail..." class="bg-white rounded-lg w-80 h-10" borderless>
          <template v-slot:prepend>
            <q-icon name="search" class="text-slate-400" />
          </template>
        </q-input>
      </q-card-section>
      
      <q-table
        flat bordered
        :rows="filteredCustomers"
        :columns="columns"
        row-key="id"
        :pagination="initialPagination"
        class="text-slate-700"
      >
        <template v-slot:body-cell-name="props">
          <q-td :props="props" class="flex items-center gap-3">
            <q-avatar size="32px" color="primary" text-color="white">{{ props.row.name.charAt(0) }}</q-avatar>
            <div class="flex flex-col">
              <span class="font-medium text-dark">{{ props.row.name }}</span>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-role="props">
          <q-td :props="props">
            <q-chip :style="`background: ${roleColor(props.row.role).bg}; color: ${roleColor(props.row.role).text}`" dense class="font-bold text-xs" square>
              {{ props.row.role }}
            </q-chip>
          </q-td>
        </template>

        <!-- #9 - spent column -->
        <template v-slot:body-cell-spent="props">
          <q-td :props="props">
            <span class="font-semibold" :class="props.row.spent > 0 ? 'text-positive' : 'text-slate-400'">
              {{ formatSpent(props.row.spent) }}
            </span>
          </q-td>
        </template>
        
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="text-right">
            <q-btn flat dense round color="primary" icon="mail_outline" class="mr-2" @click="sendEmail(props.row)" />
            <q-btn flat dense round color="slate-400" icon="more_vert">
              <q-menu auto-close>
                <q-list style="min-width: 150px">
                  <q-item clickable @click="openEditDialog(props.row)">
                    <q-item-section avatar><q-icon name="edit" size="sm"/></q-item-section>
                    <q-item-section>Editar</q-item-section>
                  </q-item>
                  <q-item clickable @click="openAddSaleDialog(props.row)">
                    <q-item-section avatar><q-icon name="add_shopping_cart" size="sm" color="positive"/></q-item-section>
                    <q-item-section>Registrar Venda</q-item-section>
                  </q-item>
                  <q-item clickable class="text-negative" @click="removeCustomer(props.row)">
                    <q-item-section avatar><q-icon name="delete" color="negative" size="sm"/></q-item-section>
                    <q-item-section>Remover</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Create / Edit Customer Dialog -->
    <q-dialog v-model="isCustomerDialogOpen">
      <q-card style="min-width: 480px; border-radius: 16px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 font-bold">{{ isEditing ? 'Editar Cliente' : 'Adicionar Novo Cliente' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="space-y-4 q-pt-md">
          <q-input outlined v-model="customerForm.name" label="Nome Completo" autofocus />
          <q-input outlined v-model="customerForm.email" label="Endereço de E-mail" type="email" />
          <q-input outlined v-model="customerForm.phone" label="Telefone" mask="(##) #####-####" unmasked-value />
          <q-select outlined v-model="customerForm.role" :options="['Cliente', 'Distribuidora', 'Sócio', 'Admin', 'Dono']" label="Tipo de Relação" />
          
          <!-- #8 - CEP e Número da Casa -->
          <div class="flex gap-3">
            <q-input
              outlined v-model="customerForm.cep" label="CEP"
              class="flex-1" mask="#####-###"
              @blur="fetchAddress"
              hint="Digite o CEP para buscar o endereço"
            >
              <template v-slot:append>
                <q-icon name="search" class="cursor-pointer" @click="fetchAddress" />
              </template>
            </q-input>
            <q-input outlined v-model="customerForm.houseNumber" label="Nº" class="w-24" />
          </div>
          <q-input outlined v-model="customerForm.address" label="Endereço" readonly bg-color="grey-2" v-if="customerForm.address" />
        </q-card-section>

        <q-card-actions align="right" class="text-primary p-4">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat class="bg-primary text-white" label="Salvar Cliente" @click="saveCustomer" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Email Dialog -->
    <q-dialog v-model="isEmailDialogOpen">
      <q-card style="min-width: 400px; border-radius: 16px;">
        <q-card-section class="row items-center q-pb-none border-b border-slate-100 pb-4">
          <div class="text-h6 font-bold flex items-center gap-2"><q-icon name="mail" color="primary"/> Enviar E-mail</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-card-section class="space-y-4 q-pt-md">
          <q-input outlined :model-value="selectedCustomer?.email" label="Para" readonly bg-color="slate-50" />
          <q-input outlined v-model="emailForm.subject" label="Assunto" autofocus />
          <q-input outlined v-model="emailForm.body" type="textarea" label="Mensagem" />
        </q-card-section>
        <q-card-actions align="right" class="text-primary p-4">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat class="bg-primary text-white" label="Enviar" @click="confirmSendEmail" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- #9 - Add Sale Dialog -->
    <q-dialog v-model="isAddSaleDialogOpen">
      <q-card style="min-width: 380px; border-radius: 16px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 font-bold flex items-center gap-2">
            <q-icon name="add_shopping_cart" color="positive" /> Registrar Venda
          </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-card-section class="q-pt-md">
          <p class="text-slate-500 mb-4">Cliente: <strong>{{ selectedCustomer?.name }}</strong></p>
          <q-input
            outlined v-model="saleAmount" label="Valor da Venda (R$)"
            type="number" step="0.01" min="0" autofocus
          />
        </q-card-section>
        <q-card-actions align="right" class="text-primary p-4">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat class="bg-positive text-white" label="Confirmar Venda" @click="confirmSale" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useCustomers } from '../composables/useCustomers'

const $q = useQuasar()
const { customers, formatSpent, addCustomer, updateCustomer, removeCustomer: removeFromStore, addSpent } = useCustomers()

const search = ref('')
const isCustomerDialogOpen = ref(false)
const isEditing = ref(false)
const customerForm = ref({ id: null, name: '', email: '', phone: '', role: 'Cliente', cep: '', houseNumber: '', address: '' })

const isEmailDialogOpen = ref(false)
const selectedCustomer = ref(null)
const emailForm = ref({ subject: '', body: '' })

const isAddSaleDialogOpen = ref(false)
const saleAmount = ref('')

const initialPagination = {
  sortBy: 'name',
  descending: false,
  page: 1,
  rowsPerPage: 10
}

const columns = [
  { name: 'name', align: 'left', label: 'Nome do Cliente', field: 'name', sortable: true },
  { name: 'email', align: 'left', label: 'E-mail', field: 'email', sortable: true },
  { name: 'phone', align: 'left', label: 'Telefone', field: 'phone' },
  { name: 'role', align: 'left', label: 'Relação', field: 'role', sortable: true },
  { name: 'spent', align: 'left', label: 'Gasto Total', field: 'spent', sortable: true },
  { name: 'actions', align: 'center', label: 'Ações', field: 'actions' }
]

const filteredCustomers = computed(() => {
  if (!search.value) return customers.value
  const lowerQuery = search.value.toLowerCase()
  return customers.value.filter(c => 
    c.name.toLowerCase().includes(lowerQuery) || 
    c.email.toLowerCase().includes(lowerQuery)
  )
})

// Stats
const activeThisMonth = computed(() => Math.floor(customers.value.length * 0.25))
const averageSpent = computed(() => {
  const total = customers.value.reduce((s, c) => s + (c.spent || 0), 0)
  return formatSpent(customers.value.length ? total / customers.value.length : 0)
})

const roleColor = (role) => {
  switch (role) {
    case 'Cliente': return { bg: '#e0f2fe', text: '#0284c7' }
    case 'Distribuidora': return { bg: '#fef08a', text: '#a16207' }
    case 'Sócio': return { bg: '#fce7f3', text: '#db2777' }
    case 'Admin': return { bg: '#dcfce7', text: '#16a34a' }
    case 'Dono': return { bg: '#f3e8ff', text: '#9333ea' }
    default: return { bg: '#f1f5f9', text: '#64748b' }
  }
}

const openCreateDialog = () => {
  isEditing.value = false
  customerForm.value = { id: null, name: '', email: '', phone: '', role: 'Cliente', cep: '', houseNumber: '', address: '' }
  isCustomerDialogOpen.value = true
}

const openEditDialog = (customer) => {
  isEditing.value = true
  customerForm.value = { ...customer, address: customer.address || '' }
  isCustomerDialogOpen.value = true
}

// #8 - Fetch address via ViaCEP
const fetchAddress = async () => {
  const cep = customerForm.value.cep.replace(/\D/g, '')
  if (cep.length !== 8) return
  try {
    const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`)
    const data = await res.json()
    if (!data.erro) {
      customerForm.value.address = `${data.logradouro}, ${data.bairro} – ${data.localidade}/${data.uf}`
    } else {
      $q.notify({ message: 'CEP não encontrado.', color: 'warning', icon: 'warning' })
    }
  } catch {
    $q.notify({ message: 'Erro ao buscar CEP.', color: 'negative', icon: 'error' })
  }
}

const saveCustomer = () => {
  if (isEditing.value) {
    updateCustomer({ ...customerForm.value })
    $q.notify({ message: 'Cliente atualizado.', color: 'positive', icon: 'check' })
  } else {
    addCustomer({ ...customerForm.value })
    $q.notify({ message: 'Cliente adicionado.', color: 'positive', icon: 'check' })
  }
  isCustomerDialogOpen.value = false
}

const removeCustomer = (customer) => {
  removeFromStore(customer.id)
  $q.notify({ message: 'Cliente removido.', color: 'negative', icon: 'delete' })
}

const sendEmail = (customer) => {
  selectedCustomer.value = customer
  emailForm.value = { subject: '', body: '' }
  isEmailDialogOpen.value = true
}

const confirmSendEmail = () => {
  $q.notify({ message: `E-mail enviado para ${selectedCustomer.value.email}`, color: 'positive', icon: 'send' })
  isEmailDialogOpen.value = false
}

// #9 - Register sale
const openAddSaleDialog = (customer) => {
  selectedCustomer.value = customer
  saleAmount.value = ''
  isAddSaleDialogOpen.value = true
}

const confirmSale = () => {
  const amount = parseFloat(saleAmount.value)
  if (!amount || amount <= 0) {
    $q.notify({ message: 'Informe um valor válido.', color: 'negative', icon: 'error' })
    return
  }
  addSpent(selectedCustomer.value.id, amount)
  $q.notify({ message: `Venda de ${formatSpent(amount)} registrada para ${selectedCustomer.value.name}`, color: 'positive', icon: 'check' })
  isAddSaleDialogOpen.value = false
}
</script>
