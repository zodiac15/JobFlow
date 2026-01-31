<template>
  <div class="bg-white p-8 rounded-2xl shadow-material-2 transform transition-all hover:shadow-material-3">
    <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-end">
      
      <!-- Keyword Input -->
      <div class="md:col-span-5 relative group">
        <label class="absolute -top-2 left-3 bg-white px-1 text-xs font-medium text-gray-500 transition-colors group-focus-within:text-primary">Keyword</label>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="e.g. Python Developer" 
          class="block w-full px-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:bg-white focus:border-primary focus:outline-none transition-colors text-gray-700 placeholder-gray-400"
        >
      </div>

      <!-- Location Input -->
      <div class="md:col-span-4 relative group">
        <label class="absolute -top-2 left-3 bg-white px-1 text-xs font-medium text-gray-500 transition-colors group-focus-within:text-primary">Location</label>
        <input 
          v-model="locationQuery" 
          type="text" 
          placeholder="e.g. Remote" 
           class="block w-full px-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:bg-white focus:border-primary focus:outline-none transition-colors text-gray-700 placeholder-gray-400"
        >
      </div>
      
      <!-- Action Buttons -->
      <div class="md:col-span-3 flex space-x-3">
        <button 
          @click="handleSearch" 
          class="flex-1 bg-primary hover:bg-primary-dark text-white font-medium py-3 px-6 rounded-xl shadow-md hover:shadow-lg transform active:scale-95 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          Search
        </button>
        <button 
          @click="handleScrape" 
          class="flex-none bg-secondary hover:bg-secondary-dark text-white font-medium p-3 rounded-xl shadow-md hover:shadow-lg transform active:scale-95 transition-all duration-200 focus:outline-none"
          :disabled="isScraping"
          title="Fetch New Jobs"
        >
            <svg v-if="!isScraping" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <svg v-else class="animate-spin h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search', 'scrape'])
const searchQuery = ref('')
const locationQuery = ref('')
const isScraping = ref(false)

const handleSearch = () => {
  emit('search', { q: searchQuery.value, location: locationQuery.value })
}

const handleScrape = async () => {
  isScraping.value = true
  await emit('scrape', { q: searchQuery.value, location: locationQuery.value })
  isScraping.value = false
}
</script>
