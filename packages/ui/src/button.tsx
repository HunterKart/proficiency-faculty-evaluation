import { type ButtonHTMLAttributes, forwardRef } from "react";

import { cn } from "./utils";

export type ButtonVariant = "default" | "outline";

const baseStyles =
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:pointer-events-none disabled:opacity-50";

const variantStyles: Record<ButtonVariant, string> = {
  default: "bg-slate-900 text-slate-50 hover:bg-slate-900/90",
  outline:
    "border border-slate-700 bg-transparent text-slate-100 hover:bg-slate-900/60"
};

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", ...props }, ref) => (
    <button
      ref={ref}
      className={cn(baseStyles, variantStyles[variant], className)}
      {...props}
    />
  )
);

Button.displayName = "Button";
