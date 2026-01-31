<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-900">
    <Navbar />
    <main class="max-w-5xl mx-auto py-10 px-4 sm:px-6 lg:px-8 flex-grow">
       <!-- Router view handles switching between Home and Job Details -->
       <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
       </router-view>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
// Layout logic only. Content is handled by views.
</script>

<style>
/* Page Transition Styles */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s ease-in-out;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
