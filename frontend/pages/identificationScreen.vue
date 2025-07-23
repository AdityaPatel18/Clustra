<template>
  <div class="container">
    <h2 class="title">Label Faces</h2>

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
  router.push("/clusteringScreen");
}

onMounted(() => {
  if (fileStore.files.length === 0) {
    router.push('/')
  }
})
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: #fdf6ec;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
  color: #3a2e2e;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 20px;
  margin-bottom: 2rem;
}

.face-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.face-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border: 2px solid #ccc;
  margin-bottom: 0.5rem;
}

.input {
  width: 100%;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  border: 1px solid #bbb;
  font-size: 0.9rem;
}

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
}

.submit-btn:hover {
  background-color: #a46c47;
}
</style>