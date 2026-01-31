<template>
  <div class="group bg-white rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border border-gray-100 hover:border-violet-100 flex flex-col h-full relative overflow-hidden">
    <!-- Gradient Overlay on Hover -->
    <div class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-violet-500 to-fuchsia-500 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>

    <div class="p-6 flex-grow flex flex-col relative z-10">
      <div class="flex justify-between items-start mb-4">
        <div class="flex items-center space-x-4 flex-grow min-w-0 mr-2">
            <!-- Company Logo -->
            <div 
                class="flex-shrink-0 h-14 w-14 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-sm ring-1 ring-gray-100 group-hover:ring-violet-100 transition-all duration-300"
                :style="{ backgroundColor: getCompanyColor(job.company) }"
            >
                {{ getCompanyInitials(job.company) }}
            </div>

            <!-- Content: Title & Company -->
            <div class="min-w-0">
                <h3 class="text-lg sm:text-xl font-bold text-gray-900 leading-snug group-hover:text-violet-600 transition-colors tracking-tight line-clamp-2">
                    <router-link :to="'/job/' + job.id" class="focus:outline-none">
                        <span class="absolute inset-0" aria-hidden="true"></span>
                        {{ job.title }}
                    </router-link>
                </h3>
                <p class="text-sm text-gray-500 font-medium mt-1 truncate">{{ job.company }}</p>
            </div>
        </div>
        
        <!-- Right Side: Actions -->
        <div class="flex space-x-1 relative z-20 flex-shrink-0">
            <!-- Cover Letter Button Removed -->
            <button @click.prevent="$emit('toggle-saved', job.id)" class="p-2 rounded-full text-gray-400 hover:bg-red-50 hover:text-red-500 transition-all duration-200 focus:outline-none transform active:scale-75" title="Save Job">
                 <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transition-all duration-300 ease-spring" :class="saved ? 'text-red-500 fill-current transform scale-125' : 'group-hover:scale-110'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
            </button>
        </div>
      </div>

      <!-- Cover Letter Modal Removed -->
       
      <!-- Tags Row -->
      <div class="flex flex-wrap gap-2 mb-4">
        <span v-if="matchScore > 0" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-emerald-50 to-teal-50 text-emerald-700 border border-emerald-100/50 shadow-sm">
             <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
             {{ matchScore }}% Match
        </span>
        <span 
            :class="{
                'bg-blue-50 text-blue-700 border-blue-100': job.source === 'LinkedIn',
                'bg-purple-50 text-purple-700 border-purple-100': job.source === 'Foundit',
                'bg-orange-50 text-orange-700 border-orange-100': job.source === 'Naukri'
            }"
            class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border"
        >
            {{ job.source }}
        </span>
      </div>

      <div class="mt-auto pt-4 border-t border-gray-50 flex items-center justify-between text-xs text-gray-500 font-medium">
         <div class="flex items-center gap-4">
             <span class="flex items-center transition-colors group-hover:text-gray-700">
                <svg class="h-4 w-4 mr-1.5 text-gray-400 group-hover:text-violet-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                {{ job.location }}
             </span>
             <span class="flex items-center transition-colors group-hover:text-gray-700">
                  <svg class="h-4 w-4 mr-1.5 text-gray-400 group-hover:text-violet-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  {{ formatDate(job.date_posted) }}
             </span>
         </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { calculateMatchScore } from '../utils/matching'

const props = defineProps({
  job: Object,
  saved: Boolean
})

defineEmits(['toggle-saved'])

// We need to parse user from localStorage and keep it reactive or re-read it.
// Since we don't have a global store properly set up with reactivity for basic localStorage,
// we can just re-read it or use a simple composable if available. 
// For now, let's just read it carefully and maybe use a window event listener for storage updates if needed,
// but simpler: `user` should be a ref that we fill.
import { ref, onMounted } from 'vue'

const user = ref(null)

onMounted(() => {
    updateUser()
    window.addEventListener('storage', updateUser)
})

const updateUser = () => {
    try {
        user.value = JSON.parse(localStorage.getItem('user'))
    } catch (e) {
        user.value = null
    }
}

const matchScore = computed(() => {
    if (!user.value || !user.value.skills) return 0
    // Try to handle both array of strings and potential string format from backend
    let skills = user.value.skills
    if (typeof skills === 'string') {
        try { skills = JSON.parse(skills) } catch (e) { skills = [] }
    }
    return calculateMatchScore(props.job, skills)
})

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  if (dateString.match(/ago|today/i)) return dateString;

  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
  
  if (diffDays <= 1) return 'Today';
  if (diffDays <= 7) return `${diffDays} days ago`;
  
  return date.toLocaleDateString()
}

const getCompanyColor = (companyName) => {
    if (!companyName) return '#6b7280';
    const colors = ['#ef4444', '#f97316', '#f59e0b', '#84cc16', '#10b981', '#06b6d4', '#3b82f6', '#6366f1', '#8b5cf6', '#d946ef', '#ec4899'];
    let hash = 0;
    for (let i = 0; i < companyName.length; i++) hash = companyName.charCodeAt(i) + ((hash << 5) - hash);
    return colors[Math.abs(hash) % colors.length];
}

const getCompanyInitials = (companyName) => {
    if (!companyName) return '?';
    return companyName.charAt(0).toUpperCase();
}

// Cover Letter Logic Removed
</script>
