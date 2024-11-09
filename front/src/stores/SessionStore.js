import { defineStore } from "pinia";

export const useSessionStore = defineStore("session", {
  state: () => ({
    tabs:[],
  }),
  actions: {
    async pushTab(tab) {
      this.tabs.push(tab)
    },
  },
  persist: {
    enabled: true,
  },
});
