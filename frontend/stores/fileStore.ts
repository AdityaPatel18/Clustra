// stores/fileStore.ts
import { defineStore } from 'pinia'

export const useFileStore = defineStore('fileStore', {
  state: () => ({
    files: [] as { file: File; url: string; name: string }[],
  }),
  actions: {
    addFiles(newFiles: File[]) {
      const processed = newFiles.map(file => ({
        file,
        url: URL.createObjectURL(file),
        name: file.name,
      }))
      this.files.push(...processed)
    },
    clearFiles() {
      // Revoke old object URLs before clearing
      this.files.forEach(({ url }) => URL.revokeObjectURL(url))
      this.files = []
    },
  },
})