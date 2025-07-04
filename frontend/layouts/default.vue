<template>
  <div class="flex flex-col min-h-screen">
    <!-- Header -->
    <Header />

    <!-- Navigation -->
    <Nav />

    <!-- Main Content -->
    <main class="flex-grow p-4">
      <slot />
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue';
import Nav from '@/components/Nav.vue';
import Footer from '@/components/Footer.vue';
</script>

<style scoped>
</style>
