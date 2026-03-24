<template>
  <div class="animate-fade-in">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-dark m-0">Gestão de Pedidos</h1>
        <p class="text-slate-500 mt-1">Visualize, rastreie e gerencie os pedidos de clientes.</p>
      </div>
      <q-btn color="primary" icon="add" label="Criar Pedido" no-caps class="rounded-xl px-4 py-2" @click="openCreateDialog" />
    </div>

    <!-- #7 - Status summary cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <q-card flat class="rounded-2xl border border-warning/30 bg-warning/5 shadow-sm p-4">
        <div class="flex items-center gap-3">
          <q-avatar color="warning" text-color="white" icon="pending" size="42px" />
          <div>
            <div class="text-slate-500 text-sm font-medium">Em Processo</div>
            <div class="text-3xl font-bold text-warning">{{ statusCount('Processando') }}</div>
          </div>
        </div>
      </q-card>
      <q-card flat class="rounded-2xl border border-info/30 bg-info/5 shadow-sm p-4">
        <div class="flex items-center gap-3">
          <q-avatar color="info" text-color="white" icon="local_shipping" size="42px" />
          <div>
            <div class="text-slate-500 text-sm font-medium">Enviados</div>
            <div class="text-3xl font-bold text-info">{{ statusCount('Enviado') }}</div>
          </div>
        </div>
      </q-card>
      <q-card flat class="rounded-2xl border border-positive/30 bg-positive/5 shadow-sm p-4">
        <div class="flex items-center gap-3">
          <q-avatar color="positive" text-color="white" icon="check_circle" size="42px" />
          <div>
            <div class="text-slate-500 text-sm font-medium">Entregues</div>
            <div class="text-3xl font-bold text-positive">{{ statusCount('Entregue') }}</div>
          </div>
        </div>
      </q-card>
    </div>

    <q-card flat class="rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <q-card-section class="p-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
        <q-input outlined dense v-model="search" placeholder="Buscar pedidos..." class="bg-white rounded-lg w-72 h-10" borderless>
          <template v-slot:prepend>
            <q-icon name="search" class="text-slate-400" />
          </template>
        </q-input>
        <q-btn flat icon="filter_list" label="Filtrar" class="text-slate-600 bg-white border border-slate-200 rounded-lg px-4" no-caps @click="showFilters = !showFilters" />
      </q-card-section>

      <!-- Advanced Filters -->
      <q-slide-transition>
        <div v-show="showFilters" class="p-4 bg-slate-50 border-b border-slate-100 flex gap-4 items-center">
          <q-select outlined dense v-model="statusFilter" :options="['Todos', 'Processando', 'Enviado', 'Entregue', 'Cancelado']" label="Status" class="w-48 bg-white" />
          <q-btn outline color="primary" label="Aplicar Filtros" @click="applyFilters" />
          <q-btn flat color="slate-500" label="Limpar" @click="clearFilters" />
        </div>
      </q-slide-transition>
      <q-table
        flat bordered
        :rows="filteredOrders"
        :columns="columns"
        row-key="id"
        :pagination="initialPagination"
        class="text-slate-700"
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-chip
              :color="props.row.status === 'Entregue' ? 'positive' : props.row.status === 'Processando' ? 'warning' : props.row.status === 'Cancelado' ? 'negative' : 'info'"
              text-color="white"
              dense class="font-medium" square
            >
              {{ props.row.status }}
            </q-chip>
          </q-td>
        </template>
        
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="text-right">
            <q-btn flat round color="slate-400" icon="more_vert">
              <q-menu auto-close>
                <q-list style="min-width: 150px">
                  <q-item clickable @click="openEditDialog(props.row)">
                    <q-item-section avatar><q-icon name="edit" size="sm"/></q-item-section>
                    <q-item-section>Editar Pedido</q-item-section>
                  </q-item>
                  <q-item clickable class="text-negative" @click="cancelOrder(props.row)">
                    <q-item-section avatar><q-icon name="cancel" color="negative" size="sm"/></q-item-section>
                    <q-item-section>Cancelar Pedido</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Create / Edit Order Dialog -->
    <q-dialog v-model="isOrderDialogOpen">
      <q-card style="min-width: 480px; border-radius: 16px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 font-bold">{{ isEditing ? 'Editar Pedido' : 'Criar Novo Pedido' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="space-y-4 q-pt-md">
          <q-input outlined v-model="orderForm.customer" label="Nome do Cliente" autofocus />
          <!-- #6 - Lote e Objeto do pedido (obrigatórios) -->
          <q-input
            outlined v-model="orderForm.lote" label="Número do Lote *"
            :rules="[val => !!val || 'Informe o número do lote']"
            hint="Ex: LOTE-2025-001"
          />
          <q-input
            outlined v-model="orderForm.objeto" label="Objeto / Descrição do Pedido *"
            :rules="[val => !!val || 'Informe o objeto do pedido']"
            type="textarea" autogrow
            hint="Descreva o conteúdo ou finalidade do pedido"
          />
          <q-input outlined v-model="orderForm.total" label="Valor Total (Ex: R$ 150,00)" />
          <q-select outlined v-model="orderForm.status" :options="['Processando', 'Enviado', 'Entregue', 'Cancelado']" label="Status" />
        </q-card-section>

        <q-card-actions align="right" class="text-primary p-4">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat class="bg-primary text-white" label="Salvar Pedido" @click="saveOrder" />
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
const showFilters = ref(false)
const statusFilter = ref('Todos')

const isOrderDialogOpen = ref(false)
const isEditing = ref(false)
const orderForm = ref({ id: '', customer: '', lote: '', objeto: '', total: '', status: 'Processando' })

const initialPagination = {
  sortBy: 'id',
  descending: true,
  page: 1,
  rowsPerPage: 10
}

const columns = [
  { name: 'id', align: 'left', label: 'ID Pedido', field: 'id', sortable: true },
  { name: 'lote', align: 'left', label: 'Lote', field: 'lote', sortable: true },
  { name: 'customer', align: 'left', label: 'Cliente', field: 'customer', sortable: true },
  { name: 'date', align: 'left', label: 'Data', field: 'date', sortable: true },
  { name: 'total', align: 'left', label: 'Total', field: 'total', sortable: true },
  { name: 'status', align: 'left', label: 'Status', field: 'status', sortable: true },
  { name: 'actions', align: 'center', label: 'Ações', field: 'actions' }
]

const rows = ref([
  { id: '#ORD-001', lote: 'LOTE-2025-001', customer: 'Alice Johnson', date: '2025-03-10', total: 'R$ 120,00', status: 'Processando', objeto: 'Teclado mecânico e mouse' },
  { id: '#ORD-002', lote: 'LOTE-2025-002', customer: 'Bob Smith', date: '2025-03-09', total: 'R$ 85,50', status: 'Entregue', objeto: 'Hub USB-C' },
  { id: '#ORD-003', lote: 'LOTE-2025-003', customer: 'Charlie Brown', date: '2025-03-08', total: 'R$ 210,00', status: 'Enviado', objeto: 'Fone de Ouvido NC' },
  { id: '#ORD-004', lote: 'LOTE-2025-004', customer: 'Diana Prince', date: '2025-03-08', total: 'R$ 15,99', status: 'Entregue', objeto: 'Cabo USB-C' },
  { id: '#ORD-005', lote: 'LOTE-2025-005', customer: 'Evan Wright', date: '2025-03-07', total: 'R$ 450,00', status: 'Processando', objeto: 'Mesa Ajustável' },
  { id: '#ORD-006', lote: 'LOTE-2025-006', customer: 'Fiona Gallagher', date: '2025-03-06', total: 'R$ 65,00', status: 'Entregue', objeto: 'Led de Mesa' },
  { id: '#ORD-007', lote: 'LOTE-2025-007', customer: 'George Miller', date: '2025-03-05', total: 'R$ 99,90', status: 'Enviado', objeto: 'Mouse Ergonômico' },
])

// #7 - Status counter
const statusCount = (status) => rows.value.filter(o => o.status === status).length

const filteredOrders = computed(() => {
  let result = rows.value
  if (statusFilter.value !== 'Todos') {
    result = result.filter(order => order.status === statusFilter.value)
  }
  if (search.value) {
    const lowerQuery = search.value.toLowerCase()
    result = result.filter(order => 
      order.customer.toLowerCase().includes(lowerQuery) || 
      order.id.toLowerCase().includes(lowerQuery) ||
      (order.lote || '').toLowerCase().includes(lowerQuery)
    )
  }
  return result
})

const applyFilters = () => {
  $q.notify({ message: 'Filtros aplicados', color: 'primary', icon: 'filter_list' })
}

const clearFilters = () => {
  statusFilter.value = 'Todos'
  search.value = ''
}

const openCreateDialog = () => {
  isEditing.value = false
  orderForm.value = { id: '', customer: '', lote: '', objeto: '', total: '', status: 'Processando' }
  isOrderDialogOpen.value = true
}

const openEditDialog = (order) => {
  isEditing.value = true
  orderForm.value = { ...order }
  isOrderDialogOpen.value = true
}

const saveOrder = () => {
  // #6 - Validate lote and objeto
  if (!orderForm.value.lote || !orderForm.value.objeto) {
    $q.notify({ message: 'Preencha o número do lote e o objeto do pedido.', color: 'negative', icon: 'error' })
    return
  }

  if (isEditing.value) {
    const index = rows.value.findIndex(o => o.id === orderForm.value.id)
    if (index !== -1) rows.value[index] = { ...orderForm.value }
    $q.notify({ message: 'Pedido atualizado com sucesso.', color: 'positive', icon: 'check' })
  } else {
    const newId = `#ORD-00${rows.value.length + 1}`
    rows.value.unshift({
      id: newId,
      lote: orderForm.value.lote,
      objeto: orderForm.value.objeto,
      customer: orderForm.value.customer || 'Novo Cliente',
      date: new Date().toISOString().split('T')[0],
      total: orderForm.value.total || 'R$ 0,00',
      status: orderForm.value.status
    })
    $q.notify({ message: 'Pedido criado com sucesso.', color: 'positive', icon: 'check' })
  }
  isOrderDialogOpen.value = false
}

const cancelOrder = (order) => {
  order.status = 'Cancelado'
  $q.notify({ message: `Pedido ${order.id} foi cancelado.`, color: 'warning', icon: 'cancel' })
}
</script>
