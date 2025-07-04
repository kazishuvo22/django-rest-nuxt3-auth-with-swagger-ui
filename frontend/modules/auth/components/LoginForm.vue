<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl font-bold tracking-tight text-gray-900">Sign in to your account</h2>
    </div>
    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-900">Username/Email address</label>
          <div class="mt-2">
            <input
                v-model="credentials.username_or_email"
                type="text"
                name="email"
                id="email"
                required
                class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-900">Password</label>
          <div class="mt-2">
            <input
                v-model="credentials.password"
                type="password"
                name="password"
                id="password"
                required
                class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        <div>
          <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Sign in
          </button>
        </div>
        <!-- Display error message -->
        <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>

      </form>
    </div>
  </div>
</template>

<script setup>
const { $compositeAuthApi } = useNuxtApp()
import { useAuthStore } from '@auth/stores/auth'
const router = useRouter()
const credentials = ref({
  username_or_email: '',
  password: ''
})
const errorMessage = ref('')

const authStore = useAuthStore()

const handleLogin = async () => {
  try {
    const response = await authStore.login(credentials.value)
    errorMessage.value = '' // Clear error on success
    console.log('Login response:', response)

    if (authStore.isAuthenticated && authStore.isActiveUser && !authStore.isAdmin){
      router.push('/dashboard/user')
    }
    else if (authStore.isAuthenticated && authStore.isAdmin){
      router.push('/dashboard/admin')
    }
    else {
      router.push('/login')
    }
  } catch (error) {
    errorMessage.value = error.data.error
    console.error('Login error:', errorMessage.value)
  }
}
</script>
