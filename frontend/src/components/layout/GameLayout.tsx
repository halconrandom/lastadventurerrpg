"use client";

import * as React from "react";
import { useState, ReactNode } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

// ============================================
// TIPOS
// ============================================

interface GameLayoutProps {
  children: ReactNode;
  sidebar?: ReactNode;
  header?: ReactNode;
  footer?: ReactNode;
  /** Sidebar colapsado por defecto */
  defaultCollapsed?: boolean;
  /** Clases adicionales para el contenedor principal */
  className?: string;
  /** Clases para el área de contenido */
  contentClassName?: string;
}

// ============================================
// CONTEXTO PARA SIDEBAR
// ============================================

interface SidebarContextType {
  isCollapsed: boolean;
  toggle: () => void;
  collapse: () => void;
  expand: () => void;
}

const SidebarContext = React.createContext<SidebarContextType | undefined>(undefined);

export function useSidebar() {
  const context = React.useContext(SidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a GameLayout");
  }
  return context;
}

// ============================================
// GAME LAYOUT
// ============================================

export function GameLayout({
  children,
  sidebar,
  header,
  footer,
  defaultCollapsed = false,
  className,
  contentClassName,
}: GameLayoutProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);

  const toggle = () => setIsCollapsed((prev) => !prev);
  const collapse = () => setIsCollapsed(true);
  const expand = () => setIsCollapsed(false);

  return (
    <SidebarContext.Provider value={{ isCollapsed, toggle, collapse, expand }}>
      <div className={cn("flex h-screen overflow-hidden bg-[#0a0a0f]", className)}>
        {/* Sidebar */}
        {sidebar && (
          <AnimatePresence mode="wait">
            <motion.aside
              initial={false}
              animate={{ width: isCollapsed ? 60 : 280 }}
              transition={{ duration: 0.3, ease: "easeInOut" }}
              className="flex-shrink-0 h-full bg-[#12121a] border-r border-white/5 overflow-hidden"
            >
              {sidebar}
            </motion.aside>
          </AnimatePresence>
        )}

        {/* Contenido principal */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          {/* Header */}
          {header && (
            <header className="flex-shrink-0 h-14 border-b border-white/5">
              {header}
            </header>
          )}

          {/* Área de contenido */}
          <main className={cn("flex-1 overflow-y-auto custom-scrollbar", contentClassName)}>
            {children}
          </main>

          {/* Footer */}
          {footer && (
            <footer className="flex-shrink-0 border-t border-white/5">
              {footer}
            </footer>
          )}
        </div>
      </div>
    </SidebarContext.Provider>
  );
}

// ============================================
// COMPONENTES AUXILIARES
// ============================================

/** Botón para colapsar/expandir el sidebar */
export function SidebarToggle({ className }: { className?: string }) {
  const { isCollapsed, toggle } = useSidebar();

  return (
    <button
      onClick={toggle}
      className={cn(
        "p-2 rounded-lg text-[#9a978a] hover:text-[#e8e4d9] hover:bg-white/5 transition-colors",
        className
      )}
      aria-label={isCollapsed ? "Expandir sidebar" : "Colapsar sidebar"}
    >
      <svg
        className={cn("w-5 h-5 transition-transform", isCollapsed && "rotate-180")}
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
        />
      </svg>
    </button>
  );
}

/** Wrapper para contenido del sidebar */
export function SidebarContent({ children, className }: { children: ReactNode; className?: string }) {
  const { isCollapsed } = useSidebar();

  return (
    <div
      className={cn(
        "h-full flex flex-col",
        isCollapsed ? "w-[60px]" : "w-[280px]",
        className
      )}
    >
      {children}
    </div>
  );
}

/** Sección dentro del sidebar */
export function SidebarSection({
  children,
  title,
  className,
  collapsible = false,
  defaultOpen = true,
}: {
  children: ReactNode;
  title?: ReactNode;
  className?: string;
  collapsible?: boolean;
  defaultOpen?: boolean;
}) {
  const { isCollapsed } = useSidebar();
  const [isOpen, setIsOpen] = useState(defaultOpen);

  if (isCollapsed) {
    return null;
  }

  return (
    <div className={cn("border-t border-white/5 first:border-t-0", className)}>
      {title && (
        <button
          onClick={collapsible ? () => setIsOpen(!isOpen) : undefined}
          className={cn(
            "w-full flex items-center justify-between px-4 py-3 text-xs uppercase tracking-wider text-[#9a978a]",
            collapsible && "hover:text-[#e8e4d9] cursor-pointer"
          )}
        >
          <span>{title}</span>
          {collapsible && (
            <svg
              className={cn("w-4 h-4 transition-transform", !isOpen && "-rotate-90")}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          )}
        </button>
      )}
      <AnimatePresence mode="wait">
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4">{children}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/** Header del sidebar con toggle */
export function SidebarHeader({
  children,
  className,
}: {
  children?: ReactNode;
  className?: string;
}) {
  const { isCollapsed } = useSidebar();

  return (
    <div
      className={cn(
        "flex items-center justify-between px-4 py-3 border-b border-white/5",
        isCollapsed && "justify-center px-2",
        className
      )}
    >
      {children}
    </div>
  );
}

/** Footer del sidebar */
export function SidebarFooter({ children, className }: { children?: ReactNode; className?: string }) {
  const { isCollapsed } = useSidebar();

  return (
    <div
      className={cn(
        "mt-auto border-t border-white/5 px-4 py-3",
        isCollapsed && "px-2",
        className
      )}
    >
      {children}
    </div>
  );
}

export default GameLayout;