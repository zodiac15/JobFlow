<template>
  <span class="typewriter inline-block">
    <span class="text-transparent bg-clip-text bg-gradient-to-r from-yellow-200 to-pink-200">
        {{ currentText }}
    </span>
    <span class="cursor animate-pulse text-pink-200">|</span>
  </span>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  words: {
    type: Array,
    required: true
  },
  typeSpeed: {
    type: Number,
    default: 100
  },
  deleteSpeed: {
    type: Number,
    default: 50
  },
  pauseTime: {
    type: Number,
    default: 1500
  }
})

const currentText = ref('')
const currentWordIndex = ref(0)
const isDeleting = ref(false)
let timer = null

const type = () => {
    const currentWord = props.words[currentWordIndex.value]
    
    if (isDeleting.value) {
        currentText.value = currentWord.substring(0, currentText.value.length - 1)
    } else {
        currentText.value = currentWord.substring(0, currentText.value.length + 1)
    }

    let speed = props.typeSpeed

    if (!isDeleting.value && currentText.value === currentWord) {
        speed = props.pauseTime
        isDeleting.value = true
    } else if (isDeleting.value && currentText.value === '') {
        isDeleting.value = false
        currentWordIndex.value = (currentWordIndex.value + 1) % props.words.length
        speed = 500
    } else if (isDeleting.value) {
        speed = props.deleteSpeed
    }

    timer = setTimeout(type, speed)
}

onMounted(() => {
    if (props.words.length) {
        type()
    }
})

onUnmounted(() => {
    clearTimeout(timer)
})
</script>

<style scoped>
/* Optional custom cursor styling if Tailwind animate-pulse isn't enough */
</style>
