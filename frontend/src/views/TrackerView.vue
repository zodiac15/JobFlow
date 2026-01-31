<template>
  <div class="min-h-screen bg-gray-50 pt-20 pb-12 px-4 sm:px-6 lg:px-8 overflow-x-auto">
    <div class="max-w-7xl mx-auto min-w-[1000px]">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <svg class="w-8 h-8 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            Application Tracker
        </h1>
        <button @click="showAddModal = true" class="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-md shadow-sm text-sm font-medium transition-colors">
            + Add Application
        </button>
      </div>

      <div class="grid grid-cols-4 gap-6">
          <div v-for="col in columns" :key="col.id" class="bg-gray-100 rounded-xl p-4 flex flex-col h-full min-h-[500px]">
              <h3 class="text-lg font-semibold text-gray-700 mb-4 px-2">{{ col.title }} ({{ getAppsByStatus(col.id).length }})</h3>
              
              <div class="space-y-4 flex-1" v-auto-animate>
                  <div v-for="app in getAppsByStatus(col.id)" :key="app.id" class="bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow relative group">
                      <h4 class="font-bold text-gray-900">{{ app.title }}</h4>
                      <p class="text-sm text-gray-600">{{ app.company }}</p>
                      <p class="text-xs text-gray-400 mt-2">{{ formatDate(app.date_applied) }}</p>
                      
                      <!-- Quick Actions -->
                      <div class="mt-3 flex justify-between items-center opacity-0 group-hover:opacity-100 transition-opacity">
                            <select @change="updateStatus(app, $event.target.value)" class="text-xs border-gray-300 rounded shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50">
                                <option v-for="c in columns" :key="c.id" :value="c.id" :selected="c.id === app.status">{{ c.title }}</option>
                            </select>
                            <button @click="deleteApp(app.id)" class="text-red-500 hover:text-red-700">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                            </button>
                      </div>
                  </div>
              </div>
          </div>
      </div>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-xl max-w-md w-full p-6 shadow-2xl">
            <h2 class="text-xl font-bold mb-4">Track New Application</h2>
            <form @submit.prevent="addApplication" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Company</label>
                    <input v-model="newApp.company" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Job Title</label>
                    <input v-model="newApp.title" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
                </div>
                 <div>
                    <label class="block text-sm font-medium text-gray-700">Status</label>
                    <select v-model="newApp.status" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
                        <option v-for="c in columns" :key="c.id" :value="c.id">{{ c.title }}</option>
                    </select>
                </div>
                <div class="flex justify-end gap-3 mt-6">
                    <button type="button" @click="showAddModal = false" class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Cancel</button>
                    <button type="submit" class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark">Add</button>
                </div>
            </form>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithAuth } from '../utils/api'

const columns = [
    { id: 'Applied', title: 'Applied' },
    { id: 'Interviewing', title: 'Interviewing' },
    { id: 'Offer', title: 'Offer' },
    { id: 'Rejected', title: 'Rejected' }
]

const applications = ref([])
const showAddModal = ref(false)
const newApp = ref({ company: '', title: '', status: 'Applied' })

const fetchApplications = async () => {
    try {
        const response = await fetchWithAuth('http://localhost:5000/api/user/applications', {
             headers: { 'Content-Type': 'application/json' }
        })
        if (response.ok) {
            applications.value = await response.json()
        }
    } catch (e) {
        console.error("Fetch failed", e)
    }
}

const getAppsByStatus = (status) => applications.value.filter(a => a.status === status)

const addApplication = async () => {
    try {
         const response = await fetchWithAuth('http://localhost:5000/api/user/applications', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify(newApp.value)
        })
        if (response.ok) {
            const added = (await response.json()).application
            applications.value.unshift(added)
            showAddModal.value = false
            newApp.value = { company: '', title: '', status: 'Applied' }
        }
    } catch (e) { console.error(e) }
}

const updateStatus = async (app, newStatus) => {
    app.status = newStatus // Optimistic
    try {
        await fetchWithAuth(`http://localhost:5000/api/user/applications/${app.id}`, {
             method: 'PUT',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({ status: newStatus })
        })
    } catch (e) { console.error(e) }
}

const deleteApp = async (id) => {
    if (!confirm("Delete this application?")) return
    applications.value = applications.value.filter(a => a.id !== id)
    try {
        await fetchWithAuth(`http://localhost:5000/api/user/applications/${id}`, {
             method: 'DELETE'
        })
    } catch (e) { console.error(e) }
}

const formatDate = (isoStr) => {
    return new Date(isoStr).toLocaleDateString()
}

onMounted(() => {
    fetchApplications()
})
</script>
