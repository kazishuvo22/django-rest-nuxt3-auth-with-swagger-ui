<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img
          class="mx-auto h-10 w-auto"
          src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=600"
          alt="Your Company"
      />
      <h2 class="mt-10 text-center text-2xl font-bold tracking-tight text-gray-900">Create your account</h2>
    </div>

    <div v-if="successMessage.message" class="mb-4 rounded-md bg-green-50 p-4">
      <div class="flex">
        <div class="ml-3">
          <p class="text-sm font-medium text-green-800">{{ successMessage.message }}</p>
        </div>
      </div>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-md">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Username -->
        <div>
          <label for="username" class="block text-sm font-medium text-gray-900">Username</label>
          <div class="mt-2">
            <input
                v-model="form.username"
                type="text"
                id="username"
                name="username"
                required
                class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm"
            />
          </div>
          <p v-if="errors.username" class="mt-1 text-sm text-red-600">{{ errors.username }}</p>
        </div>

        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-900">Email address</label>
          <div class="mt-2">
            <input
                v-model="form.email"
                type="email"
                id="email"
                name="email"
                autocomplete="email"
                required
                class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm"
            />
          </div>
          <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
        </div>

        <!-- Password -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-900">Password</label>
          <div class="mt-2">
            <input
                v-model="form.password"
                type="password"
                id="password"
                name="password"
                autocomplete="new-password"
                required
                class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm"
            />
          </div>
          <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
        </div>

        <!-- Confirm Password -->
        <div>
          <label for="password_confirm" class="block text-sm font-medium text-gray-900">Confirm Password</label>
          <div class="mt-2">
            <input
                v-model="form.password_confirm"
                type="password"
                id="password_confirm"
                name="password_confirm"
                required
                class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm"
            />
          </div>
          <p v-if="errors.password_confirm" class="mt-1 text-sm text-red-600">{{ errors.password_confirm }}</p>
        </div>

        <!-- First Name -->
        <div>
          <label for="first_name" class="block text-sm font-medium text-gray-900">First Name</label>
          <div class="mt-2">
            <input
                v-model="form.first_name"
                type="text"
                id="first_name"
                name="first_name"
                required
                class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm"
            />
          </div>
          <p v-if="errors.first_name" class="mt-1 text-sm text-red-600">{{ errors.first_name }}</p>
        </div>

        <!-- Last Name -->
        <div>
          <label for="last_name" class="block text-sm font-medium text-gray-900">Last Name</label>
          <div class="mt-2">
            <input
                v-model="form.last_name"
                type="text"
                id="last_name"
                name="last_name"
                required
                class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm"
            />
          </div>
          <p v-if="errors.last_name" class="mt-1 text-sm text-red-600">{{ errors.last_name }}</p>
        </div>

        <!-- Submit Button -->
        <div>
          <button
              type="submit"
              class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Sign up
          </button>
        </div>
      </form>

      <p class="mt-10 text-center text-sm text-gray-500">
        Already have an account?
        <a href="/login" class="font-semibold text-indigo-600 hover:text-indigo-500">Sign in</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useAuthStore } from '@auth/stores/auth';

const authStore = useAuthStore();

const successMessage = reactive({ message: null });


const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  first_name: '',
  last_name: '',
});

// Reactive errors object
const errors = reactive({
  username: null,
  email: null,
  password: null,
  password_confirm: null,
  first_name: null,
  last_name: null,
});

const handleSubmit = async () => {
  try {
    // Clear previous errors
    Object.keys(errors).forEach((key) => (errors[key] = null));
    // Send the form data
    const response = await authStore.register(form);
    // Set success message
    successMessage.message = response?.data?.message || "Account created successfully!";

    console.log(response);

    // navigateTo('/');
  } catch (error) {
    if (error.response && error.response.data) {
      const errorDetails = error.response.data.error || error.response.data;

      if (typeof errorDetails === 'object') {
        // Assign error messages to fields
        Object.entries(errorDetails).forEach(([field, messages]) => {
          // Sometimes the error message may be a string or array
          if (Array.isArray(messages)) {
            errors[field] = messages.join(', ');
          } else {
            errors[field] = messages;
          }
        });
      } else if (typeof errorDetails === 'string') {
        alert(errorDetails);
      } else {
        alert('An unknown error occurred.');
      }
    } else {
      alert('A network error occurred. Please try again.');
    }
  }
};
</script>

