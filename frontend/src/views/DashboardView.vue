<template>
  <div>
    <!-- Top Stats Row -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      
      <q-card flat bordered class="rounded-2xl border-slate-200">
        <q-card-section class="p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="text-slate-500 font-medium flex items-center gap-2">
              <q-icon name="payments" size="20px" />
              Faturamento Total
            </div>
          </div>
          <div class="text-4xl font-bold text-dark mb-2">R$ 156.200,44</div>
          <div class="flex items-center text-sm gap-2">
            <span class="text-positive flex items-center bg-positive/10 px-2 py-0.5 rounded-full font-medium">
              <q-icon name="trending_up" size="16px" class="mr-1" />
              +16%
            </span>
            <span class="text-slate-400">vs último mês</span>
          </div>
        </q-card-section>
      </q-card>

      <q-card flat bordered class="rounded-2xl border-slate-200">
        <q-card-section class="p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="text-slate-500 font-medium flex items-center gap-2">
              <q-icon name="shopping_bag" size="20px" />
              Total de Pedidos
            </div>
          </div>
          <div class="text-4xl font-bold text-dark mb-2">10.362</div>
          <div class="flex items-center text-sm gap-2">
            <span class="text-negative flex items-center bg-negative/10 px-2 py-0.5 rounded-full font-medium">
              <q-icon name="trending_down" size="16px" class="mr-1" />
              -2.4%
            </span>
            <span class="text-slate-400">vs último mês</span>
          </div>
        </q-card-section>
      </q-card>

      <q-card flat bordered class="rounded-2xl border-slate-200">
        <q-card-section class="p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="text-slate-500 font-medium flex items-center gap-2">
              <q-icon name="inventory_2" size="20px" />
              Estoque Baixo
            </div>
          </div>
          <div class="text-4xl font-bold text-warning mb-2">231</div>
          <div class="flex items-center text-sm gap-2">
            <span class="text-warning flex items-center bg-warning/10 px-2 py-0.5 rounded-full font-medium">
              <q-icon name="warning_amber" size="16px" class="mr-1" />
              Atenção
            </span>
            <span class="text-slate-400">Requer reposição</span>
          </div>
        </q-card-section>
      </q-card>

    </div>

    <!-- Middle Content Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      
      <!-- Chart Area -->
      <q-card flat bordered class="rounded-2xl border-slate-200 lg:col-span-2">
        <q-card-section class="p-6 pb-2 border-b border-slate-100 flex justify-between items-center">
          <div class="text-lg font-bold text-dark">Resumo de Faturamento</div>
          <div class="flex items-center gap-2">
            <q-btn-group rounded flat outline class="border border-slate-200">
              <q-btn :outline="timeRange === 'M'" :flat="timeRange !== 'M'" @click="timeRange = 'M'" :color="timeRange === 'M' ? 'primary' : 'slate-500'" label="Mês" class="px-3" />
              <q-btn :outline="timeRange === 'Y'" :flat="timeRange !== 'Y'" @click="timeRange = 'Y'" :color="timeRange === 'Y' ? 'primary' : 'slate-500'" label="Ano" class="px-3" />
              <q-btn :outline="timeRange === 'All'" :flat="timeRange !== 'All'" @click="timeRange = 'All'" :color="timeRange === 'All' ? 'primary' : 'slate-500'" label="Tudo" class="px-3" />
            </q-btn-group>
            <q-btn flat icon="download" label="Exportar" class="text-slate-600 bg-slate-50 border border-slate-200 rounded-xl px-4 py-1" no-caps @click="exportBillingXlsx" />
          </div>
        </q-card-section>
        <q-card-section class="p-6">
          <div class="h-[300px] w-full mt-2">
            <LineChart :data="chartData" :options="chartOptions" />
          </div>
        </q-card-section>
      </q-card>

      <!-- Top Customers (from store) -->
      <q-card flat bordered class="rounded-2xl border-slate-200 lg:col-span-1">
        <q-card-section class="p-6 pb-2 border-b border-slate-100 flex justify-between items-center">
          <div class="text-lg font-bold text-dark">Top Clientes</div>
          <q-btn flat dense icon="chevron_right" color="primary" />
        </q-card-section>
        <q-list class="p-4" separator>
          <q-item v-for="(customer, index) in topCustomersList" :key="index" class="py-3 items-center">
            <q-item-section avatar>
              <q-avatar size="36px" color="primary" text-color="white" :class="'bg-opacity-' + (100 - index*15)">
                {{ customer.name.charAt(0) }}
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label class="font-bold text-dark">{{ customer.name }}</q-item-label>
              <q-item-label caption>{{ customer.email }}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <div class="font-bold text-dark">{{ customer.spentFormatted }}</div>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>

    </div>

    <!-- Recent Orders Table -->
    <q-card flat bordered class="rounded-2xl border-slate-200">
      <q-card-section class="px-6 py-5 border-b border-slate-100 flex justify-between items-center">
        <div class="text-lg font-bold text-dark">Últimos Pedidos</div>
        <q-btn flat :icon="filterFirstOrders ? 'check_box' : 'filter_list'" :color="filterFirstOrders ? 'primary' : 'secondary'" :label="filterFirstOrders ? 'Todos os pedidos' : 'Primeiros pedidos do dia'" class="bg-slate-50 hover:bg-slate-100 rounded-lg p-2 no-caps" @click="filterFirstOrders = !filterFirstOrders" />
      </q-card-section>
      
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 text-slate-500 text-sm border-b border-slate-200">
              <th class="p-4 pl-6 font-medium">Pedido</th>
              <th class="p-4 font-medium">Data</th>
              <th class="p-4 font-medium">Cliente</th>
              <th class="p-4 font-medium">Status</th>
              <th class="p-4 font-medium">Valor</th>
              <th class="p-4 pr-6 font-medium text-right">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in displayedOrders" :key="order.id" class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
              <td class="p-4 pl-6 font-medium text-dark">{{ order.id }}</td>
              <td class="p-4 text-slate-600">{{ order.date }}</td>
              <td class="p-4">
                <div class="flex items-center gap-3">
                  <q-avatar size="28px" :color="order.color" text-color="white">{{ order.initial }}</q-avatar>
                  <span class="font-medium text-dark">{{ order.customer }}</span>
                </div>
              </td>
              <td class="p-4">
                <span class="px-3 py-1 rounded-full text-xs font-bold" :class="statusColor(order.status)">
                  {{ order.status }}
                </span>
              </td>
              <td class="p-4 font-bold text-dark">R$ {{ order.amount.toFixed(2) }}</td>
              <td class="p-4 pr-6 text-right">
                <q-btn flat round dense icon="more_horiz" color="secondary">
                  <q-menu auto-close>
                    <q-list style="min-width:160px">
                      <q-item clickable v-ripple><q-item-section avatar><q-icon name="visibility" size="sm"/></q-item-section><q-item-section>Ver Pedido</q-item-section></q-item>
                      <q-item clickable v-ripple><q-item-section avatar><q-icon name="edit" size="sm"/></q-item-section><q-item-section>Editar</q-item-section></q-item>
                      <q-item clickable v-ripple class="text-negative"><q-item-section avatar><q-icon name="cancel" color="negative" size="sm"/></q-item-section><q-item-section>Cancelar</q-item-section></q-item>
                    </q-list>
                  </q-menu>
                </q-btn>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </q-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Line as LineChart } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Title, Tooltip, Filler, Legend
} from 'chart.js'
import * as XLSX from 'xlsx'
import { useCustomers } from '../composables/useCustomers'
import { useQuasar } from 'quasar'

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler, Legend
)

