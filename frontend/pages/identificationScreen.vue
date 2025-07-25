<template>
  
  <div class="container">
          <div class="clustra-title">Clustra</div>

    <h2 class="title">Who’s who? Label them before you go.
</h2>

    <form @submit.prevent="submitLabels">
      <div class="grid">
        <div v-for="(face, index) in faces" :key="face.label" class="face-card">
          <img
            :src="'data:image/jpeg;base64,' + face.face"
            alt="Face"
            class="face-img"
          />
          <input
            v-model="nameInputs[face.label]"
            type="text"
            :placeholder="`Person ${index + 1}`"
            class="input"
          />
        </div>
      </div>

      <button type="submit" class="submit-btn">Submit</button>
    </form>
    </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFileStore } from '@/stores/fileStore'

const router = useRouter()
const fileStore = useFileStore()
const faces = fileStore.people_faces
const nameInputs = reactive<Record<string, string>>({})

faces.forEach((f) => {
  nameInputs[f.label] = ''
})

function submitLabels() {
  fileStore.updateFaceLabels(nameInputs);
  console.log("Updated face labels:", fileStore.people_faces);
  router.replace("/clusteringScreen");
}

onMounted(() => {
  if (fileStore.files.length === 0) {
    router.replace('/')
  }
})
</script>

<style scoped>
html, body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

.container {
  min-height: 100vh;
  min-width: 100vw;
  background-color: beige;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
}

.title {
  font-size: 3rem;
  font-weight: bold;
  text-align: center;
  color: #3a2e2e;
  margin-top: 1rem;
}
.clustra-title {
  align-self: start;
  padding-left: 2rem;
  padding-top: 2rem;
  font-size: 3rem;
  font-weight: bold;
  color: #2e1503;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
  max-width: 80vw;
}

.face-card {
  width: 120px;
}
.face-img {
  width: 120px;
  height: 120px;
  border-radius: 1.5rem;
}

.input {
  width: 84%;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  border: 1px solid #2e1503;
  font-size: 0.9rem;
background-color: beige;}

.submit-btn {
  display: block;
  margin: 0 auto;
  padding: 0.6rem 1.4rem;
  background-color: #8b5e3c;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
  margin-top: 2rem;
}

.submit-btn:hover {
  background-color: #a46c47;
}
</style>