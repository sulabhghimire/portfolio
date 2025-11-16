import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

import type { ITheme, IThemeContext } from "./types";
import getThemeFromLocalStorage from "./utils";

const ThemeContext = createContext<IThemeContext | undefined>(undefined);

export const ThemeProvider = ({children}: {children: ReactNode}) => {

    const [theme, setTheme] = useState<ITheme>(getThemeFromLocalStorage);

    useEffect(() => {

        const root = document.documentElement;
        if (theme === "dark") root.classList.add("dark");
        else root.classList.remove("dark");
        localStorage.setItem("theme", theme);

    }, [theme])

    const toggleTheme = () => {
        setTheme(prev => prev === "dark" ? "light" : "dark")
    }

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );

}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context; 
}


