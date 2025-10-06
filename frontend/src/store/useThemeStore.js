import { create } from "zustand";

export const useThemeStore = create((set) => ({
  theme: localStorage.getItem("tulululu-theme") || "coffee",
  setTheme: (theme) => {
    localStorage.setItem("tulululu-theme", theme);
    set({ theme });
  },
}));