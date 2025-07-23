<template>
  <div class="container">
    <!-- Sidebar Filters -->
    <aside class="sidebar">
      <h2>Filter by People</h2>
      <div class="chips">
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
const selectedFiles = ref<string[]>([])
function getCleanPeople(people: string[]): string {
  const unique = [...new Set(people)];
  const filtered = unique.filter(p => p !== 'Unknown');
  return filtered.join(', ');
}
// Toggle logic
function toggleSelection(fileName: string) {
  if (selectedFiles.value.includes(fileName)) {
    selectedFiles.value = selectedFiles.value.filter(name => name !== fileName)
  } else {
    selectedFiles.value.push(fileName)
  }
}
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
}

.sidebar {
  width: 10%;
  flex-shrink: 0;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
}

.sidebar h2 {
  font-size: 18px;
  margin-bottom: 12px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.chip {
  padding: 6px 12px;
  border: 1px solid #aaa;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  background-color: white;
  transition: all 0.2s ease;
}

.chip:hover {
  background-color: #e6f0ff;
}

.chip.active {
  background-color: #0066cc;
  color: white;
  border-color: #005bb5;
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
  border: .5rem solid #007bff;
  height: 9rem;
}
</style>