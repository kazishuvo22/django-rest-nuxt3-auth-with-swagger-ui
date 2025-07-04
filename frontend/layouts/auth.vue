<template>
  <div class="auth-layout">
    <main>
      <slot/> <!-- Page content goes here -->
    </main>
  </div>
</template>



<style scoped>
.auth-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

main {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
