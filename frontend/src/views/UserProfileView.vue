<template>
  <div class="max-w-4xl mx-auto py-10 px-4">
    <div class="bg-white rounded-2xl shadow-material-2 overflow-hidden">
      <!-- Header -->
      <div class="bg-primary text-white p-8">
        <h1 class="text-3xl font-bold">User Profile</h1>
        <p class="opacity-90 mt-2">Manage your professional details and resume.</p>
      </div>
      
      <div class="p-8">
        <!-- CV Upload Section -->
        <div class="mb-10 bg-gray-50 border-2 border-dashed border-gray-300 rounded-xl p-8 text-center transition-colors hover:border-primary">
          <div v-if="uploading" class="py-4">
             <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
             <p class="mt-2 text-gray-600">Parsing CV...</p>
          </div>
          <div v-else>
            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <div class="mt-4 flex text-sm text-gray-600 justify-center">
              <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-primary hover:text-indigo-500 focus-within:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <span>Upload a CV (PDF/DOCX)</span>
                <input id="file-upload" name="file-upload" type="file" class="sr-only" @change="handleFileUpload" accept=".pdf,.docx">
              </label>
              <p class="pl-1">to autofill details</p>
            </div>
            <p v-if="uploadError" class="mt-2 text-sm text-red-600">{{ uploadError }}</p>
            <p v-if="parsedSuccess" class="mt-2 text-sm text-green-600">CV Parsed Successfully!</p>
          </div>
        </div>

        <!-- Personal Details Form -->
        <h2 class="text-xl font-bold text-gray-800 mb-4 border-b pb-2">Personal Information</h2>
        <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6 mb-8">
          <div class="sm:col-span-3">
            <label class="block text-sm font-medium text-gray-700">Full Name</label>
            <input v-model="profile.name" type="text" class="mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md p-2 border">
          </div>

          <div class="sm:col-span-3">
            <label class="block text-sm font-medium text-gray-700">Job Title / Headline</label>
            <input v-model="profile.title" type="text" placeholder="e.g. Senior Software Engineer" class="mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md p-2 border">
          </div>

          <div class="sm:col-span-3">
            <label class="block text-sm font-medium text-gray-700">Email Address</label>
             <input v-model="profile.email" type="email" class="mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md p-2 border">
          </div>

          <div class="sm:col-span-3">
             <label class="block text-sm font-medium text-gray-700">Phone Number</label>
             <input v-model="profile.phone" type="text" class="mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md p-2 border">
          </div>
          
           <div class="sm:col-span-3">
             <label class="block text-sm font-medium text-gray-700">Location</label>
             <input v-model="profile.location" type="text" placeholder="City, Country" class="mt-1 focus:ring-primary focus:border-primary block w-full shadow-sm sm:text-sm border-gray-300 rounded-md p-2 border">
          </div>
        </div>
        
        <h2 class="text-xl font-bold text-gray-800 mb-4 border-b pb-2">Links & Summary</h2>
        <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6 mb-8">
           <div class="sm:col-span-6">
            <label class="block text-sm font-medium text-gray-700">Links (one per line)</label>
            <textarea v-model="profile.linksText" rows="2" placeholder="https://linkedin.com/in/..." class="mt-1 shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border border-gray-300 rounded-md p-2"></textarea>
          </div>
          <div class="sm:col-span-6">
            <label class="block text-sm font-medium text-gray-700">Professional Summary</label>
            <textarea v-model="profile.summary" rows="3" class="mt-1 shadow-sm focus:ring-primary focus:border-primary block w-full sm:text-sm border border-gray-300 rounded-md p-2"></textarea>
          </div>
        </div>

        <!-- Experience Section (Timeline) -->
        <h2 class="text-xl font-bold text-gray-800 mb-6 border-b pb-2 flex justify-between items-center">
            Professional Experience
            <button @click="addExperience" class="text-sm bg-indigo-50 text-indigo-700 px-3 py-1 rounded hover:bg-indigo-100 transition-colors">+ Add</button>
        </h2>
        
        <div class="relative pl-8 mb-10 space-y-6 before:content-[''] before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-gray-200">
             <div v-for="(exp, index) in profile.experience" :key="index" class="relative bg-white p-6 rounded-xl border border-gray-100 shadow-sm transition-shadow hover:shadow-md">
                <!-- Timeline Dot -->
                <div class="absolute -left-[30px] top-6 h-4 w-4 rounded-full bg-primary border-4 border-white shadow-sm ring-1 ring-gray-100"></div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="md:col-span-2 flex justify-between">
                         <h3 class="font-semibold text-lg text-gray-800">
                            <input v-model="exp.role" placeholder="Role / Title" class="bg-transparent focus:bg-gray-50 w-full border-none focus:ring-0 p-0 font-bold placeholder-gray-400">
                         </h3>
                         <button @click="removeExperience(index)" class="text-gray-400 hover:text-red-500 transition-colors">
                             <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                         </button>
                    </div>
                    
                    <div>
                        <label class="text-xs text-gray-500 uppercase font-semibold">Company</label>
                        <input v-model="exp.company" placeholder="Company Name" class="mt-1 block w-full border-gray-200 bg-gray-50 rounded-md text-sm p-2 focus:ring-primary focus:border-primary">
                    </div>
                    
                    <div>
                        <label class="text-xs text-gray-500 uppercase font-semibold">Duration</label>
                         <input v-model="exp.duration" placeholder="e.g. 2020 - Present" class="mt-1 block w-full border-gray-200 bg-gray-50 rounded-md text-sm p-2 focus:ring-primary focus:border-primary">
                    </div>
                </div>
             </div>
             
             <div v-if="profile.experience.length === 0" class="text-gray-400 italic text-sm pl-2">
                 No experience detailed yet.
             </div>
        </div>

        <!-- Education Section (Timeline) -->
        <h2 class="text-xl font-bold text-gray-800 mb-6 border-b pb-2 flex justify-between items-center">
            Education
             <button @click="addEducation" class="text-sm bg-indigo-50 text-indigo-700 px-3 py-1 rounded hover:bg-indigo-100 transition-colors">+ Add</button>
        </h2>
        <div class="relative pl-8 mb-10 space-y-6 before:content-[''] before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-gray-200">
             <div v-for="(edu, index) in profile.education" :key="index" class="relative bg-white p-6 rounded-xl border border-gray-100 shadow-sm transition-shadow hover:shadow-md">
                 <!-- Timeline Dot -->
                <div class="absolute -left-[30px] top-6 h-4 w-4 rounded-full bg-indigo-400 border-4 border-white shadow-sm ring-1 ring-gray-100"></div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                     <div class="md:col-span-2 flex justify-between">
                         <h3 class="font-semibold text-lg text-gray-800 w-full">
                            <input v-model="edu.school" placeholder="School / University" class="bg-transparent focus:bg-gray-50 w-full border-none focus:ring-0 p-0 font-bold placeholder-gray-400">
                         </h3>
                         <button @click="removeEducation(index)" class="text-gray-400 hover:text-red-500 transition-colors">
                             <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                         </button>
                    </div>
                    
                     <div>
                        <label class="text-xs text-gray-500 uppercase font-semibold">Degree</label>
                        <input v-model="edu.degree" placeholder="Degree / Major" class="mt-1 block w-full border-gray-200 bg-gray-50 rounded-md text-sm p-2 focus:ring-primary focus:border-primary">
                    </div>
                    
                    <div>
                        <label class="text-xs text-gray-500 uppercase font-semibold">Year</label>
                        <input v-model="edu.year" placeholder="Year (e.g. 2018)" class="mt-1 block w-full border-gray-200 bg-gray-50 rounded-md text-sm p-2 focus:ring-primary focus:border-primary">
                    </div>
                </div>
             </div>
               <div v-if="profile.education.length === 0" class="text-gray-400 italic text-sm pl-2">
                 No education detailed yet.
             </div>
        </div>

        <!-- Skills -->
        <h2 class="text-xl font-bold text-gray-800 mb-4 border-b pb-2">Skills</h2>
          <div class="sm:col-span-6 mb-8">
            <div class="mt-1 flex flex-wrap gap-2 mb-2">
                <span v-for="(skill, index) in profile.skills" :key="index" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
                    {{ skill }}
                    <button @click="removeSkill(index)" class="ml-2 text-indigo-600 hover:text-indigo-900">×</button>
                </span>
            </div>
            <div class="flex gap-2">
                <input v-model="newSkill" @keyup.enter="addSkill" type="text" placeholder="Add a skill..." class="focus:ring-primary focus:border-primary block w-full pl-3 sm:text-sm border-gray-300 rounded-md p-3 border">
                <button @click="addSkill" class="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200">Add</button>
            </div>
          </div>

        <div class="mt-8 pt-5 border-t border-gray-200 flex justify-end items-center gap-4">
             <span v-if="saveMessage" :class="saveMessage.includes('Error') ? 'text-red-600' : 'text-green-600'">{{ saveMessage }}</span>
             <button @click="saveProfile" :disabled="saving" class="bg-primary text-white px-6 py-3 rounded-xl shadow-md hover:bg-primary-dark transition-colors font-medium">
                 <span v-if="saving">Saving...</span>
                 <span v-else>Save Profile</span>
             </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchWithAuth } from '../utils/api'

