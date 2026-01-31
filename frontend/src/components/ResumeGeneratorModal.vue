<template>
  <Transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-gray-900/75 backdrop-blur-sm transition-opacity" @click="$emit('close')"></div>

      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div class="relative transform overflow-hidden rounded-2xl bg-white text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-3xl border border-gray-100">
          
          <!-- Header -->
          <div class="bg-gradient-to-r from-primary to-primary-dark px-6 py-4 flex justify-between items-center">
             <h3 class="text-xl font-bold text-white flex items-center">
                 <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                 AI Resume Tailor
             </h3>
             <button @click="$emit('close')" class="text-white/80 hover:text-white transition-colors">
                 <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
             </button>
          </div>

          <!-- Body -->
          <div class="px-8 py-8">
            
            <!-- Step 1: Selection Mode -->
            <div v-if="step === 1">
                <div class="text-center mb-8">
                    <h4 class="text-2xl font-bold text-gray-900 mb-2">Resume Source</h4>
                    <p class="text-gray-500">Choose a base resume to start tailoring.</p>
                </div>

                <!-- Case A: Profile Available and Selected -->
                <div v-if="useSavedProfile && userProfile" class="max-w-md mx-auto">
                    <div class="bg-gray-50 border border-gray-200 rounded-xl p-6 text-left hover:shadow-md transition-shadow">
                        <div class="flex items-center justify-between mb-4">
                            <span class="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-0.5 rounded">Saved Profile</span>
                            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                        </div>
                        <h5 class="font-bold text-lg text-gray-900">{{ userProfile.name || 'Your Profile' }}</h5>
                        <p class="text-sm text-gray-500">{{ userProfile.title || 'No Job Title' }}</p>
                        
                        <div class="mt-4 flex flex-wrap gap-2">
                             <span v-if="userProfile.skills && userProfile.skills.length" class="text-xs bg-white border border-gray-200 px-2 py-1 rounded">{{ userProfile.skills.length }} Skills</span>
                             <span v-if="userProfile.experience && userProfile.experience.length" class="text-xs bg-white border border-gray-200 px-2 py-1 rounded">{{ userProfile.experience.length }} Experience Entries</span>
                        </div>
                    </div>

                    <div class="mt-8 space-y-4">
                        <button @click="useProfileAsResume" class="w-full py-3 bg-primary text-white rounded-xl font-bold hover:bg-primary-dark transition-colors shadow-lg">
                            Continue with Profile
                        </button>
                        <button @click="switchToUpload" class="text-sm text-gray-500 hover:text-gray-700 underline">
                            or upload a different file
                        </button>
                    </div>
                </div>
                
                <!-- Case B: Upload Mode -->
                <div v-else>
                    <div 
                        class="border-2 border-dashed border-gray-300 rounded-xl p-10 text-center hover:border-primary hover:bg-primary/5 transition-all cursor-pointer group"
                        @click="$refs.fileInput.click()"
                        @dragover.prevent
                        @drop.prevent="handleDrop"
                    >
                        <input type="file" ref="fileInput" class="hidden" accept=".pdf,.docx" @change="handleFileSelect">
                        <div class="mb-4 text-gray-400 group-hover:text-primary transition-colors">
                            <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                        </div>
                        <p class="text-lg font-medium text-gray-700 mb-1">Click to upload or drag and drop</p>
                        <p class="text-sm text-gray-500">PDF or DOCX (Max 5MB)</p>
                    </div>

                    <div v-if="userProfile" class="mt-6 text-center">
                        <button @click="useSavedProfile = true" class="text-sm text-primary hover:text-primary-dark font-medium">
                            Use your saved profile instead
                        </button>
                    </div>

                    <div v-if="uploadError" class="mt-4 text-red-600 bg-red-50 p-3 rounded-lg text-sm text-center">
                        {{ uploadError }}
                    </div>
                </div>
            </div>

            <!-- Step 2: Job Description -->
            <div v-if="step === 2">
                <div class="mb-6">
                    <h4 class="text-xl font-bold text-gray-900 mb-2">Job Description</h4>
                    <p class="text-gray-500 text-sm mb-4">Edit formatting if needed. This will be used to tailor your resume.</p>
                    <textarea 
                        v-model="localJobDescription" 
                        class="w-full h-64 p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent resize-none bg-gray-50 text-sm leading-relaxed"
                        placeholder="Paste job description here..."
                    ></textarea>
                </div>
                <div class="flex justify-end space-x-3">
                    <button @click="step = 1" class="px-6 py-2.5 rounded-lg text-gray-600 hover:bg-gray-100 font-medium transition-colors">Back</button>
                    <button @click="generateResume" class="px-8 py-2.5 rounded-lg bg-primary text-white font-bold shadow-lg hover:bg-primary-dark transition-all transform hover:-translate-y-0.5">
                        Generate Resume
                    </button>
                </div>
            </div>

            <!-- Step 3: Loading -->
            <div v-if="step === 3" class="text-center py-12">
                <div class="relative w-24 h-24 mx-auto mb-8">
                    <div class="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
                    <div class="absolute inset-0 border-4 border-primary rounded-full border-t-transparent animate-spin"></div>
                    <div class="absolute inset-0 flex items-center justify-center">
                        <svg class="w-8 h-8 text-primary animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    </div>
                </div>
                <h4 class="text-2xl font-bold text-gray-900 mb-2">Crafting Your Resume...</h4>
                <p class="text-gray-500 animate-pulse">Analyzing job requirements • Matching skills • Formatting</p>
            </div>

            <!-- Step 4: Result -->
            <div v-if="step === 4" class="h-[70vh] flex flex-col">
                 <div class="flex justify-between items-center mb-4">
                     <h4 class="text-xl font-bold text-gray-900">Tailored Resume</h4>
                     <div class="flex space-x-2">
                         <button @click="copyToClipboard" class="flex items-center px-4 py-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 font-medium transition-colors text-sm">
                             <span v-if="copied">Copied!</span>
                             <span v-else class="flex items-center">
                                 <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
                                 Copy Markdown
                             </span>
                         </button>
                     </div>
                 </div>
                 
                 <div class="flex-1 overflow-y-auto bg-gray-50 rounded-xl p-6 border border-gray-200 shadow-inner">
                     <div v-html="renderedResume" class="prose max-w-none prose-sm prose-blue"></div>
                 </div>
                 
                 <div class="mt-6 flex justify-end">
                      <button @click="$emit('close')" class="px-6 py-2.5 rounded-lg bg-gray-200 text-gray-800 font-medium hover:bg-gray-300 transition-colors">Close</button>
                 </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { fetchWithAuth } from '../utils/api'
 // ... imports ...

// ... props, emits, state ...

const renderedResume = computed(() => {
    if (!generatedResumeMarkdown.value) return ''
    const rawHtml = marked(generatedResumeMarkdown.value)
    return DOMPurify.sanitize(rawHtml)
})

// ... rest of script ...

const copyToClipboard = () => {
    navigator.clipboard.writeText(generatedResumeMarkdown.value)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
