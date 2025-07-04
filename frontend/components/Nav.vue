<template>
  <nav class="bg-gray-100 border-b p-4">
    <ul class="flex space-x-4">
      <nav>
        <NuxtLink to="/">Home</NuxtLink>
        <NuxtLink v-if="!isAuthenticated" to="/login">Login</NuxtLink>
        <NuxtLink v-if="!isAuthenticated" to="/register">Register</NuxtLink>
        <NuxtLink v-if="isAuthenticated && isAdmin" to="/dashboard/admin">Admin Dashboard</NuxtLink>
        <NuxtLink v-if="isAuthenticated && isActiveUser" to="/dashboard/user">User Dashboard</NuxtLink>
        <a href="#" role="button" v-if="isAuthenticated" @click="handleLogout">Logout</a>
      </nav>
    </ul>
  </nav>
</template>

<script setup>

import { useAuth } from "@auth/composables/useAuth";

const { isAuthenticated, isAdmin, isActiveUser, logout } = useAuth()

const handleLogout = () => {
  logout();
};

</script>

<style scoped>
</style>
