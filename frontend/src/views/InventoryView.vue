<template>
  <div class="animate-fade-in">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-dark m-0">Controle de Estoque</h1>
        <p class="text-slate-500 mt-1">Gerencie níveis de estoque, preços e detalhes de produtos.</p>
      </div>
      <q-btn color="primary" icon="inventory_2" label="Adicionar Produto" no-caps class="rounded-xl px-4 py-2" @click="openCreateDialog" />
    </div>

    <q-card flat class="rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <q-card-section class="p-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
        <q-input outlined dense v-model="search" placeholder="Buscar produtos..." class="bg-white rounded-lg w-72 h-10" borderless>
          <template v-slot:prepend>
            <q-icon name="search" class="text-slate-400" />
          </template>
        </q-input>
        <div class="flex gap-2">
          <q-btn flat icon="filter_alt" label="Estoque Baixo" :color="filterLowStock ? 'negative' : 'slate-600'" class="bg-white border border-slate-200 rounded-lg px-4" no-caps @click="filterLowStock = !filterLowStock" />
        </div>
      </q-card-section>
      
      <q-table
        flat bordered
        :rows="filteredProducts"
        :columns="columns"
        row-key="id"
        :pagination="initialPagination"
        class="text-slate-700"
      >
        <template v-slot:body-cell-category="props">
          <q-td :props="props">
            <q-chip dense square :style="categoryStyle(props.row.category)">{{ props.row.category }}</q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-stock="props">
          <q-td :props="props">
            <div class="flex items-center gap-2">
              <span :class="props.row.stock < 20 ? 'text-negative font-bold' : 'text-slate-700'">{{ props.row.stock }} un</span>
              <q-icon v-if="props.row.stock < 20" name="warning" color="negative" size="xs">
                <q-tooltip>Estoque Baixo</q-tooltip>
              </q-icon>
            </div>
          </q-td>
        </template>
        
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="text-right">
            <q-btn flat dense round color="primary" icon="edit" class="mr-1" @click="openEditDialog(props.row)" />
            <q-btn flat dense round color="negative" icon="delete_outline" @click="removeProduct(props.row)" />
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Create / Edit Product Dialog -->
    <q-dialog v-model="isProductDialogOpen">
      <q-card style="min-width: 440px; border-radius: 16px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 font-bold">{{ isEditing ? 'Editar Produto' : 'Adicionar Novo Produto' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="space-y-4 q-pt-md">
          <q-input outlined v-model="productForm.sku" label="SKU (Automático)" readonly />
          <q-input outlined v-model="productForm.product" label="Nome do Produto" autofocus />
          
          <!-- #10 - Category select with fixed categories + create new -->
          <q-select
            outlined
            v-model="productForm.category"
            :options="categoryOptions"
            label="Categoria"
            use-input
            hide-selected
            fill-input
            input-debounce="0"
            @filter="filterCategories"
          >
            <template v-slot:before-options>
              <q-item clickable class="text-primary font-semibold" @click.stop="openNewCategoryDialog">
                <q-item-section avatar><q-icon name="add_circle" color="primary" /></q-item-section>
                <q-item-section>Nova Categoria</q-item-section>
              </q-item>
              <q-separator />
            </template>
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey">Nenhuma categoria encontrada</q-item-section>
              </q-item>
            </template>
          </q-select>

          <q-input outlined v-model="productForm.price" label="Preço (R$)" type="number" step="0.01" />
          <q-input outlined v-model.number="productForm.stock" type="number" min="0" label="Quantidade em Estoque" />
        </q-card-section>

        <q-card-actions align="right" class="text-primary p-4">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat class="bg-primary text-white" label="Salvar Produto" @click="saveProduct" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- New Category Dialog -->
    <q-dialog v-model="isNewCategoryDialogOpen">
      <q-card style="min-width: 360px; border-radius: 16px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 font-bold">Nova Categoria</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-card-section class="q-pt-md">
          <q-input outlined v-model="newCategoryName" label="Nome da Categoria" autofocus @keyup.enter="saveNewCategory" />
        </q-card-section>
        <q-card-actions align="right" class="p-4">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn flat class="bg-primary text-white" label="Criar" @click="saveNewCategory" />
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
const filterLowStock = ref(false)
const isProductDialogOpen = ref(false)
const isEditing = ref(false)
const productForm = ref({ id: null, sku: '', product: '', category: '', price: '', stock: 0 })

const isNewCategoryDialogOpen = ref(false)
const newCategoryName = ref('')

// #10 - Fixed categories + ability to add new ones
const fixedCategories = ['Eletrônicos', 'Móveis', 'Acessórios', 'Vestuário', 'Alimentos', 'Ferramentas']
const customCategories = ref([])
const allCategories = computed(() => [...fixedCategories, ...customCategories.value])
const categoryOptions = ref([...fixedCategories])

const filterCategories = (val, update) => {
  update(() => {
    if (val === '') {
      categoryOptions.value = allCategories.value
    } else {
      const needle = val.toLowerCase()
      categoryOptions.value = allCategories.value.filter(c => c.toLowerCase().includes(needle))
    }
  })
}

const openNewCategoryDialog = () => {
  newCategoryName.value = ''
  isNewCategoryDialogOpen.value = true
}

const saveNewCategory = () => {
  const name = newCategoryName.value.trim()
  if (!name) {
    $q.notify({ message: 'Digite o nome da categoria.', color: 'warning', icon: 'warning' })
    return
  }
  if (allCategories.value.includes(name)) {
    $q.notify({ message: 'Categoria já existe.', color: 'warning', icon: 'warning' })
    return
  }
  customCategories.value.push(name)
  productForm.value.category = name
  isNewCategoryDialogOpen.value = false
  $q.notify({ message: `Categoria "${name}" criada!`, color: 'positive', icon: 'check' })
}

const categoryColors = {
  'Eletrônicos': { bg: '#dbeafe', text: '#1d4ed8' },
  'Móveis': { bg: '#fef3c7', text: '#b45309' },
  'Acessórios': { bg: '#ede9fe', text: '#7c3aed' },
  'Vestuário': { bg: '#fce7f3', text: '#db2777' },
  'Alimentos': { bg: '#dcfce7', text: '#15803d' },
  'Ferramentas': { bg: '#fee2e2', text: '#b91c1c' },
}

const categoryStyle = (category) => {
  const c = categoryColors[category] || { bg: '#f1f5f9', text: '#64748b' }
  return `background: ${c.bg}; color: ${c.text};`
}

const initialPagination = {
  sortBy: 'stock',
  descending: false,
  page: 1,
  rowsPerPage: 10
}

const columns = [
  { name: 'sku', align: 'left', label: 'SKU', field: 'sku', sortable: true },
  { name: 'product', align: 'left', label: 'Nome do Produto', field: 'product', sortable: true },
  { name: 'category', align: 'left', label: 'Categoria', field: 'category', sortable: true },
  { name: 'price', align: 'left', label: 'Preço', field: 'price', sortable: true },
  { name: 'stock', align: 'left', label: 'Estoque', field: 'stock', sortable: true },
  { name: 'actions', align: 'center', label: 'Ações', field: 'actions' }
]

const rows = ref([])

const fetchProducts = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/v1/produtos/')
    if (res.ok) {
      const data = await res.json()
      rows.value = data.map(p => ({
        id: p.id_produto,
        sku: p.sku || `SKU-${p.id_produto}`,
        product: p.nome,
        category: 'Eletrônicos',
        price: p.preco_venda,
        stock: p.quantidade_atual
      }))
    }
  } catch (e) {
    console.error(e)
  }
}
fetchProducts()

