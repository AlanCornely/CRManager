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
        <div class="text-3xl font-bold text-dark mt-2">1.248</div>
      </q-card>
      <q-card flat class="rounded-2xl border border-slate-200 shadow-sm p-4">
        <div class="text-slate-500 font-medium">Ativos este Mês</div>
        <div class="text-3xl font-bold text-primary mt-2">312</div>
      </q-card>
      <q-card flat class="rounded-2xl border border-slate-200 shadow-sm p-4">
        <div class="text-slate-500 font-medium">Gasto Médio</div>
        <div class="text-3xl font-bold text-dark mt-2">R$ 840,50</div>
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
      <q-card style="min-width: 400px; border-radius: 16px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 font-bold">{{ isEditing ? 'Editar Cliente' : 'Adicionar Novo Cliente' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="space-y-4 q-pt-md">
          <q-input outlined v-model="customerForm.name" label="Nome Completo" autofocus />
          <q-input outlined v-model="customerForm.email" label="Endereço de E-mail" type="email" />
          <q-input outlined v-model="customerForm.phone" label="Telefone" />
          <q-select outlined v-model="customerForm.role" :options="['Cliente', 'Distribuidora', 'Sócio', 'Admin', 'Dono']" label="Tipo de Relação" />
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const search = ref('')

const isCustomerDialogOpen = ref(false)
const isEditing = ref(false)
const customerForm = ref({ id: null, name: '', email: '', phone: '', role: 'Cliente', spent: 'R$ 0,00' })

const isEmailDialogOpen = ref(false)
const selectedCustomer = ref(null)
const emailForm = ref({ subject: '', body: '' })

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

const rows = ref([
  { id: 1, name: 'TechSolutions Ltda', email: 'contato@techsolutions.com', phone: '(11) 98765-0100', role: 'Cliente', spent: 'R$ 124.500,00' },
  { id: 2, name: 'Mercado Fácil SA', email: 'vendas@mercadofacil.com.br', phone: '(21) 99888-0101', role: 'Distribuidora', spent: 'R$ 89.200,50' },
  { id: 3, name: 'Carlos Eduardo', email: 'carlos.ed@example.com', phone: '(31) 98888-0102', role: 'Sócio', spent: 'R$ 0,00' },
  { id: 4, name: 'Lojas Delta', email: 'compras@lojasdelta.com', phone: '(41) 97777-0103', role: 'Cliente', spent: 'R$ 42.800,00' },
  { id: 5, name: 'Administração Flow', email: 'admin@crmanager.com', phone: '(11) 95555-0104', role: 'Dono', spent: 'R$ 0,00' },
])

const filteredCustomers = computed(() => {
  if (!search.value) return rows.value
  const lowerQuery = search.value.toLowerCase()
  return rows.value.filter(c => 
    c.name.toLowerCase().includes(lowerQuery) || 
    c.email.toLowerCase().includes(lowerQuery)
  )
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
  customerForm.value = { id: null, name: '', email: '', phone: '', role: 'Cliente', spent: 'R$ 0,00' }
  isCustomerDialogOpen.value = true
}

const openEditDialog = (customer) => {
  isEditing.value = true
  customerForm.value = { ...customer }
  isCustomerDialogOpen.value = true
}

const saveCustomer = () => {
  if (isEditing.value) {
    const index = rows.value.findIndex(c => c.id === customerForm.value.id)
    if (index !== -1) rows.value[index] = { ...customerForm.value }
    $q.notify({ message: 'Cliente atualizado.', color: 'positive', icon: 'check' })
  } else {
    customerForm.value.id = Date.now()
    rows.value.unshift({ ...customerForm.value })
    $q.notify({ message: 'Cliente adicionado.', color: 'positive', icon: 'check' })
  }
  isCustomerDialogOpen.value = false
}

const removeCustomer = (customer) => {
  rows.value = rows.value.filter(c => c.id !== customer.id)
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
</script>
