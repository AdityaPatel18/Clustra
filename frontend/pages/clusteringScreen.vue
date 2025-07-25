<template>
<div class="title-container">
  <div class="clustra-title">Clustra</div>
  <div class="center-subtitle">Everything’s sorted! Pick your favorites to save.</div>
</div>
  <div class="container">
    
    <aside class="sidebar">
      <h2>Filter & Download</h2>
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
      <div class="download-section">
        <button class="selectButton" @click="toggleSelectAll">
          {{ allFilteredSelected ? "Deselect All" : "Select All" }}
        </button>
        <button class="download" @click="downloadSelected">Download</button>
        <p>{{ selectedFiles.length }} images selected</p>
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
const filteredFiles = computed(() => {
  if (selectedPeople.value.length === 0) return fileStore.files;

  return fileStore.files.filter((file) =>
    selectedPeople.value.every((person) => file.people.includes(person))
  );
});

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
  selectedFiles.value = selectedFiles.value.filter(
    name => !filteredFiles.value.some(f => f.name === name)
  );
} else {
  const filteredNames = filteredFiles.value.map(f => f.name);
  selectedFiles.value = [...new Set([...selectedFiles.value, ...filteredNames])];
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
  const zipBlob = await zip.generateAsync({ type: "blob" });
  const { saveAs } = await import('file-saver');
  saveAs(zipBlob, "photos.zip");

};

onMounted(() => {
  if (fileStore.files.length === 0) {
    router.replace("/");
  }
});
</script>

<style scoped>
.container {
  display: flex;
  margin: 0 auto;
  padding: 40px;
  gap: 24px;
  background-color: beige;
  height: 900rem;
}

.title-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  align-items: center;
  background: beige;
  padding: 1rem 0;
  padding-bottom: 0rem;
}

.clustra-title {
  justify-self: start;
  padding-left: 2rem;
  font-size: 3rem;
  font-weight: bold;
  color: #2e1503;
}

.center-subtitle {
    grid-column: 2 / 4;
  justify-self: self-start;
  font-size: 2rem;
  font-weight: 500;
  color: #3a2e2e;
}

.sidebar {
  position: sticky;
  top: 2rem;
  min-width: 8rem;
  height: 81vh;
  padding: 1rem;
  border: 2px solid #2e1503;
  border-radius: 8px;
  background: #F5F5DC;
  display: flex;
  flex-direction: column;
  gap: .5rem;
scrollbar-color: transparent transparent;
}

.sidebar:hover {
      scrollbar-width: thin;
  scrollbar-color: #572908 transparent;
}

.sidebar h2 {
  font-size: 1.25rem;
}

.chips {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  height: 55vh;
  overflow-y: auto;
  padding-right: .5rem;
  
}

.chip, .reset-filter {
  padding: 6px 12px;
  border: 2px solid #2e1503;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  background-color: transparent;
  transition: all 0.2s ease;
  text-align: center;
}

.chip:hover, .reset-filter:hover {
  background-color: #D2691E;
}

.chip.active {
  background-color: #D2691E;
  color: 2e1503;
}

.download-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selectButton {
    width: 90%;
  padding: 10px;
  font-size: 15px;
  background-color: beige;
  color: #2e1503;
  border: 2px solid #2e1503;
  border-radius: 2rem;
  cursor: pointer;
  transition: background-color 0.2s ease;  
}

.selectButton:hover {
    background-color: #D2691E;
}
.filter-btn, .download {
  width: 90%;
  padding: 10px;
  font-size: 15px;
  background-color: beige;
  color: #2e1503;
  border: 2px solid #2e1503;
  border-radius: 2rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.filter-btn:hover {
  background-color: #D2691E;
}

.download:hover {
    background-color: green;
}
.download {
    background-color: #D2691E;
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
  opacity: 1;
}
.card.selected {
  border: 0.5rem solid #D2691E;
  height: 9rem;
}

.download-section p {
    text-align: center;
}



</style>
