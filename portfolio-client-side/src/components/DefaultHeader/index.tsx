import { Moon, Sun } from "lucide-react";
import { useTheme } from "../../context/ThemeContext"
import Button from "../Button";
import Avatar from "../Avatar";

const DefaultHeader = () => {

    const { theme, toggleTheme } = useTheme();

    return (
        <header className="border-b border-zinc-200 dark:border-zinc-800 px-4 py-3">
        <div className="max-w-3xl mx-auto flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <Avatar/>
            <h1 className="text-zinc-900 dark:text-zinc-100">
              Sulabh Ghimire - Software Engineer
            </h1>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            aria-label="Toggle theme"
            className="cursor-pointer"
          >
            {theme === "light" ? (
              <Moon className="h-5 w-5" />
            ) : (
              <Sun className="h-5 w-5" />
            )}
          </Button>
        </div>
      </header>
    )
}

export default DefaultHeader;