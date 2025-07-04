<template>
  <div>
    <h1>Admin Dashboard</h1>
    <p v-if="authStore?.user?.username">
      Welcome, {{ authStore.user.username }}
    </p>
    <p v-else>
      User data is not available.
    </p>
  </div>
</template>

<script setup>
import { useAuthStore } from '@auth/stores/auth';

const authStore = useAuthStore();

definePageMeta({
  layout: 'admin',
});


</script>
