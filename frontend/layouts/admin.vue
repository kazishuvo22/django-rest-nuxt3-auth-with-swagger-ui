<template>
  <div class="default-layout">
    <header>
      <nav>
        <NuxtLink to="/">Home</NuxtLink>
        <NuxtLink to="/login">Login</NuxtLink>
        <NuxtLink to="/dashboard/admin">Dashboard</NuxtLink>
        <button v-if="authStore.isAuthenticated" @click="logout">Logout</button>
      </nav>
    </header>
    <main>
      <slot /> <!-- Page content goes here -->
    </main>
    <footer>
      <p>&copy; 2025 My App</p>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '@auth/stores/auth';

const authStore = useAuthStore();

const logout = () => {
  authStore.logout();
};
</script>
