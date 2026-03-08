"use client";

import type { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
  children: ReactNode;
}

export function Button({
  variant = "primary",
  size = "md",
  children,
  className = "",
  ...props
}: ButtonProps) {
  const baseStyles =
    "font-medieval cursor-pointer transition-all duration-300 relative overflow-hidden";

  const variants = {
    primary:
      "bg-gradient-to-b from-[#1a1a25] to-[#12121a] border-2 border-[#a67c00] text-[#d4a843] hover:border-[#d4a843] hover:text-[#f0c654] hover:-translate-y-0.5 hover:shadow-[0_4px_20px_rgba(212,168,67,0.3)]",
    secondary:
      "bg-gradient-to-b from-[#1a1a25] to-[#12121a] border border-[#2a2a35] text-[#9a978a] hover:border-[#d4a843] hover:text-[#d4a843]",
    danger:
      "bg-gradient-to-b from-[#1a1a25] to-[#12121a] border-2 border-[#8b2942] text-[#c44536] hover:border-[#c44536] hover:text-[#ff6b6b]",
  };

  const sizes = {
    sm: "px-4 py-2 text-sm",
    md: "px-8 py-3 text-base",
    lg: "px-12 py-4 text-lg",
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      <span className="relative z-10">{children}</span>
      <span className="absolute inset-0 bg-gradient-to-r from-transparent via-[rgba(212,168,67,0.1)] to-transparent -translate-x-full hover:translate-x-full transition-transform duration-500" />
    </button>
  );
}