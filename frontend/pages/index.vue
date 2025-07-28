<template>
  <div class="page-wrapper">
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-box">
        <h2>🔧 Localhost Backend Required</h2>
        <p>
          This app performs heavy image processing and requires a backend to be hosted locally.
          <br />
          Please clone and run the backend using the link below:
        </p>
        <a
          href="https://github.com/AdityaPatel18/Clustra"
          target="_blank"
          class="link"
        >
          → Open GitHub Repo
        </a>
        <div class="modal-actions">
          <button @click="closeModal">Got it</button>
        </div>
      </div>
    </div>

    <!-- Warning Banner -->
    <div v-if="!backendAvailable" class="warning-banner">
      ⚠️ Backend not detected. Please run it locally at
      <code>http://localhost:3001</code> before uploading files.
    </div>

    <div class="homepage">
      <div class="title">Clustra</div>

      <div class="center-box">
        <div class="center-box-header">Sort Photos by People</div>

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

                <button class="remove-btn" @click="removeFile(index)"></button>
              </div>
            </div>
            <div v-else class="placeholder-text">Drag & Drop Files Here</div>
          </div>

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
            <button
              class="btn upload"
              @click="classifyPage"
              :disabled="!backendAvailable"
            >
              Upload
            </button>
          </div>
        </div>
        <div class="numberSelected">{{ uploadedCountText }}</div>
      </div>
    </div>
    <div class="info">
      <!-- About Section -->
      <div class="about-section">
        <p>
          <span class="special-word">Clustra</span> is an intelligent photo
          grouping tool that helps you quickly identify and organize faces
          across multiple images. Drag, drop, and let
          <span class="special-word">Clustra</span> do the work. No signup or
          download needed!
        </p>
      </div>

      <!-- Steps Section -->
      <div class="steps-section">
        <div class="step">
          <video class="step-image" autoplay muted playsinline>
            <source src="/assets/videos/landing.mp4" type="video/mp4" />
          </video>

          <div class="step-text">
            <h3>Upload Your Pictures</h3>
            <p>Drag and drop or select the photos you want to organize.</p>
          </div>
        </div>

        <div class="step reverse">
          <video class="step-image" autoplay muted playsinline>
            <source src="/assets/videos/identification.mp4" type="video/mp4" />
          </video>

          <div class="step-text">
            <h3>Identify the Faces</h3>
            <p>
              Tag or name the people in each group to keep things organized.
            </p>
          </div>
        </div>

        <div class="step">
          <video class="step-image" autoplay muted playsinline>
            <source src="/assets/videos/Clustering.mp4" type="video/mp4" />
          </video>

          <div class="step-text">
            <h3>Filter and Download</h3>
            <p>
              <span class="special-word">Clustra</span> helps you sort the
              images you need — then download everything in one click.
            </p>
          </div>
        </div>
      </div>

      <div class="perfect-for">
        Whether you’re a photographer organizing thousands of event shots, a
        family sorting through memories, or friends fresh off a trip,
        <span class="special-word">Clustra</span>
        helps you bring it all together — effortlessly.
      </div>
    </div>
    <theFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useFileStore } from "@/stores/fileStore";
import { useRouter } from "vue-router";

const fileStore = useFileStore();
const router = useRouter();
const fileInputRef = ref<HTMLInputElement | null>(null);

const validImageTypes = ["image/png", "image/jpeg", "image/jpg", "image/heic"];
const selectedFiles = computed(() => fileStore.files);

function triggerFileInput() {
  fileInputRef.value?.click();
}

function removeFile(index: number) {
  fileStore.files.splice(index, 1);
}

function handleFileInput(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    const files = Array.from(input.files).filter((file) =>
      validImageTypes.includes(file.type)
    );
    fileStore.addFiles(files);

    input.value = "";
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
  router.replace("/loading");
}

const showModal = ref(true);
const backendAvailable = ref(false);

function closeModal() {
  showModal.value = false;
}

// Ping backend on mount
onMounted(async () => {
  try {
    const res = await fetch("http://localhost:3001/ping");
    if (res.ok) {
      backendAvailable.value = true;
    }
  } catch (err) {
    backendAvailable.value = false;
  }
});

