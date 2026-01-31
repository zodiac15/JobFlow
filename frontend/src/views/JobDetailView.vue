<template>
  <div class="bg-white rounded-2xl shadow-material-3 overflow-hidden max-w-4xl mx-auto">
    <div v-if="loading" class="text-center py-20">
       <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-4 border-primary"></div>
    </div>
    
    <div v-else-if="error" class="p-10 text-center">
        <h2 class="text-2xl font-bold text-red-600 mb-4">Error Loading Job</h2>
        <p class="text-gray-600">{{ error }}</p>
        <router-link to="/" class="mt-6 inline-block text-primary hover:underline">Back to Search</router-link>
    </div>

    <div v-else-if="job">
        <!-- Header -->
        <div class="bg-primary text-white p-10 relative overflow-hidden">
            <div class="relative z-10">
                <div class="flex items-center space-x-3 mb-4 opacity-90">
                    <span class="bg-white/20 px-3 py-1 rounded-full text-sm font-medium backdrop-blur-sm">{{ job.source }}</span>
                    <span>{{ formatDate(job.date_posted) }}</span>
                </div>
                <h1 class="text-4xl font-extrabold mb-2 leading-tight">{{ job.title }}</h1>
                <div class="text-2xl font-medium opacity-90">{{ job.company }}</div>
                <div class="flex items-center mt-4 text-white/80">
                    <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    {{ job.location }}
                </div>
            </div>
            <!-- Decorative circle -->
            <div class="absolute -right-10 -bottom-20 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
        </div>
        
        <!-- Content -->
        <div class="p-10">
            <div class="prose max-w-none text-gray-700">
                <h3 class="text-2xl font-bold text-gray-900 mb-4">Job Description</h3>
                <p v-if="job.description" class="whitespace-pre-line leading-relaxed">{{ job.description }}</p>
                <div v-else class="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center text-gray-500 italic">
                    Full description is available on the source website.
                </div>
            </div>

            <!-- Action Bar -->
            <div class="mt-10 pt-8 border-t border-gray-100 flex items-center justify-between">
                <router-link to="/" class="text-gray-500 hover:text-gray-900 font-medium flex items-center transition-colors">
                    <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                    Back to Jobs
                </router-link>
                
                <button @click="showResumeModal = true" class="mr-4 text-primary font-bold hover:text-primary-dark transition-colors flex items-center">
                    <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    Tailor Resume
                </button>
                
                <a :href="job.url" target="_blank" class="bg-secondary hover:bg-secondary-dark text-white text-lg font-bold py-4 px-10 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300">
                    Apply Now
                </a>
            </div>
        </div>
        
        <ResumeGeneratorModal 
            :isOpen="showResumeModal" 
            :jobDescription="job.description" 
            @close="showResumeModal = false" 
        />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ResumeGeneratorModal from '../components/ResumeGeneratorModal.vue'

const route = useRoute()
const job = ref(null)
const loading = ref(true)
const error = ref(null)
const showResumeModal = ref(false)

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(async () => {
    try {
        const response = await fetch(`http://localhost:5000/api/jobs/${route.params.id}`)
        if (!response.ok) throw new Error('Job not found')
        job.value = await response.json()
        
        // SEO: Dynamic Title
        document.title = `${job.value.title} at ${job.value.company} - JobFlow`
        
        // SEO: Structured Data (JSON-LD)
        const schema = {
             "@context": "https://schema.org/",
             "@type": "JobPosting",
             "title": job.value.title,
             "description": job.value.description,
             "identifier": {
                 "@type": "PropertyValue",
                 "name": job.value.company,
                 "value": job.value.id
             },
             "datePosted": job.value.date_posted,
             "hiringOrganization": {
                 "@type": "Organization",
                 "name": job.value.company
             },
             "jobLocation": {
                 "@type": "Place",
                 "address": {
                     "@type": "PostalAddress",
                     "addressLocality": job.value.location || "Remote"
                 }
             }
         }
         
         const script = document.createElement('script')
         script.type = 'application/ld+json'
         script.text = JSON.stringify(schema)
         document.head.appendChild(script)

    } catch (e) {
        error.value = e.message
    } finally {
        loading.value = false
    }
})
</script>
