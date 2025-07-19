<template>
  <div class="upload-page">
    <div
      class="upload-box"
      @drop="handleDrop"
      @dragover="handleDragOver"
    >
      <input
        type="file"
        multiple
        accept=".png, .jpg, .jpeg, .heic"
        @change="handleFileInput"
        class="hidden-input"
        id="fileInput"
      />
      <label for="fileInput" class="upload-label">
        Upload Images (PNG, JPG, JPEG, HEIC)
      </label>

      <!-- Preview Thumbnails -->
      <div v-if="selectedFiles.length" class="preview-box">
        <div
          v-for="(file, index) in selectedFiles"
          :key="index"
          class="thumb"
        >
          <img
            :src="file.preview"
            :alt="file.name"
            class="thumb-img"
          />
        </div>
      </div>

      <!-- Upload Controls -->
      <div class="upload-controls">
        <label class="upload-input">
          <input
            type="file"
            webkitdirectory
            directory
            multiple
            hidden
            @change="handleFileInput"
          />
          <button class="btn">From Computer</button>
        </label>
        <router-link to="/identificationScreen">
  <button class="btn upload-btn">Upload</button>
</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedFiles = ref([])

const validImageTypes = [
  'image/png',
  'image/jpeg',
  'image/jpg',
  'image/heic',
]

function handleFileInput(event) {
  const files = Array.from(event.target.files)
  selectedFiles.value = files
    .filter(file => validImageTypes.includes(file.type))
    .map(file => ({
      ...file,
      preview: URL.createObjectURL(file)
    }))
}

function handleDrop(event) {
  event.preventDefault()
  const files = Array.from(event.dataTransfer.files)
  selectedFiles.value = files
    .filter(file => validImageTypes.includes(file.type))
    .map(file => ({
      ...file,
      preview: URL.createObjectURL(file)
    }))
}

function handleDragOver(event) {
  event.preventDefault()
}
</script>

<style scoped>
.upload-page {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f9fafb;
  margin: 0;
  padding: 0;
}

.upload-box {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 420px;
  max-width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-label {
  display: block;
  margin-bottom: 1rem;
  cursor: pointer;
  color: #4f46e5;
  font-weight: 600;
}

.preview-box {
  width: 100%;
  min-height: 150px;
  background-color: #f3f4f6;
  border: 2px dashed #d1d5db;
  border-radius: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem;
  gap: 0.5rem;
}

.thumb {
  width: 60px;
  height: 60px;
  overflow: hidden;
  border-radius: 0.5rem;
  border: 1px solid #ddd;
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-controls {
  display: flex;
  gap: 1rem;
}

.upload-input {
  display: inline-block;
}

.btn {
  padding: 0.6rem 1.1rem;
  border: none;
  border-radius: 0.5rem;
  background-color: #4f46e5;
  color: white;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.btn:hover {
  background-color: #3730a3;
}

.upload-btn {
  background-color: #10b981;
}

.upload-btn:hover {
  background-color: #059669;
}
</style>