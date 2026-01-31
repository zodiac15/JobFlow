<template>
  <nav class="bg-primary text-white shadow-material-2 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center space-x-3 cursor-pointer group" @click="$router.push('/')">
           <div class="relative w-10 h-10 transition-transform group-hover:scale-110 duration-200">
               <img :src="logo" alt="JobFlow" class="w-full h-full object-contain filter drop-shadow-md pb-1">
           </div>
           <span class="font-heading font-bold text-2xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-200 group-hover:text-white transition-all">JobFlow</span>
        </div>
        <div class="flex items-center space-x-4">
            <template v-if="user">
                <router-link to="/profile" class="text-white hover:bg-primary-dark px-3 py-2 rounded-md font-medium transition-colors">
                    Profile
                </router-link>
                <router-link to="/saved-jobs" class="text-white hover:bg-primary-dark px-3 py-2 rounded-md font-medium transition-colors">
                    Saved Jobs
                </router-link>
                <router-link to="/tracker" class="text-white hover:bg-primary-dark px-3 py-2 rounded-md font-medium transition-colors">
                    Tracker
                </router-link>
                 <button @click="logout" class="text-white hover:bg-primary-dark px-3 py-2 rounded-md font-medium transition-colors">
                    Logout
                </button>
            </template>
            <template v-else>
                 <router-link to="/login" class="text-white hover:bg-primary-dark px-3 py-2 rounded-md font-medium transition-colors">
                    Login
                </router-link>
            </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchWithAuth } from '../utils/api'
import logo from '@/assets/logo.png' // Explicit import

const router = useRouter()
const route = useRoute()
const user = ref(JSON.parse(localStorage.getItem('user')))

// Watch for route changes to update user state (e.g. after login/logout redirect)
watch(route, () => {
    user.value = JSON.parse(localStorage.getItem('user'))
})

// Also listen for storage events (if multiple tabs or direct events are used)
onMounted(() => {
    user.value = JSON.parse(localStorage.getItem('user'))
})

const logout = async () => {
    // Clear local storage immediately
    localStorage.removeItem('user')
    user.value = null
    
    try {
        await fetchWithAuth('http://localhost:5000/api/auth/logout', { 
            method: 'POST'
        })
    } catch (e) {
        console.error("Logout failed", e)
    }
    
    router.push('/login')
}
</script>
