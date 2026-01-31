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
        <div class="p-4 border-t border-gray-800">
             <!-- Logout handled in dashboard but link is useful -->
        </div>
    </div>
    <!-- Spacer for fixed sidebar -->
    <div class="w-64"></div>

    <div class="flex-1 p-6">
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Job Management</h2>
        <div class="flex space-x-2">
            <button @click="openScraperModal" class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">Run Scraper</button>
        </div>
    </div>

    <div v-if="loading" class="text-center py-4">Loading jobs...</div>
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Company</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source</th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                <tr v-for="job in jobs" :key="job.id">
                    <td class="px-6 py-4">{{ job.title }}</td>
                    <td class="px-6 py-4">{{ job.company }}</td>
                    <td class="px-6 py-4">{{ job.source }}</td>
                    <td class="px-6 py-4 text-right">
                        <button @click="deleteJob(job.id)" class="text-red-600 hover:text-red-900">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Scraper Modal -->
    <div v-if="showScraperModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 class="text-lg font-bold mb-4">Run Job Scraper</h3>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Query</label>
                    <input v-model="scraperQuery" class="mt-1 block w-full border border-gray-300 rounded-md p-2">
                </div>
                <div>
                     <label class="block text-sm font-medium text-gray-700">Location</label>
                    <input v-model="scraperLocation" class="mt-1 block w-full border border-gray-300 rounded-md p-2">
                </div>
                <div v-if="scraperMessage" :class="scraperError ? 'text-red-600' : 'text-green-600'">{{ scraperMessage }}</div>
            </div>
            <div class="mt-6 flex justify-end space-x-3">
                <button @click="showScraperModal = false" class="px-4 py-2 border rounded">Close</button>
                <button @click="runScraper" :disabled="runningScraper" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
                    {{ runningScraper ? 'Running...' : 'Start Scraping' }}
                </button>
            </div>
        </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithAuth } from '../utils/api'

const jobs = ref([])
const loading = ref(true)
const showScraperModal = ref(false)
const scraperQuery = ref('developer')
const scraperLocation = ref('India')
const runningScraper = ref(false)
const scraperMessage = ref('')
const scraperError = ref(false)

const API = 'http://localhost:5000/api'

onMounted(() => fetchJobs())

const fetchJobs = async () => {
    try {
        const res = await fetchWithAuth(`${API}/jobs`)
        jobs.value = await res.json()
    } finally {
        loading.value = false
    }
}

const deleteJob = async (id) => {
    if(!confirm('Are you sure?')) return
    await fetchWithAuth(`${API}/admin/jobs/${id}`, { method: 'DELETE' })
    fetchJobs()
}

const openScraperModal = () => {
    showScraperModal.value = true
    scraperMessage.value = ''
}

const runScraper = async () => {
    runningScraper.value = true
    scraperMessage.value = ''
    try {
        const res = await fetchWithAuth(`${API}/admin/scraper/run`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ q: scraperQuery.value, location: scraperLocation.value })
        })
        const data = await res.json()
        scraperMessage.value = data.message
        scraperError.value = false
        fetchJobs()
    } catch (e) {
        scraperMessage.value = "Failed to run scraper"
        scraperError.value = true
    } finally {
        runningScraper.value = false
    }
}
</script>
