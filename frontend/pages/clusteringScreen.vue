<template>
  <div class="container">
    <!-- Sidebar Filters -->
    <aside class="sidebar">
      <h2>Filter by People</h2>
      <div class="chips">
        <button class="reset-filter" @click="resetToggle">Reset All</button>

        <div
          v-for="person in allPeople"
          :key="person"
          :class="['chip', selectedPeople.includes(person) ? 'active' : '']"
          @click="togglePerson(person)"
        >
          {{ person }}
        </div>
      </div>
      <button class="filter-btn" @click="filterImages">Search</button>
      <div class="download-section">
        <button @click="toggleSelectAll">
          {{ allFilteredSelected ? "Deselect All" : "Select All" }}
        </button>
        <button class="download" @click="downloadSelected">Download</button>
      </div>
    </aside>

    <!-- Image Gallery -->
    <main class="gallery">
      <div class="grid">
        <div
          v-for="file in filteredFiles"
          :key="file.name"
          class="card"
          :class="{ selected: selectedFiles.includes(file.name) }"
          @click="toggleSelection(file.name)"
        >
          <img :src="file.url" :alt="file.name" />
          <div v-if="getCleanPeople(file.people)" class="overlay">
            {{ getCleanPeople(file.people) }}
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useFileStore } from "@/stores/fileStore";
import { useRouter } from "vue-router";
import JSZip from "jszip";
import { saveAs } from "file-saver";

const fileStore = useFileStore();
const router = useRouter();

const selectedPeople = ref<string[]>([]);

const allPeople = computed(() => {
  const names = new Set<string>();
  fileStore.files.forEach((file) => file.people.forEach((p) => names.add(p)));
  return [...names];
});

function togglePerson(person: string) {
  const idx = selectedPeople.value.indexOf(person);
  if (idx > -1) selectedPeople.value.splice(idx, 1);
  else selectedPeople.value.push(person);
}
function resetToggle() {
  selectedPeople.value = [];
}
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
const selectedFiles = ref<string[]>([]);
function getCleanPeople(people: string[]): string {
  const unique = [...new Set(people)];
  const filtered = unique.filter((p) => p !== "Unknown");
  return filtered.join(", ");
}
// Toggle logic
function toggleSelection(fileName: string) {
  if (selectedFiles.value.includes(fileName)) {
    selectedFiles.value = selectedFiles.value.filter(
      (name) => name !== fileName
    );
  } else {
    selectedFiles.value.push(fileName);
  }
}

const allFilteredSelected = computed(() =>
  filteredFiles.value.every((file) => selectedFiles.value.includes(file.name))
);
function toggleSelectAll() {
  const allNames = filteredFiles.value.map((file) => file.name);

  const allSelected = allNames.every((name) =>
    selectedFiles.value.includes(name)
  );

  if (allSelected) {
    // Deselect all
    selectedFiles.value = selectedFiles.value.filter(
      (name) => !allNames.includes(name)
    );
  } else {
    // Select all filtered files
    const unique = new Set([...selectedFiles.value, ...allNames]);
    selectedFiles.value = [...unique];
  }
}
const downloadSelected = async () => {
  const zip = new JSZip();
  const selected = fileStore.files.filter((file) =>
    selectedFiles.value.includes(file.name)
  );

  // Fetch and add files to the zip
  const fileFetches = selected.map(async (file) => {
    const response = await fetch(file.url);
    const blob = await response.blob();
    zip.file(file.name, blob);
  });

  // Wait for all fetches to finish
  await Promise.all(fileFetches);
  if (process) {
    // Generate zip and trigger download
    const zipBlob = await zip.generateAsync({ type: "blob" });
    saveAs(zipBlob, "photos.zip");
  }
};

onMounted(() => {
  if (fileStore.files.length === 0) {
    router.push("/");
  }
});
</script>

<style scoped>
.container {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  gap: 24px;

  height: 900rem;
}

.sidebar {
  position: sticky;
  top: 2rem;
  width: 10%;
  height: 81vh;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
  display: flex;
  flex-direction: column;
}

.sidebar h2 {
  font-size: 1.5rem;
}

.chips {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  height: 55vh;
  overflow-y: auto;
}

.chip {
  padding: 6px 12px;
  border: 1px solid #aaa;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  background-color: white;
  transition: all 0.2s ease;
  text-align: center;
}

.chip:hover {
  background-color: #e6f0ff;
}

.chip.active {
  background-color: #0066cc;
  color: white;
  border-color: #005bb5;
}
.reset-filter {
  padding: 6px 12px;
  border: 1px solid #aaa;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  background-color: white;
  transition: all 0.2s ease;
}

.download-section {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-btn {
  width: 100%;
  padding: 10px;
  font-size: 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.filter-btn:hover {
  background-color: #0056b3;
}

.gallery {
  flex: 1;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.card {
  position: relative;
  background: white;
  border-radius: 8px;
  height: 10rem;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Overlay text */
.card .overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8); /* Darker = more contrast */
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
  padding: 1rem;
  text-align: center;
}
.card:hover .overlay {
  opacity: 2;
}
.card.selected {
  border: 0.5rem solid #007bff;
  height: 9rem;
}
</style>