const API_URL = 'http://localhost:5000/api'
const profile = ref({
  name: '',
  title: '',
  email: '',
  phone: '',
  location: '',
  linksText: '',
  summary: '',
  skills: [],
  experience: [],
  education: []
})

const newSkill = ref('')
const uploading = ref(false)
const uploadError = ref(null)
const parsedSuccess = ref(false)
const saving = ref(false)
const saveMessage = ref(null)

onMounted(async () => {
    await loadProfile()
})

const loadProfile = async () => {
    try {
        // GET requests don't need CSRF token, but fetchWithAuth handles credentials nicely
        const response = await fetchWithAuth(`${API_URL}/user/profile`)
        if (response.ok) {
            const data = await response.json()
            // Map backend fields to frontend
            profile.value.name = data.name || ''
            profile.value.email = data.email || ''
            profile.value.phone = data.phone || ''
            profile.value.summary = data.summary || ''
            profile.value.skills = data.skills || []
            profile.value.experience = data.experience || []
            profile.value.education = data.education || []
            
            // Sync localStorage
            const user = JSON.parse(localStorage.getItem('user')) || {}
            localStorage.setItem('user', JSON.stringify({ ...user, ...data }))
        }
    } catch (e) {
        console.error("Failed to load profile", e)
    }
}

