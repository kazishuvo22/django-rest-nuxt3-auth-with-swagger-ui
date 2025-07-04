<template>
  <div>
    <h1>User Dashboard</h1>
    <p v-if="response.username">
      Welcome, {{response.username}}, {{response.email}}
    </p>
    <p v-else>
      User data is not available.
    </p>
  </div>
</template>

<script setup>
import { useAuthStore } from '@auth/stores/auth'
const { $compositeAuthApi } = useNuxtApp()

const authStore = useAuthStore();

const response = await $compositeAuthApi.auth.getProfile()

console.log(response)

// definePageMeta({
//   layout: 'default',
// });


</script>
