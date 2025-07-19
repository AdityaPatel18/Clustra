// stores/fileStore.ts
import { defineStore } from 'pinia'

type FileEntry = {
  name: string
  file: File
  url: string
}

export const useFileStore = defineStore('fileStore', {
  state: () => ({
    files: [] as FileEntry[],
  }),

  actions: {
    addFiles(newFiles: File[]) {
      const wrapped = newFiles.map(file => ({
        name: file.name,
        file,
        url: URL.createObjectURL(file),
      }))
      this.files.push(...wrapped)
    },

    clearFiles() {
      this.files.forEach(f => URL.revokeObjectURL(f.url)) // Clean memory
      this.files = []
    },
  },
})