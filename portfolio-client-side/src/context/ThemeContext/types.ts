export type ITheme = "light" | "dark";

export interface IThemeContext {
    theme: ITheme;
    toggleTheme: VoidFunction;
}