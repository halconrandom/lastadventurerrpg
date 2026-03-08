"use client";

import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  selected?: boolean;
  hoverable?: boolean;
}

export function Card({
  children,
  className = "",
  onClick,
  selected = false,
  hoverable = false,
}: CardProps) {
  const baseStyles =
    "bg-gradient-to-b from-[#1a1a25] to-[#12121a] border rounded relative";

  const borderStyles = selected
    ? "border-[#d4a843] shadow-[0_0_20px_rgba(212,168,67,0.3)]"
    : "border-[#2a2a35]";

  const hoverStyles = hoverable
    ? "cursor-pointer hover:border-[#d4a843] hover:shadow-[0_0_15px_rgba(212,168,67,0.2)] transition-all duration-300"
    : "";

  return (
    <div
      className={`${baseStyles} ${borderStyles} ${hoverStyles} ${className}`}
      onClick={onClick}
    >
      {/* Línea dorada superior */}
      <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[#a67c00] to-transparent" />
      {children}
    </div>
  );
}

interface CardHeaderProps {
  children: ReactNode;
  className?: string;
}

export function CardHeader({ children, className = "" }: CardHeaderProps) {
  return (
    <div className={`p-4 border-b border-[#2a2a35] ${className}`}>
      <h3 className="font-medieval text-[#d4a843] text-lg">{children}</h3>
    </div>
  );
}

interface CardContentProps {
  children: ReactNode;
  className?: string;
}

export function CardContent({ children, className = "" }: CardContentProps) {
  return <div className={`p-4 ${className}`}>{children}</div>;
}