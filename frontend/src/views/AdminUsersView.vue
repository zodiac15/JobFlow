<template>
  <div class="min-h-screen bg-gray-100 flex">
      <!-- Sidebar (Duplicated for speed) -->
    <div class="w-64 bg-gray-900 text-white flex flex-col fixed h-full">
        <div class="p-6 text-2xl font-bold border-b border-gray-800">JobFlow Admin</div>
        <nav class="flex-1 p-4 space-y-2">
            <router-link to="/admin" class="block py-2.5 px-4 rounded hover:bg-gray-800" :class="$route.path === '/admin' ? 'bg-gray-800' : ''">Dashboard</router-link>
            <router-link to="/admin/jobs" class="block py-2.5 px-4 rounded hover:bg-gray-800" :class="$route.path === '/admin/jobs' ? 'bg-gray-800' : ''">Jobs</router-link>
            <router-link to="/admin/users" class="block py-2.5 px-4 rounded hover:bg-gray-800" :class="$route.path === '/admin/users' ? 'bg-gray-800' : ''">Users</router-link>
            <router-link to="/" class="block py-2.5 px-4 rounded hover:bg-gray-800 mt-8 text-gray-400">Back to App</router-link>
        </nav>
    </div>
    <!-- Spacer for fixed sidebar -->
    <div class="w-64"></div>

    <div class="flex-1 p-6">
    <h2 class="text-2xl font-bold mb-6">User Management</h2>
    <div v-if="loading" class="text-center py-4">Loading users...</div>
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                <tr v-for="user in users" :key="user.id">
                    <td class="px-6 py-4">{{ user.email }}</td>
                    <td class="px-6 py-4">{{ user.name }}</td>
                    <td class="px-6 py-4">
                        <span v-if="user.is_admin" class="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full">Admin</span>
                        <span v-else class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full">User</span>
                    </td>
                    <td class="px-6 py-4 text-right">
                        <button v-if="!user.is_admin" @click="deleteUser(user.id)" class="text-red-600 hover:text-red-900">Delete</button>
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
import { fetchWithAuth } from '../utils/api'

const users = ref([])
const loading = ref(true)
const API = 'http://localhost:5000/api'

onMounted(() => fetchUsers())

const fetchUsers = async () => {
    try {
        const res = await fetchWithAuth(`${API}/admin/users`)
        users.value = await res.json()
    } finally {
        loading.value = false
    }
}

const deleteUser = async (id) => {
    if(!confirm('Are you sure? This cannot be undone.')) return
    await fetchWithAuth(`${API}/admin/users/${id}`, { method: 'DELETE' })
    fetchUsers()
}
</script>