onMounted(() => {
  const videos = document.querySelectorAll<HTMLVideoElement>(".step-image");

  if (!videos || videos.length === 0) {
    console.warn("No videos found with .step-image");
    return;
  }

  const delaySeconds = 2;

  videos.forEach((video) => {
    video.addEventListener("ended", () => {
      setTimeout(() => {
        video.currentTime = 0;
        video.play();
      }, delaySeconds * 1000);
    });
  });
});
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
}

.page-wrapper {
  display: flex;
  flex-direction: column;
  background-color: #2e1503;
}

.homepage {
  width: 100%;
}

.title {
  display: flex;
  align-self: start;
  padding-left: 2rem;
  padding-top: 2rem;
  font-size: 3rem;
  font-weight: bold;
  color: #f5f5dc;
}

.thumb {
  width: 60px;
  height: 60px;
  overflow: hidden;
  border-radius: 0.5rem;
  position: relative;
}
.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: -8px;
  right: -6px;
  background-color: red;
  color: white;
  border: none;
  border-radius: 50%;
  font-weight: bold;
  cursor: pointer;
  width: 20px;
  height: 20px;
  line-height: 16px;
  text-align: center;
  font-size: 14px;
}

.numberSelected {
  color: beige;
  padding-top: 1rem;
}

.inner-drop-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  padding: 1rem;
  min-height: 150px;
  border-radius: 1rem;
  background-color: beige;
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
  overflow-y: auto;
  max-height: 300px;
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
}

.center-box-header {
  align-items: start;
  color: beige;
  font-size: clamp(1.5rem, 10vh, 6rem);
  margin-bottom: 2rem;
  font-style: italic;
}

.drop-area {
  width: clamp(20rem, 40vw, 35rem);
  height: clamp(15rem, 30vw, 25rem);
  border: 2px solid tan;
  border-radius: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  background-color: 2e1503;
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
  border: 2px solid beige;
  border-radius: 16px;
  cursor: pointer;
  background-color: transparent;
  color: beige;
  font-size: 0.95rem;
  transition: background-color 0.2s ease;
}

.btn:hover {
  background-color: #d2691e;
}

.btn.upload {
  background-color: transparent;
  color: beige;
}

.btn.upload:hover {
  background-color: #45a049;
}
.info {
  width: 100%;
  border-radius: 2rem;
  background-color: beige;
}

.about-section {
  padding: 1rem 2rem;
  text-align: center;
  max-width: 70vw;
  margin: 0 auto;
}

.about-section p {
  font-size: 2rem;
  color: #2e1503;
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
  color: #2e2e2e;
}

.step-text p {
  font-size: 2rem;
  color: #2e1503;
}

/* Only force wrap on small screens */
@media (max-width: 768px) {
  .step {
    height: auto;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .step.reverse {
    flex-direction: column;
  }

  .step-text {
    width: 100%;
    margin-top: 1rem;
  }
}
.perfect-for {
  padding: 6rem 2rem;
  text-align: center;
  max-width: 70vw;
  margin: 0 auto;
  font-size: 2rem;
  color: #2e1503;
  line-height: 1.5;
}

.special-word {
  color: #d2691e;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal-box {
  background-color: #f7e8d0;
  border: 2px solid #4b2e2e;
  border-radius: 1rem;
  padding: 1.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
}

.modal-box h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.modal-box p {
  margin-bottom: 1rem;
  line-height: 1.5;
}

.link {
  color: #4b2e2e;
  text-decoration: underline;
  font-weight: 600;
}

.link:hover {
  color: #2f1c1c;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.modal-actions button {
  background-color: #4b2e2e;
  color: white;
  padding: 0.5rem 1.25rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.modal-actions button:hover {
  background-color: #3c1f1f;
}

/* Warning Banner */
.warning-banner {
  background-color: #f4d9b6;
  border-bottom: 2px solid #4b2e2e;
  padding: 0.75rem 1rem;
  text-align: center;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

</style>
