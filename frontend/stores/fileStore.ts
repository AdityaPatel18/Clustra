// stores/fileStore.ts
import { defineStore } from "pinia";

export const useFileStore = defineStore("fileStore", {
  state: () => ({
    files: [] as { file: File; url: string; name: string; people: string[] }[],
    people_faces: [] as {
      label: string;
      face: string;
      name?: string;
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
    updateFaceLabels(nameMap: Record<string, string>) {
      // Update people_faces with user-defined names
      this.people_faces = this.people_faces.map((face) => ({
        ...face,
        name: nameMap[face.label] || "",
      }));

      // Create a lookup from label to name
      const labelToName: Record<string, string> = {};
      this.people_faces.forEach((face) => {
        if (face.name) labelToName[face.label] = face.name;
      });

      // Update people[] in each file using labelToName
      this.files = this.files.map((file) => ({
        ...file,
        people: file.people.map((label) => labelToName[label] || "Unknown"),
      }));
    },
  },
});