const $q = useQuasar()
const timeRange = ref('M')
const { topCustomers } = useCustomers()
const topCustomersList = computed(() => topCustomers())

const datasets = {
  'M': {
    labels: ['Dia 1', 'Dia 5', 'Dia 10', 'Dia 15', 'Dia 20', 'Dia 25', 'Dia 30'],
    dataThisYear: [1200, 4500, 8000, 11000, 15000, 16500, 19000],
    dataLastYear: [900, 3200, 6500, 9500, 12000, 14000, 16000]
  },
  'Y': {
    labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
    dataThisYear: [25000, 32000, 28000, 41000, 48000, 35000, 42000, 39000, 58000, 72000, 68000, 85000],
    dataLastYear: [21000, 28000, 24000, 35000, 40000, 28000, 31000, 35000, 45000, 52000, 55000, 62000]
  },
  'All': {
    labels: ['2021', '2022', '2023', '2024', '2025'],
    dataThisYear: [120000, 180000, 250000, 380000, 550000],
    dataLastYear: [80000, 120000, 180000, 250000, 380000]
  }
}

const chartData = computed(() => {
  const currentData = datasets[timeRange.value]
  return {
    labels: currentData.labels,
    datasets: [
      {
        label: 'Período Atual',
        backgroundColor: 'rgba(67, 56, 202, 0.1)',
        borderColor: '#4338ca',
        borderWidth: 3,
        pointBackgroundColor: '#fff',
        pointBorderColor: '#4338ca',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.4,
        data: currentData.dataThisYear
      },
      {
        label: 'Período Anterior',
        backgroundColor: 'rgba(139, 92, 246, 0.0)',
        borderColor: '#8b5cf6',
        borderWidth: 2,
        borderDash: [5, 5],
        pointBackgroundColor: '#fff',
        pointBorderColor: '#8b5cf6',
        pointBorderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 6,
        fill: false,
        tension: 0.4,
        data: currentData.dataLastYear
      }
    ]
  }
})

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1e293b',
      padding: 12,
      titleFont: { size: 13, family: 'Inter' },
      bodyFont: { size: 14, family: 'Inter', weight: 'bold' },
      displayColors: false,
      callbacks: {
        label: (context) => `R$${context.parsed.y.toLocaleString('pt-BR')}`
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f1f5f9', drawBorder: false },
      ticks: { color: '#64748b', font: { family: 'Inter', size: 11 }, callback: (value) => `R$${value/1000}k` }
    },
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { color: '#64748b', font: { family: 'Inter', size: 12 } }
    }
  },
  interaction: { intersect: false, mode: 'index' },
})

