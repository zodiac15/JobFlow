<template>
  <div>
    <!-- Modern Hero Section -->
    <div class="relative bg-gradient-to-r from-violet-600 to-indigo-600 pb-32 pt-16 rounded-b-[3rem] shadow-xl overflow-hidden">
      <!-- Decor items -->
      <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
          <div class="absolute -top-24 -left-20 w-96 h-96 rounded-full bg-white opacity-10 blur-3xl"></div>
          <div class="absolute top-32 right-10 w-72 h-72 rounded-full bg-fuchsia-400 opacity-20 blur-3xl"></div>
      </div>
    
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
        <h1 class="text-4xl md:text-6xl font-extrabold tracking-tight mb-6 animate-fade-in-down h-20 md:h-24">
          Find Your Next Job at <br class="md:hidden" />
          <TypewriterEffect :words="['Google', 'Netflix', 'Amazon', 'Microsoft', 'OpenAI', 'SpaceX']" />
        </h1>
        <p class="text-xl md:text-2xl opacity-90 mb-10 max-w-2xl mx-auto font-light">
          Discover thousands of opportunities from LinkedIn, Naukri, and more.
        </p>
        
        <!-- Glassmorphism Stats -->
        <div class="flex justify-center gap-6 mb-8 text-sm font-medium opacity-80">
            <span class="flex items-center"><svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg> 500+ New Jobs</span>
            <span class="flex items-center"><svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg> Top Companies</span>
        </div>
      </div>
    </div>

    <!-- Main Content (Overlapping Hero) -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-24 relative z-20">
      
      <!-- Search & Scrape Card -->
      <div class="bg-white/80 backdrop-blur-md rounded-2xl shadow-material-3 p-6 md:p-8 mb-12 border border-white/50">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
             <div class="md:col-span-2 relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
                <input 
                    v-model="searchQuery"
                    type="text" 
                    placeholder="Job title, keywords, or company" 
                    class="pl-10 block w-full border-gray-200 rounded-xl bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary focus:border-transparent transition-all p-3 shadow-inner"
                    @keyup.enter="fetchJobs"
                >
             </div>
             <div>
                <input 
                    v-model="locationQuery"
                    type="text" 
                    placeholder="Location (e.g. Remote)" 
                    class="block w-full border-gray-200 rounded-xl bg-gray-50 focus:bg-white focus:ring-2 focus:ring-primary focus:border-transparent transition-all p-3 shadow-inner"
                >
             </div>
             <div class="flex space-x-2">
                 <button 
                    @click="fetchJobs" 
     class="flex-1 bg-primary text-white font-bold py-3 px-6 rounded-xl shadow-lg shadow-primary/30 hover:bg-primary-dark hover:shadow-primary/50 active:scale-95 transform transition-all duration-200 flex justify-center items-center"
                    :disabled="loading"
                 >
                    <span v-if="loading" class="animate-spin mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                    <span v-else>Search</span>
                 </button>
             </div>
        </div>
      </div>

      <!-- Job List -->
      <div class="mb-4 flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-800">Latest Opportunities</h2>
        <span class="text-gray-500 text-sm bg-gray-100 px-3 py-1 rounded-full">{{ filteredJobs.length }} Jobs Found</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-20" v-auto-animate>
        <!-- Skeleton Loaders -->
        <template v-if="loading">
            <SkeletonJobCard v-for="n in 6" :key="n" />
        </template>
        
        <!-- Job Cards -->
        <template v-else>
            <JobCard 
                v-for="(job, index) in filteredJobs" 
                :key="job.id" 
                :job="job"
                :saved="savedJobIds.includes(job.id)"
                @toggle-saved="toggleSaved"
                class="animate-fade-in-up"
                :style="{ animationDelay: `${index * 100}ms` }"
            />
            
            <div v-if="filteredJobs.length === 0" class="col-span-full py-12 text-center text-gray-400">
                <div class="bg-gray-50 rounded-full h-24 w-24 flex items-center justify-center mx-auto mb-4">
                    <svg class="h-10 w-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <p class="text-xl font-medium text-gray-600">No jobs found.</p>
                <p>Try scraping for new listings!</p>
            </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import JobCard from '../components/JobCard.vue'
