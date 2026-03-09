import { GameProvider } from "@/lib/GameContext";
import { NotificationProvider } from "@/lib/NotificationContext";
import { TooltipProvider } from "@/components/ui/tooltip";
import type { ReactNode } from "react";

export function Providers({ children }: { children: ReactNode }) {
  return (
    <GameProvider>
      <NotificationProvider>
        <TooltipProvider>
          {children}
        </TooltipProvider>
      </NotificationProvider>
    </GameProvider>
  );
}