// Feature #4 – Export billing summary as xlsx with chart
const exportBillingXlsx = () => {
  const currentData = datasets[timeRange.value]
  const wb = XLSX.utils.book_new()

  // Build data rows
  const rows = [
    ['Período', 'Período Atual (R$)', 'Período Anterior (R$)'],
    ...currentData.labels.map((label, i) => [
      label,
      currentData.dataThisYear[i],
      currentData.dataLastYear[i]
    ])
  ]

  // Summary row
  const sumCurrent = currentData.dataThisYear.reduce((a, b) => a + b, 0)
  const sumLast = currentData.dataLastYear.reduce((a, b) => a + b, 0)
  rows.push([])
  rows.push(['TOTAL', sumCurrent, sumLast])
  rows.push(['Variação (%)', (((sumCurrent - sumLast) / sumLast) * 100).toFixed(1) + '%', ''])

  const ws = XLSX.utils.aoa_to_sheet(rows)

  // Column widths
  ws['!cols'] = [{ wch: 18 }, { wch: 22 }, { wch: 22 }]

  // Add chart data reference (SheetJS chart)
  const chartData2 = {
    name: 'Faturamento',
    data: currentData.dataThisYear,
    categories: currentData.labels
  }

  XLSX.utils.book_append_sheet(wb, ws, 'Resumo de Faturamento')

  // Second sheet: raw chart data for easy charting in Excel
  const chartRows = [
    ['Período', ...currentData.labels],
    ['Atual', ...currentData.dataThisYear],
    ['Anterior', ...currentData.dataLastYear]
  ]
  const wsChart = XLSX.utils.aoa_to_sheet(chartRows)
  wsChart['!cols'] = [{ wch: 12 }, ...currentData.labels.map(() => ({ wch: 14 }))]
  XLSX.utils.book_append_sheet(wb, wsChart, 'Dados do Gráfico')

  const rangeLabel = timeRange.value === 'M' ? 'Mes' : timeRange.value === 'Y' ? 'Ano' : 'Total'
  XLSX.writeFile(wb, `Faturamento_${rangeLabel}.xlsx`)
  $q.notify({ message: 'Relatório exportado com sucesso!', color: 'positive', icon: 'download' })
}

// Feature #3 – card menu export
const exportCardData = (card) => {
  $q.notify({ message: `Exportando dados de ${card}...`, color: 'primary', icon: 'download' })
}

const recentOrders = ref([
  { id: '#SQ12994', date: '01 Mar 2025', customer: 'João Silva', initial: 'J', color: 'primary', status: 'Concluído', amount: 320.00 },
  { id: '#SQ12995', date: '01 Mar 2025', customer: 'Maria Oliveira', initial: 'M', color: 'accent', status: 'Concluído', amount: 440.00 },
  { id: '#SQ12996', date: '02 Mar 2025', customer: 'Carlos Eduardo', initial: 'C', color: 'warning', status: 'Cancelado', amount: 220.00 },
  { id: '#SQ12997', date: '03 Mar 2025', customer: 'Ana Beatriz', initial: 'A', color: 'info', status: 'Pendente', amount: 510.00 },
  { id: '#SQ12998', date: '04 Mar 2025', customer: 'Fernanda Lima', initial: 'F', color: 'negative', status: 'Cancelado', amount: 600.00 },
  { id: '#SQ12999', date: '05 Mar 2025', customer: 'Roberto Costa', initial: 'R', color: 'secondary', status: 'Pendente', amount: 360.00 },
])

const filterFirstOrders = ref(false)

const displayedOrders = computed(() => {
  if (filterFirstOrders.value) {
    // Assuming the first orders of the day implies picking the oldest orders per date logic,
    // or simply showing a filtered set (mocked as the first 3 for simplicity since recentOrders is static).
    return recentOrders.value.slice().reverse().slice(0, 3) 
  }
  return recentOrders.value
})

const statusColor = (status) => {
  switch (status) {
    case 'Concluído': return 'bg-positive/10 text-positive'
    case 'Pendente': return 'bg-warning/10 text-warning'
    case 'Cancelado': return 'bg-negative/10 text-negative'
    default: return 'bg-slate-100 text-slate-500'
  }
}
</script>
