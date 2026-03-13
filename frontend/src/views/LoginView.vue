<template>
  <div class="min-h-screen bg-slate-50 flex">
    <!-- Left Pattern/Image Side -->
    <div class="hidden lg:flex lg:w-1/2 bg-primary p-12 text-white flex-col justify-between relative overflow-hidden">
      <!-- Decorative background circles -->
      <div class="absolute -top-32 -left-32 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-0 w-full h-1/2 bg-gradient-to-t from-black/20 to-transparent"></div>
      
      <div class="relative z-10 flex items-center gap-3">
        <q-icon name="view_in_ar" size="48px" />
        <span class="text-3xl font-bold tracking-tight">FlowStock</span>
      </div>

      <div class="relative z-10 max-w-md">
        <h1 class="text-5xl font-bold leading-tight mb-6">Manage your inventory<br>like a pro.</h1>
        <p class="text-lg text-white/80">Streamline your supply chain, track orders in real-time, and get AI-powered insights to avoid stockouts.</p>
      </div>

      <div class="relative z-10 text-sm text-white/60">
        &copy; 2025 FlowStock Inc. All rights reserved.
      </div>
    </div>

    <!-- Right Login Side -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 lg:p-24 relative">
      <!-- Mobile Logo -->
      <div class="absolute top-8 left-8 flex lg:hidden items-center gap-2 text-primary">
        <q-icon name="view_in_ar" size="32px" />
        <span class="text-xl font-bold tracking-tight">FlowStock</span>
      </div>

      <div class="w-full max-w-md">
        <div class="mb-10 text-center lg:text-left">
          <h2 class="text-3xl font-bold text-dark mb-2">Welcome back</h2>
          <p class="text-slate-500">Please enter your details to sign in.</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
            <q-input outlined dense v-model="email" placeholder="Enter your email" type="email" class="bg-white rounded-lg">
              <template v-slot:prepend>
                <q-icon name="mail_outline" size="20px" class="text-slate-400" />
              </template>
            </q-input>
          </div>

          <div>
            <div class="flex justify-between mb-1">
              <label class="block text-sm font-medium text-slate-700">Password</label>
              <a href="#" class="text-sm text-primary font-medium hover:underline">Forgot password?</a>
            </div>
            <q-input outlined dense v-model="password" placeholder="••••••••" :type="showPassword ? 'text' : 'password'" class="bg-white rounded-lg">
              <template v-slot:prepend>
                <q-icon name="lock_outline" size="20px" class="text-slate-400" />
              </template>
              <template v-slot:append>
                <q-icon 
                  :name="showPassword ? 'visibility_off' : 'visibility'" 
                  class="cursor-pointer text-slate-400"
                  size="20px"
                  @click="showPassword = !showPassword"
                />
              </template>
            </q-input>
          </div>

          <div class="flex items-center">
            <q-checkbox v-model="rememberMe" label="Remember for 30 days" color="primary" dense class="text-sm text-slate-600" />
          </div>

          <q-btn unelevated color="primary" class="w-full rounded-lg py-3 font-semibold text-base" label="Sign in" type="submit" no-caps />
          
          <div class="relative py-4">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-slate-200"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-slate-50 text-slate-500">Or continue with</span>
            </div>
          </div>

          <q-btn 
            unelevated 
            class="w-full rounded-lg py-3 font-semibold text-base border border-slate-200 bg-white text-dark hover:bg-slate-50 transition-colors" 
            no-caps 
            @click="handleGoogleLogin"
          >
            <img src="https://www.google.com/favicon.ico" class="w-5 h-5 mr-3" alt="Google" />
            Sign in with Google
          </q-btn>
        </form>

        <p class="text-center text-sm text-slate-500 mt-8">
          Don't have an account? <a href="#" class="text-primary font-medium hover:underline">Sign up</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)

const handleLogin = () => {
  // Demo login
  localStorage.setItem('crm_authenticated', 'true')
  router.push('/')
}

const handleGoogleLogin = () => {
  // Demo Google SSO login
  localStorage.setItem('crm_authenticated', 'true')
  router.push('/')
}
</script>
