"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
  TooltipPortal,
} from "@/components/ui/tooltip";
import { Info } from "lucide-react";

export type ProgressBarVariant = "hp" | "mana" | "stamina" | "exp" | "default";

interface ProgressBarProps {
  /** Valor actual */
  current: number;
  /** Valor máximo */
  max: number;
  /** Variante de color */
  variant?: ProgressBarVariant;
  /** Mostrar label */
  showLabel?: boolean;
  /** Label personalizado */
  label?: string;
  /** Tamaño */
  size?: "sm" | "md" | "lg";
  /** Tooltip con título y descripción */
  tooltip?: {
    title: string;
    description: string;
  };
  /** Clases adicionales */
  className?: string;
  /** Animar cambios */
  animate?: boolean;
  /** Mostrar porcentaje */
  showPercentage?: boolean;
}

const variantStyles: Record<ProgressBarVariant, {
  gradient: string;
  glow: string;
  icon?: string;
}> = {
  hp: {
    gradient: "bg-gradient-to-r from-[#c44536] to-[#8b2942]",
    glow: "shadow-[0_0_10px_rgba(196,69,54,0.4)]",
  },
  mana: {
    gradient: "bg-gradient-to-r from-[#3b82f6] to-[#1d4ed8]",
    glow: "shadow-[0_0_10px_rgba(59,130,246,0.4)]",
  },
  stamina: {
    gradient: "bg-gradient-to-r from-[#22c55e] to-[#16a34a]",
    glow: "shadow-[0_0_10px_rgba(34,197,94,0.4)]",
  },
  exp: {
    gradient: "bg-gradient-to-r from-[#d4a843] to-[#a67c00]",
    glow: "shadow-[0_0_10px_rgba(212,168,67,0.4)]",
  },
  default: {
    gradient: "bg-gradient-to-r from-[#4a4a4a] to-[#2a2a2a]",
    glow: "",
  },
};

const sizeStyles = {
  sm: {
    height: "h-1",
    text: "text-[10px]",
    padding: "px-1",
  },
  md: {
    height: "h-2.5",
    text: "text-xs",
    padding: "px-2",
  },
  lg: {
    height: "h-4",
    text: "text-sm",
    padding: "px-3",
  },
};

export function ProgressBar({
  current,
  max,
  variant = "default",
  showLabel = false,
  label,
  size = "md",
  tooltip,
  className,
  animate = true,
  showPercentage = false,
}: ProgressBarProps) {
  const percentage = Math.min(100, Math.max(0, (current / max) * 100));
  const styles = variantStyles[variant];
  const sizeConfig = sizeStyles[size];

  const bar = (
    <div className={cn("w-full space-y-1.5", className)}>
      {/* Label y valores */}
      {(showLabel || label) && (
        <div className={cn("flex justify-between items-center", sizeConfig.padding)}>
          {label && (
            <span className={cn("font-medium text-[#9a978a] uppercase tracking-wider", sizeConfig.text)}>
              {label}
            </span>
          )}
          <div className="flex items-center gap-2">
            {showPercentage && (
              <span className={cn("text-[#e8e4d9]", sizeConfig.text)}>
                {Math.round(percentage)}%
              </span>
            )}
            <span className={cn("text-[#9a978a]", sizeConfig.text)}>
              {current} / {max}
            </span>
          </div>
        </div>
      )}

      {/* Barra de progreso */}
      <div
        className={cn(
          "relative w-full overflow-hidden rounded-full bg-[#1a1a25] border border-white/5",
          sizeConfig.height
        )}
      >
        {/* Fondo con patrón */}
        <div className="absolute inset-0 bg-gradient-to-b from-white/5 to-transparent pointer-events-none" />

        {/* Barra de relleno */}
        <motion.div
          initial={animate ? { width: 0 } : false}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className={cn(
            "h-full relative",
            styles.gradient,
            percentage > 0 && styles.glow
          )}
        >
          {/* Brillo superior */}
          <div className="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent" />
          
          {/* Animación de brillo */}
          {percentage > 0 && (
            <div className="absolute inset-0 overflow-hidden">
              <div
                className="absolute inset-0 animate-shimmer"
                style={{
                  background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)",
                  backgroundSize: "200% 100%",
                }}
              />
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );

  // Si hay tooltip, envolver en TooltipProvider
  if (tooltip) {
    return (
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="cursor-help">{bar}</div>
        </TooltipTrigger>
        <TooltipPortal>
          <TooltipContent
            side="top"
            align="start"
            className="bg-[#0f0f15] border border-[#d4a843]/30 p-3 max-w-xs shadow-xl"
          >
            <div className="space-y-1">
              <p className="text-[#d4a843] font-medium flex items-center gap-2">
                <Info className="w-3.5 h-3.5" />
                {tooltip.title}
              </p>
              <p className="text-[11px] text-[#9a978a] italic leading-relaxed">
                {tooltip.description}
              </p>
            </div>
          </TooltipContent>
        </TooltipPortal>
      </Tooltip>
    );
  }

  return bar;
}

// Variante compacta para usar en headers/sidebars
export function ProgressBarCompact({
  current,
  max,
  variant = "default",
  showValues = true,
  className,
}: {
  current: number;
  max: number;
  variant?: ProgressBarVariant;
  showValues?: boolean;
  className?: string;
}) {
  const percentage = Math.min(100, Math.max(0, (current / max) * 100));
  const styles = variantStyles[variant];

  return (
    <div className={cn("flex items-center gap-2", className)}>
      <div className="flex-1 relative h-1.5 overflow-hidden rounded-full bg-[#1a1a25] border border-white/5">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.3 }}
          className={cn("h-full", styles.gradient)}
        />
      </div>
      {showValues && (
        <span className="text-[10px] text-[#9a978a] tabular-nums min-w-[3rem] text-right">
          {current}/{max}
        </span>
      )}
    </div>
  );
}

// Variante para stats con icono
export function ProgressBarWithIcon({
  current,
  max,
  variant = "default",
  icon,
  label,
  className,
}: {
  current: number;
  max: number;
  variant?: ProgressBarVariant;
  icon: React.ReactNode;
  label: string;
  className?: string;
}) {
  const percentage = Math.min(100, Math.max(0, (current / max) * 100));
  const styles = variantStyles[variant];

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <div className="flex items-center gap-2 min-w-[80px]">
        <span className="text-[#9a978a]">{icon}</span>
        <span className="text-[10px] uppercase font-bold tracking-widest text-[#9a978a]">
          {label}
        </span>
      </div>
      <div className="flex-1 relative h-3 overflow-hidden rounded-full bg-[#1a1a25] border border-white/5">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5 }}
          className={cn("h-full", styles.gradient)}
        />
      </div>
      <span className="text-xs text-[#e8e4d9] tabular-nums min-w-[4rem] text-right">
        {current} / {max}
      </span>
    </div>
  );
}

export default ProgressBar;