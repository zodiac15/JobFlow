<template>
  <div class="mt-8">
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      <p class="mt-2 text-gray-500">Loading jobs...</p>
    </div>
    <div v-else-if="jobs.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">No jobs found. Try searching or fetching new jobs.</p>
    </div>
    <div v-else>
      <JobCard v-for="job in jobs" :key="job.id" :job="job" />
    </div>
  </div>
</template>

<script setup>
import JobCard from './JobCard.vue'

defineProps({
  jobs: Array,
  loading: Boolean
})
</script>
