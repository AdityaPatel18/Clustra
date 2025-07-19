<template>
  <div class="loading-screen">
    <p>Processing images, please wait...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(async () => {
  // Simulate classification delay
  await fakeClassification()

  // After processing, go to results
  router.push('/identificationScreen')
})

async function fakeClassification() {
  return new Promise(resolve => setTimeout(resolve, 3000)) // Replace with real logic
}
</script>

<style scoped>
.loading-screen {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.4rem;
}
</style>