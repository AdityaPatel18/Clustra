<template>
  <div class="page-wrapper">
    <div class="homepage">
      <div class="title">Clustra</div>

      <div class="center-box">
        <div class="drop-area">
          <div
            class="inner-drop-box"
            @drop="handleDrop"
            @dragover="handleDragOver"
          >
            <div v-if="selectedFiles.length" class="preview-box">
              <div
                v-for="(file, index) in selectedFiles"
                :key="index"
                class="thumb"
              >
                <img :src="file.url" :alt="file.name" class="thumb-img" />
              </div>
            </div>
            <div v-else class="placeholder-text">Drag & Drop Files Here</div>
          </div>

          <!-- Hidden file input -->
          <input
            type="file"
            ref="fileInputRef"
            @change="handleFileInput"
            style="display: none"
            multiple
            accept="image/png, image/jpeg, image/jpg, image/heic"
          />

          <div class="button-row">
            <button class="btn" @click="triggerFileInput">From Computer</button>
            <button class="btn upload" @click="classifyPage">Upload</button>
          </div>
        </div>
      </div>
    </div>
    <!-- About Section -->
    <div class="about-section">
      <p>
        Clustra is an intelligent photo grouping tool that helps you quickly
        identify and organize faces across multiple images. Drag, drop, and let
        Clustra do the work. No signup or download needed!
      </p>
    </div>

    <!-- Steps Section -->
    <div class="steps-section">
      <div
        class="step"
        v-for="(step, index) in steps"
        :key="index"
        :class="{ reverse: index % 2 === 1 }"
      >
        <img class="step-image" :src="step.image" :alt="step.title" />
        <div class="step-text">
          <h3>{{ step.title }}</h3>
          <p>{{ step.description }}</p>
        </div>
      </div>
    </div>

    <div class="perfect-for">
      Whether you’re a photographer organizing thousands of event shots, a
      family sorting through memories, or friends fresh off a trip, Clustra
      helps you bring it all together — effortlessly.
    </div>

    <theFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue"; // Add `ref`
import { useFileStore } from "@/stores/fileStore";
import { useRouter } from "vue-router";

const fileStore = useFileStore();
const router = useRouter();
const fileInputRef = ref<HTMLInputElement | null>(null); // 👈 new

const steps = [
  {
    title: "Step 1: Upload Your Pictures",
    description: "Drag and drop or select the photos you want to organize.",
    image: "/images/pic01.jpg",
  },
  {
    title: "Step 2: Identify the Faces",
    description:
      "Tag or name the people in each group to keep things organized.",
    image: "/images/pic01.jpg",
  },
  {
    title: "Step 3: Filter and Download",
    description:
      "Clustra helps you sort the images you need — then download everything in one click.",
    image: "/images/pic01.jpg",
  },
];

const validImageTypes = ["image/png", "image/jpeg", "image/jpg", "image/heic"];
const selectedFiles = computed(() => fileStore.files);

// 👇 new method to trigger the hidden input
function triggerFileInput() {
  fileInputRef.value?.click();
}

// 👇 updated to work with the input
function handleFileInput(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    const files = Array.from(input.files).filter((file) =>
      validImageTypes.includes(file.type)
    );
    fileStore.addFiles(files);
    input.value = ""; // Clear file input so same file can be selected again
  }
}

function handleDrop(event: DragEvent) {
  event.preventDefault();
  if (event.dataTransfer?.files) {
    const files = Array.from(event.dataTransfer.files).filter((file) =>
      validImageTypes.includes(file.type)
    );
    fileStore.addFiles(files);
  }
}

function handleDragOver(event: DragEvent) {
  event.preventDefault();
}

function classifyPage() {
  if (fileStore.files.length === 0) {
    alert("Please upload images first.");
    return;
  }
  router.push("/loading");
}
</script>

<style scoped>
.body,
html {
  margin: 0;
  padding: 0;
  border: 0;
}
.page-wrapper {
  display: flex;
  flex-direction: column;
}

.homepage {
  width: 100%;
  background-color: #f5f5f5;
}

.title {
  display: flex;
  align-self: start;
  padding-left: 2rem;
  padding-top: 2rem;
  font-size: 3rem;
  font-weight: bold;
  color: #333;
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

.inner-drop-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  padding: 1rem;
  min-height: 150px;
  border: 2px dashed #ccc;
  border-radius: 1rem;
  background-color: #f9f9f9;
  position: relative;
  text-align: center;
  height: 90%;
  width: 90%;
}

.preview-box {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  width: 100%;
}

.placeholder-text {
  width: 100%;
  text-align: center;
  color: #777;
  font-size: 1.1rem;
}
.center-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 67vh;
}

.drop-area {
  width: 35rem;
  height: 25rem;
  border: 2px solid #aaa;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  background-color: white;
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.button-row {
  display: flex;
  gap: 10px;
  justify-content: center;
  width: 100%;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background-color: #e0e0e0;
  color: #333;
  font-size: 0.95rem;
  transition: background-color 0.2s ease;
}

.btn:hover {
  background-color: #d0d0d0;
}

.btn.upload {
  background-color: #4caf50;
  color: white;
}

.btn.upload:hover {
  background-color: #45a049;
}

.about-section {
  padding: 1rem 2rem;
  text-align: center;
  max-width: 70vw;
  margin: 0 auto;
}

.about-section p {
  font-size: 2rem;
  color: #555;
  line-height: 1.5;
}

.steps-section {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  padding: 3rem 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.step {
  display: flex;
  align-items: self-start;
  gap: 2rem;
  flex-wrap: wrap;
  padding-top: 10vh;
  height: 25rem;
}

.step.reverse {
  flex-direction: row-reverse;
}

.step-image {
  flex: 1 1 300px;
  height: 25rem;
  width: 25rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.step-text {
  flex: 1 1 300px;
}

.step-text h3 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  color: #222;
}

.step-text p {
  font-size: 2rem;
  color: #444;
}

.perfect-for {
  padding: 6rem 2rem;
  text-align: center;
  max-width: 70vw;
  margin: 0 auto;
  font-size: 2rem;
  color: #555;
  line-height: 1.5;
}
</style>
