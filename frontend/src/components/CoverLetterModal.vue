<template>
  <Teleport to="body">
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      
      <!-- Background overlay -->
      <div @click="close" class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <!-- Modal panel -->
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
      <div class="inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        
        <!-- Header -->
        <div class="bg-gradient-to-r from-violet-600 to-indigo-600 px-4 py-5 sm:px-6">
          <div class="flex justify-between items-center">
             <h3 class="text-lg leading-6 font-medium text-white flex items-center" id="modal-title">
                <svg class="w-5 h-5 mr-2 text-yellow-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                AI Cover Letter Generator
             </h3>
             <button @click="close" class="text-white hover:text-gray-200 focus:outline-none">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
             </button>
          </div>
        </div>

        <!-- Body -->
        <div class="px-4 py-5 sm:p-6">
           <div v-if="loading" class="flex flex-col items-center justify-center py-12">
               <svg class="animate-spin h-10 w-10 text-primary mb-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
               <p class="text-gray-500 animate-pulse">Crafting your perfect letter...</p>
           </div>

           <div v-else-if="error" class="text-center py-8">
               <p class="text-red-500 mb-4">{{ error }}</p>
               <button @click="generateLetter" class="text-primary hover:text-indigo-700 font-medium">Try Again</button>
           </div>

           <div v-else>
               <textarea 
                  v-model="coverLetter" 
                  rows="12"
                  class="shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md font-mono text-gray-700 p-4 bg-gray-50"
               ></textarea>
               
               <div class="mt-4 flex justify-end space-x-3">
                   <button @click="copyToClipboard" class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                       <span v-if="copied">Copied!</span>
                       <span v-else>Copy to Clipboard</span>
                   </button>
                   <button @click="close" class="inline-flex justify-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                       Done
                   </button>
               </div>
           </div>
        </div>

      </div>
    </div>
  </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  job: Object
})

const emit = defineEmits(['close'])

const loading = ref(false)
const error = ref(null)
const coverLetter = ref('')
const copied = ref(false)

const close = () => {
    emit('close')
}

const generateLetter = async () => {
    if (!props.job) return
    
    loading.value = true
    error.value = null
    coverLetter.value = ''
    
    try {
        const response = await fetch('http://localhost:5000/api/ai/generate-cover-letter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                job_title: props.job.title,
                company_name: props.job.company,
                job_description: props.job.description || props.job.title // Fallback
            })
        })
        
        const data = await response.json()
        if (response.ok) {
            coverLetter.value = data.cover_letter
        } else {
            error.value = data.error || 'Failed to generate letter'
        }
    } catch (e) {
        error.value = 'Network error occurred'
    } finally {
        loading.value = false
    }
}

const copyToClipboard = () => {
    navigator.clipboard.writeText(coverLetter.value)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
}

// Generate when opened
watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        generateLetter()
    }
})
</script>
