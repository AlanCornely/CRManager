import { ref } from 'vue'

const customers = ref([])

const fetchCustomers = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/v1/clientes/')
    if (res.ok) {
      customers.value = await res.json()
    }
  } catch (err) {
    console.error('Erro ao buscar clientes:', err)
  }
}

// Fetch immediately
fetchCustomers()

const formatSpent = (value) => {
  return 'R$ ' + Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

export function useCustomers() {
  const addCustomer = async (customer) => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/clientes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(customer)
      })
      if (res.ok) {
        const novo = await res.json()
        customers.value.unshift(novo)
      }
    } catch (e) {
      console.error(e)
    }
  }

  const updateCustomer = (updated) => {
    const index = customers.value.findIndex(c => c.id_cliente === updated.id_cliente)
    if (index !== -1) customers.value[index] = { ...updated }
  }

  const removeCustomer = (id) => {
    customers.value = customers.value.filter(c => c.id_cliente !== id)
  }

  const addSpent = (id, amount) => {
    const customer = customers.value.find(c => c.id_cliente === id)
    if (customer) {
      customer.spent = (customer.spent || 0) + Number(amount)
    }
  }

  const topCustomers = () => {
    return [...customers.value]
      .sort((a, b) => (b.spent || 0) - (a.spent || 0))
      .slice(0, 5)
      .map(c => ({
        ...c,
        cnpj: c.email,
        spentFormatted: formatSpent(c.spent)
      }))
  }

  return { customers, formatSpent, addCustomer, updateCustomer, removeCustomer, addSpent, topCustomers }
}
