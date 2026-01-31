<template>
  <div class="min-h-screen bg-gray-50 pt-20 pb-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <svg class="w-8 h-8 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            Saved Jobs
        </h1>
      </div>

      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
           <div v-for="n in 6" :key="n" class="bg-white rounded-xl shadow-md h-64 animate-pulse"></div>
      </div>

      <div v-else-if="jobs.length === 0" class="text-center py-20 bg-white rounded-xl shadow-sm">
           <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
               <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
           </svg>
           <h3 class="mt-2 text-sm font-medium text-gray-900">No saved jobs</h3>
           <p class="mt-1 text-sm text-gray-500">Get started by searching for jobs and saving them.</p>
           <div class="mt-6">
               <router-link to="/" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark">
                   Find Jobs
               </router-link>
           </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" v-auto-animate>
          <JobCard v-for="job in jobs" :key="job.id" :job="job" :saved="true" @toggle-saved="removeJob" :matchScore="job.matchScore" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import JobCard from '../components/JobCard.vue'
import { fetchWithAuth } from '../utils/api'

const jobs = ref([])
const loading = ref(true)

const fetchSavedJobs = async () => {
    try {
        const response = await fetchWithAuth('http://localhost:5000/api/user/saved-jobs', {
            headers: { 'Content-Type': 'application/json' }
        })
        if (response.ok) {
            jobs.value = await response.json()
        }
    } catch (e) {
        console.error("Failed to fetch saved jobs", e)
    } finally {
        loading.value = false
    }
}

const removeJob = async (jobId) => {
    // Optimistic removal
    jobs.value = jobs.value.filter(j => j.id !== jobId)
    try {
         await fetchWithAuth(`http://localhost:5000/api/user/saved-jobs/${jobId}`, {
            method: 'POST'
        })
    } catch (e) {
        // Revert if failed (omitted for brevity)
    }
}

onMounted(() => {
    fetchSavedJobs()
})
</script>
