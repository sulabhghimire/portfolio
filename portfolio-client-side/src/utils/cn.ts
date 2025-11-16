import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

// Combines clsx + tailwind-merge for smart class merging
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