const filteredProducts = computed(() => {
  let result = rows.value
  if (filterLowStock.value) result = result.filter(p => p.stock < 20)
  if (search.value) {
    const lowerQuery = search.value.toLowerCase()
    result = result.filter(p => 
      p.product.toLowerCase().includes(lowerQuery) || 
      p.sku.toLowerCase().includes(lowerQuery) ||
      p.category.toLowerCase().includes(lowerQuery)
    )
  }
  return result
})

const openCreateDialog = () => {
  isEditing.value = false
  const autoSku = 'SKU-' + Date.now().toString().slice(-6)
  productForm.value = { id: null, sku: autoSku, product: '', category: 'Eletrônicos', price: '', stock: 0 }
  isProductDialogOpen.value = true
}

const openEditDialog = (product) => {
  isEditing.value = true
  productForm.value = { ...product }
  isProductDialogOpen.value = true
}

const saveProduct = async () => {
  if (productForm.value.stock <= 0) {
    if (productForm.value.id) removeProduct(productForm.value)
    isProductDialogOpen.value = false
    $q.notify({ message: 'Produto removido pois o estoque chegou a zero.', color: 'warning', icon: 'info' })
    return
  }

  if (isEditing.value) {
    const index = rows.value.findIndex(p => p.id === productForm.value.id)
    if (index !== -1) rows.value[index] = { ...productForm.value }
    $q.notify({ message: 'Produto atualizado.', color: 'positive', icon: 'check' })
  } else {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/produtos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome: productForm.value.product,
          sku: productForm.value.sku,
          quantidade_atual: productForm.value.stock,
          preco_venda: parseFloat(productForm.value.price || 0)
        })
      })
      if (res.ok) {
        const data = await res.json()
        productForm.value.id = data.id_produto
        rows.value.unshift({ ...productForm.value })
        $q.notify({ message: 'Produto adicionado com sucesso.', color: 'positive', icon: 'check' })
      }
    } catch(e) {}
  }
  isProductDialogOpen.value = false
}

const removeProduct = async (product) => {
  rows.value = rows.value.filter(p => p.id !== product.id)
  try {
    await fetch(`http://127.0.0.1:8000/api/v1/produtos/${product.id}`, { method: 'DELETE' })
  } catch(e) {}
  $q.notify({ message: 'Produto excluído.', color: 'negative', icon: 'delete' })
}
</script>
