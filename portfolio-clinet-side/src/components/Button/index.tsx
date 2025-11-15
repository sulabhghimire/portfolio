

type ButtonVariant = "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
type ButtonSize = "sm" | "default" | "lg" | "icon";

interface IButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

const Button = ( {
  children,
  variant = "default",
  size = "default",
  className = "",
  ...props
}: IButtonProps) => {

    const base =
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all " +
    "disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2";

    const variants: Record<ButtonVariant, string> = {
    default: "bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500",
    destructive: "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500",
    outline: "border border-gray-300 text-gray-900 hover:bg-gray-100 dark:border-gray-700 dark:text-gray-100",
    secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100",
    ghost: "hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-800 dark:text-gray-100",
    link: "text-blue-600 underline-offset-4 hover:underline dark:text-blue-400",
  };

  const sizes: Record<ButtonSize, string> = {
    sm: "h-8 px-3 text-xs",
    default: "h-9 px-4",
    lg: "h-10 px-6 text-base",
    icon: "h-9 w-9 p-0",
  };


  const classes = `${base} ${variants[variant]} ${sizes[size]} ${className}`;

  return (
    <button className={classes} {...props}>
      {children}
    </button>
  );
}

export default Button