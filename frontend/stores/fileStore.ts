// stores/fileStore.ts
import { defineStore } from "pinia";

export const useFileStore = defineStore("fileStore", {
  state: () => ({
    files: [] as { file: File; url: string; name: string; people: string[] }[],
    people_faces: [] as {
      label: string;
      face: string; //base 64 image string
    }[],
  }),
  actions: {
    addFiles(newFiles: File[]) {
      const processed = newFiles.map((file) => ({
        file,
        url: URL.createObjectURL(file),
        name: file.name,
        people: [],
      }));
      this.files.push(...processed);
    },
    clearFiles() {
      this.files.forEach(({ url }) => URL.revokeObjectURL(url));
      this.files = [];
    },
  },
});
