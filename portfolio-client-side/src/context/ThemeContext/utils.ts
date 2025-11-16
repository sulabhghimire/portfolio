import type { ITheme } from "./types";

function getThemeFromLocalStorage() {
    const stored = localStorage.getItem("theme") as ITheme | null;
    if (stored) return stored;

    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light"; 
}

export default  getThemeFromLocalStorage ;