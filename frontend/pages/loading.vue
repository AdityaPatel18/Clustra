<template>
  <div class="loading-screen">
    <p>Processing images, please wait...</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useFileStore } from "@/stores/fileStore";


const router = useRouter();
const fileStore = useFileStore();

onMounted(async () => {
  console.log("Stored files:", fileStore.files);
  const files = fileStore.files;
  const formData = new FormData();

  files.forEach((fileObj) => {
    formData.append("files", fileObj.file);
  });

  // Then send it
  const response = await fetch("http://localhost:3001/extract", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  console.log("Received:", data);

  router.push("/identificationScreen");
});


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