import SkeletonJobCard from '../components/SkeletonJobCard.vue'
import TypewriterEffect from '../components/TypewriterEffect.vue'
import { fetchWithAuth } from '../utils/api'

const jobs = ref([])
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const locationQuery = ref('')
const savedJobIds = ref([])

const filteredJobs = computed(() => {
    return jobs.value
})

onMounted(() => {
  fetchJobs()
  fetchSavedJobIds()
})

const fetchSavedJobIds = async () => {
    try {
        const response = await fetchWithAuth('/api/user/saved-jobs/ids')
        if (response.ok) {
            savedJobIds.value = await response.json()
        }
    } catch (e) {
        console.error("Failed to fetch saved IDs", e)
    }
}

const toggleSaved = async (jobId) => {
    // Optimistic UI update
    const index = savedJobIds.value.indexOf(jobId)
    if (index === -1) {
        savedJobIds.value.push(jobId)
    } else {
        savedJobIds.value.splice(index, 1)
    }

    try {
        await fetchWithAuth(`/api/user/saved-jobs/${jobId}`, {
            method: 'POST'
        })
    } catch (e) {
        // Revert if failed
        if (index === -1) {
            savedJobIds.value = savedJobIds.value.filter(id => id !== jobId)
        } else {
             savedJobIds.value.push(jobId)
        }
    }
}

const fetchJobs = async (filters = {}, isRetry = false) => {
  loading.value = true
  error.value = null
  try {
    const params = new URLSearchParams()
    if (filters.q || searchQuery.value) params.append('q', filters.q || searchQuery.value)
    if (filters.location || locationQuery.value) params.append('location', filters.location || locationQuery.value)
    
    // 1. First fetch attempt
    const response = await fetchWithAuth(`/api/jobs?${params.toString()}`)
    if (!response.ok) throw new Error('Failed to fetch jobs')
    const fetchedJobs = await response.json()
    jobs.value = fetchedJobs

    // 2. Check Auto-Scrape Conditions (Only if not already retrying)
    if (!isRetry) {
        let shouldScrape = false
        const now = new Date()
        
        if (fetchedJobs.length < 10) {
            shouldScrape = true
        } else {
            // Check if latest job is older than 24 hours
            // Assuming jobs are sorted desc by backend
            const latestJobDate = new Date(fetchedJobs[0].date_posted)
            const diffMs = now - latestJobDate
            const diffHours = diffMs / (1000 * 60 * 60)
            
            if (diffHours > 24) {
                shouldScrape = true
            }
        }
        
        if (shouldScrape) {
            await triggerScrape({
                q: searchQuery.value,
                location: locationQuery.value
            })
            // Recursive call after scraping, marked as retry to prevent infinite loop
            return fetchJobs(filters, true) 
        }
    }

  } catch (e) {
    error.value = e.message
  } finally {
      // Only set loading false if we aren't about to recursive call
      // actually, triggerScrape handles its own loading state, so we might flicker. 
      // simple approach:
      loading.value = false
  }
}

// Scrape logic simply calls backend
const triggerScrape = async (filters) => {
  // We don't set global loading here to avoid UI flickering if we want to show a specific message
  // But let's use a separate status for clarity "scrapingStatus"
  loading.value = true 
  try {
    const response = await fetchWithAuth('/api/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(filters)
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.error || 'Scraping failed')
    // We don't fetchJobs here, we let the caller do it
  } catch (e) {
    console.error("Auto-scrape failed:", e)
    // We swallow scrape errors to show whatever cached data we might have had, or empty state
  }
}

onMounted(() => {
  fetchJobs()
})
</script>

<style>
/* Local styles removed in favor of Tailwind config */
</style>