const saveProfile = async () => {
    saving.value = true
    saveMessage.value = null
    try {
        const response = await fetchWithAuth(`${API_URL}/user/profile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile.value)
        })
        if (response.ok) {
            saveMessage.value = "Profile saved successfully!"
            // Update localStorage so other components reflect changes immediately
            const user = JSON.parse(localStorage.getItem('user')) || {}
            const updatedUser = { ...user, ...profile.value }
            localStorage.setItem('user', JSON.stringify(updatedUser))
            
            setTimeout(() => saveMessage.value = null, 3000)
        } else {
            throw new Error("Failed to save")
        }
    } catch (e) {
        saveMessage.value = "Error saving profile."
    } finally {
        saving.value = false
    }
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploading.value = true
  uploadError.value = null
  parsedSuccess.value = false

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await fetchWithAuth(`${API_URL}/parse-cv`, {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) throw new Error('Failed to parse CV')
    
    const data = await response.json()
    
    // Autofill form
    if (data.name) profile.value.name = data.name
    if (data.email) profile.value.email = data.email
    if (data.phone) profile.value.phone = data.phone
    if (data.summary) profile.value.summary = data.summary
    if (data.links && data.links.length) profile.value.linksText = data.links.join('\n')
    
    // Education & Experience
    if (data.education) profile.value.education = data.education
    if (data.experience) profile.value.experience = data.experience

    if (data.skills && data.skills.length > 0) {
        const existing = new Set(profile.value.skills.map(s => s.toLowerCase()))
        data.skills.forEach(s => {
            if (!existing.has(s.toLowerCase())) {
                profile.value.skills.push(s)
            }
        })
    }
    parsedSuccess.value = true

  } catch (e) {
    uploadError.value = e.message
  } finally {
    uploading.value = false
  }
}

const addSkill = () => {
  if (newSkill.value.trim()) {
      profile.value.skills.push(newSkill.value.trim())
      newSkill.value = ''
  }
}

const removeSkill = (index) => {
    profile.value.skills.splice(index, 1)
}

const addExperience = () => {
    profile.value.experience.push({ role: '', company: '', duration: '' })
}
const removeExperience = (index) => {
    profile.value.experience.splice(index, 1)
}

const addEducation = () => {
    profile.value.education.push({ school: '', degree: '', year: '' })
}
const removeEducation = (index) => {
    profile.value.education.splice(index, 1)
}
</script>
