<template>
  <div class="min-h-screen bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
     <!-- Abstract Shapes -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div class="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-white opacity-10 blur-3xl animate-wiggle"></div>
        <div class="absolute top-1/2 right-0 w-80 h-80 rounded-full bg-pink-400 opacity-20 blur-3xl"></div>
    </div>

    <div class="sm:mx-auto sm:w-full sm:max-w-md relative z-10 animate-fade-in-up">
      <div class="text-center mb-8">
         <h2 class="text-4xl font-extrabold text-white tracking-tight">Welcome Back</h2>
         <p class="mt-2 text-sm text-purple-100">
            Sign in to access your JobFlow dashboard
         </p>
      </div>

      <div class="bg-white/95 backdrop-blur-xl py-8 px-4 shadow-2xl rounded-2xl sm:px-10 border border-white/50">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
            <div class="mt-1 relative">
              <input v-model="email" id="email" name="email" type="email" autocomplete="email" required 
                     class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                     placeholder="you@example.com">
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <div class="mt-1 relative">
              <input v-model="password" id="password" name="password" type="password" autocomplete="current-password" required 
                     class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                     placeholder="••••••••">
            </div>
          </div>
          
           <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded">
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>
            <div class="text-sm">
              <a href="#" class="font-medium text-primary hover:text-primary-dark">
                Forgot password?
              </a>
            </div>
          </div>

          <div v-if="error" class="text-red-500 text-sm text-center bg-red-50 p-2 rounded-lg border border-red-100">
              {{ error }}
          </div>

          <div>
            <button type="submit" :disabled="loading" 
                    class="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-lg shadow-primary/30 text-sm font-bold text-white bg-gradient-to-r from-primary to-violet-600 hover:to-primary hover:shadow-primary/50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transform transition-all active:scale-95">
              <span v-if="loading" class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  Signing in...
              </span>
              <span v-else>Sign In</span>
            </button>
          </div>
        </form>
         <div class="mt-6">
            <div class="relative">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-white text-gray-500">
                  New to JobFlow?
                </span>
              </div>
            </div>

            <div class="mt-6">
                 <router-link to="/register" class="w-full flex justify-center py-3 px-4 border-2 border-primary/20 rounded-xl shadow-sm text-sm font-medium text-primary bg-white hover:bg-primary/5 transition-colors">
                    Create an account
                  </router-link>
            </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchWithAuth } from '../utils/api'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

const handleLogin = async () => {
    loading.value = true
    error.value = ''
    try {
        const response = await fetchWithAuth('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email.value, password: password.value })
        })
        const data = await response.json()
        
        if (response.ok) {
            localStorage.setItem('user', JSON.stringify(data.user))
            router.push('/profile')
        } else {
            error.value = data.error || 'Login failed'
        }
    } catch (e) {
        error.value = 'An error occurred. Please try again.'
    } finally {
        loading.value = false
    }
}
</script>
