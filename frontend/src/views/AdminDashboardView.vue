<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- Sidebar -->
    <div class="w-64 bg-gray-900 text-white flex flex-col">
        <div class="p-6 text-2xl font-bold border-b border-gray-800">JobFlow Admin</div>
        <nav class="flex-1 p-4 space-y-2">
            <router-link to="/admin" class="block py-2.5 px-4 rounded hover:bg-gray-800" :class="$route.path === '/admin' ? 'bg-gray-800' : ''">Dashboard</router-link>
            <router-link to="/admin/jobs" class="block py-2.5 px-4 rounded hover:bg-gray-800" :class="$route.path === '/admin/jobs' ? 'bg-gray-800' : ''">Jobs</router-link>
            <router-link to="/admin/users" class="block py-2.5 px-4 rounded hover:bg-gray-800" :class="$route.path === '/admin/users' ? 'bg-gray-800' : ''">Users</router-link>
            <router-link to="/" class="block py-2.5 px-4 rounded hover:bg-gray-800 mt-8 text-gray-400">Back to App</router-link>
        </nav>
        <div class="p-4 border-t border-gray-800">
            <button @click="logout" class="w-full text-left py-2 px-4 hover:bg-gray-800 rounded">Logout</button>
        </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 p-10">
        <h1 class="text-3xl font-bold mb-8">System Overview</h1>
        
        <div v-if="loading" class="text-gray-500">Loading stats...</div>
        <div v-else-if="error" class="text-red-500">{{ error }}</div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <!-- Stat Card -->
            <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <div class="text-gray-500 text-sm font-medium uppercase">Total Users</div>
                <div class="text-3xl font-bold text-gray-900 mt-2">{{ stats.users }}</div>
            </div>
             <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <div class="text-gray-500 text-sm font-medium uppercase">Total Jobs</div>
                <div class="text-3xl font-bold text-gray-900 mt-2">{{ stats.jobs }}</div>
            </div>
             <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <div class="text-gray-500 text-sm font-medium uppercase">Applications</div>
                <div class="text-3xl font-bold text-gray-900 mt-2">{{ stats.applications }}</div>
            </div>
        </div>

        <!-- User List Preview -->
        <h2 class="text-xl font-bold mb-4">Registered Users</h2>
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                         <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Resume</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="user in users" :key="user.id">
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{{ user.id }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ user.name || 'N/A' }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <span v-if="user.is_admin" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">Admin</span>
                            <span v-else class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">User</span>
                        </td>
                         <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <span v-if="user.has_resume" class="text-green-600">Yes</span>
                            <span v-else class="text-gray-400">No</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fetchWithAuth } from '../utils/api'

const router = useRouter()
const stats = ref({ users: 0, jobs: 0, applications: 0 })
const users = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
    try {
        await Promise.all([fetchStats(), fetchUsers()])
    } catch (e) {
        error.value = "Failed to load admin data. ensure you are an admin."
    } finally {
        loading.value = false
    }
})

const fetchStats = async () => {
    const res = await fetchWithAuth('http://localhost:5000/api/admin/stats')
    if (res.status === 403) throw new Error('Unauthorized')
    if (!res.ok) throw new Error('Failed to fetch stats')
    stats.value = await res.json()
}

const fetchUsers = async () => {
    const res = await fetchWithAuth('http://localhost:5000/api/admin/users')
    if (res.status === 403) throw new Error('Unauthorized')
    if (!res.ok) throw new Error('Failed to fetch users')
    users.value = await res.json()
}

const logout = async () => {
    await fetchWithAuth('http://localhost:5000/api/auth/logout', { method: 'POST' })
    localStorage.removeItem('user')
    router.push('/login')
}
</script>
