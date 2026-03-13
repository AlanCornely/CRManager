import { createApp } from 'vue'
import { Quasar } from 'quasar'
import { createPinia } from 'pinia'
import router from './router.js'
import App from './App.vue'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

// Import Tailwind css
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
  config: {
    brand: {
      primary: '#4338ca',
      secondary: '#64748b',
      accent: '#8b5cf6',
      dark: '#1e293b',
      positive: '#10b981',
      negative: '#ef4444',
      info: '#3b82f6',
      warning: '#f59e0b'
    }
  }
})

app.mount('#app')
