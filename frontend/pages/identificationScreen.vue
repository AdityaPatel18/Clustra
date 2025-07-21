<template>
  <div class="max-w-5xl mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">Label Faces</h2>

    <form @submit.prevent="submitLabels">
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
        <div
          v-for="(face, index) in faces"
          :key="face.label"
          class="flex flex-col items-center space-y-2"
        >
          <img
            :src="'data:image/jpeg;base64,' + face.face"
            alt="Face"
            class="w-24 h-24 object-cover rounded-full shadow"
          />
          <input
            v-model="nameInputs[face.label]"
            type="text"
            :placeholder="`Person ${index + 1}`"
            class="w-full px-2 py-1 border rounded"
          />
        </div>
      </div>

      <button
        type="submit"
        class="mt-8 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      >
        Submit
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useFileStore } from "@/stores/fileStore";
import { useRouter } from "vue-router";

const router = useRouter();
const fileStore = useFileStore();
const faces = fileStore.people_faces;
const nameInputs = reactive<Record<string, string>>({});

// Initialize inputs
faces.forEach((f) => {
  nameInputs[f.label] = "";
});

function submitLabels() {
  console.log("Submitted names:", nameInputs);
  router.push("/clusteringScreen");
}
onMounted(() => {
  if (fileStore.files.length === 0) {
    router.push("/");
  }
});
</script>
