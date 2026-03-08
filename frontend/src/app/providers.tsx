import { GameProvider } from "@/lib/GameContext";
import { TooltipProvider } from "@/components/ui/tooltip";
import type { ReactNode } from "react";

export function Providers({ children }: { children: ReactNode }) {
  return (
    <GameProvider>
      <TooltipProvider>
        {children}
      </TooltipProvider>
    </GameProvider>
  );
}