<template>
  <div class="p-4 max-w-7xl mx-auto">
    <!-- Top Filter Bar -->
    <div class="flex flex-wrap items-center gap-2 mb-6">
      <div
        v-for="person in allPeople"
        :key="person"
        @click="togglePerson(person)"
        :class="[
          'px-3 py-1 rounded-full cursor-pointer border transition',
          selectedPeople.includes(person)
            ? 'bg-blue-600 text-white border-blue-700'
            : 'bg-white text-gray-800 border-gray-300 hover:bg-blue-100',
        ]"
      >
        {{ person }}
      </div>

      <button
        @click="filterImages"
        class="ml-auto px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Search
      </button>
    </div>

    <!-- Filtered Images Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
      <div
        v-for="file in filteredFiles"
        :key="file.name"
        class="rounded overflow-hidden shadow"
      >
        <img
          :src="file.url"
          :alt="file.name"
          class="w-full h-48 object-cover"
        />
        <div class="p-2 text-sm text-gray-600">
          <strong>People:</strong> {{ file.people.join(", ") || "None" }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useFileStore } from "@/stores/fileStore";
import { useRouter } from "vue-router";

const fileStore = useFileStore();
const router = useRouter();

// All available unique people from all images
const allPeople = computed(() => {
  const names = new Set<string>();
  fileStore.files.forEach((file) => file.people.forEach((p) => names.add(p)));
  return [...names];
});

// Selected filters
const selectedPeople = ref<string[]>([]);

function togglePerson(person: string) {
  const idx = selectedPeople.value.indexOf(person);
  if (idx > -1) selectedPeople.value.splice(idx, 1);
  else selectedPeople.value.push(person);
}

// Filtered images
const filteredFiles = ref(fileStore.files);

function filterImages() {
  if (selectedPeople.value.length === 0) {
    filteredFiles.value = fileStore.files;
    return;
  }

  filteredFiles.value = fileStore.files.filter((file) =>
    selectedPeople.value.every((person) => file.people.includes(person))
  );
}
onMounted(() => {
  if (fileStore.files.length === 0) {
    router.push("/");
  }
});
</script>
