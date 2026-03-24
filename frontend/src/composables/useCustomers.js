import { ref } from 'vue'

// Global reactive customer store (singleton pattern)
const customers = ref([
  { id: 1, name: 'TechSolutions Ltda', email: 'contato@techsolutions.com', phone: '(11) 98765-0100', role: 'Cliente', spent: 124500.00, cep: '', houseNumber: '' },
  { id: 2, name: 'Mercado Fácil SA', email: 'vendas@mercadofacil.com.br', phone: '(21) 99888-0101', role: 'Distribuidora', spent: 89200.50, cep: '', houseNumber: '' },
  { id: 3, name: 'Carlos Eduardo', email: 'carlos.ed@example.com', phone: '(31) 98888-0102', role: 'Sócio', spent: 0, cep: '', houseNumber: '' },
  { id: 4, name: 'Lojas Delta', email: 'compras@lojasdelta.com', phone: '(41) 97777-0103', role: 'Cliente', spent: 42800.00, cep: '', houseNumber: '' },
  { id: 5, name: 'Administração Flow', email: 'admin@crmanager.com', phone: '(11) 95555-0104', role: 'Dono', spent: 0, cep: '', houseNumber: '' },
])

const formatSpent = (value) => {
  return 'R$ ' + Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

export function useCustomers() {
  const addCustomer = (customer) => {
    customer.id = Date.now()
    customer.spent = 0
    customers.value.unshift({ ...customer })
  }

  const updateCustomer = (updated) => {
    const index = customers.value.findIndex(c => c.id === updated.id)
    if (index !== -1) customers.value[index] = { ...updated }
  }

  const removeCustomer = (id) => {
    customers.value = customers.value.filter(c => c.id !== id)
  }

  const addSpent = (customerId, amount) => {
    const customer = customers.value.find(c => c.id === customerId)
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
