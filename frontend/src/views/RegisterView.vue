<template>
  <div class="min-h-screen bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
     <!-- Abstract Shapes -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div class="absolute top-20 right-20 w-72 h-72 rounded-full bg-white opacity-10 blur-3xl animate-wiggle"></div>
        <div class="absolute -bottom-20 -left-20 w-96 h-96 rounded-full bg-blue-500 opacity-20 blur-3xl"></div>
    </div>

    <div class="sm:mx-auto sm:w-full sm:max-w-md relative z-10 animate-fade-in-up">
      <div class="text-center mb-8">
         <h2 class="text-4xl font-extrabold text-white tracking-tight">Join JobFlow</h2>
         <p class="mt-2 text-sm text-purple-100">
            Start your journey to a better career
         </p>
      </div>

      <div class="bg-white/95 backdrop-blur-xl py-8 px-4 shadow-2xl rounded-2xl sm:px-10 border border-white/50">
        <form class="space-y-6" @submit.prevent="handleRegister">
           <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
            <div class="mt-1">
              <input v-model="name" id="name" name="name" type="text" autocomplete="name" required 
                     class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                     placeholder="John Doe">
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
            <div class="mt-1">
              <input v-model="email" id="email" name="email" type="email" autocomplete="email" required 
                     class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                     placeholder="you@example.com">
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <div class="mt-1">
              <input v-model="password" id="password" name="password" type="password" autocomplete="new-password" required 
                     class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                     placeholder="Create a strong password">
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
                  Creating Account...
              </span>
              <span v-else>Register</span>
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
                  Already have an account?
                </span>
              </div>
            </div>

            <div class="mt-6">
                 <router-link to="/login" class="w-full flex justify-center py-3 px-4 border-2 border-primary/20 rounded-xl shadow-sm text-sm font-medium text-primary bg-white hover:bg-primary/5 transition-colors">
                    Sign in
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

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

const handleRegister = async () => {
    loading.value = true
    error.value = ''
    try {
        const response = await fetchWithAuth('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                name: name.value,
                email: email.value, 
                password: password.value 
            })
        })
        const data = await response.json()
        
        if (response.ok) {
            localStorage.setItem('user', JSON.stringify(data.user))
            router.push('/profile')
        } else {
            error.value = data.error || 'Registration failed'
        }
    } catch (e) {
        error.value = 'An error occurred. Please try again.'
    } finally {
        loading.value = false
    }
}
</script>
