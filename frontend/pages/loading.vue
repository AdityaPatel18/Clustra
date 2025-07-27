<template>
  <div class="loading-screen">
    <div class="center-content">
      <h1 class="clustra-logo">
        <span
          v-for="(char, i) in 'Clustra'"
          :key="i"
          :style="{ animationDelay: `${i * 0.1}s` }"
          class="wave-letter"
        >
          {{ char }}
        </span>
      </h1>
      <p class="loading-text">Processing images, please wait...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useFileStore } from "@/stores/fileStore";

const router = useRouter();
const fileStore = useFileStore();

let hasRun = false;

onMounted(async () => {
  if (hasRun) return;
  hasRun = true;

  if (fileStore.files.length === 0) {
    router.replace("/");
    return;
  }

  console.log("Stored files:", fileStore.files);

  const formData = new FormData();
  fileStore.files.forEach((fileObj) => {
    formData.append("files", fileObj.file);
  });

  try {
    //const backendURL = import.meta.env.VITE_BACKEND_URL;

    const response = await fetch(`http://localhost:3001/extract`, {
      method: "POST",
      body: formData,
    });

    const raw = await response.json();
    console.log("Received:", raw);

    type ExtractResultItem = {
      filename: string;
      individuals: string[];
    };
    const data = raw as { result: ExtractResultItem[] };

    data.result.forEach(({ filename, individuals }) => {
      const file = fileStore.files.find((f) => f.name === filename);
      if (file) {
        file.people = individuals;
      }
    });

    fileStore.people_faces = raw.people_faces;

    router.replace("/identificationScreen");
  } catch (err) {
    console.error("Failed to fetch:", err);
  }
});
</script>

<style scoped>
@keyframes wave {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.wave-letter {
  display: inline-block;
  animation: wave 1.2s ease-in-out infinite;
}

.loading-screen {
  height: 100vh;
  background-color: beige;
  display: flex;
  justify-content: center;
  align-items: center;
}

.center-content {
  text-align: center;
}

.clustra-logo {
  font-size: 5rem;
  font-weight: 700;
  color: #5a3e2b;
  letter-spacing: 0.5rem;
}

.loading-text {
  font-size: 2rem;
  color: #7d5d45;
}
</style>
