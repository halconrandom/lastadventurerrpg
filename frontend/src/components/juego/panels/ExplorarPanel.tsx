"use client";

import { motion } from "framer-motion";
import { Map, ScrollText } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface ExplorarPanelProps {
  explorando: boolean;
  mensajeExploracion: string | null;
  onExplorar: () => void;
}

export function ExplorarPanel({ explorando, mensajeExploracion, onExplorar }: ExplorarPanelProps) {
  return (
    <motion.div
      key="explorar"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="max-w-4xl mx-auto"
    >
      <Card className="p-10 border-[#d4a843]/10 bg-[#0a0a0f]/50 backdrop-blur-sm relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-10 opacity-5 group-hover:opacity-10 transition-opacity">
          <Map className="w-64 h-64" />
        </div>

        <div className="relative z-10">
          <h2 className="font-medieval text-3xl text-[#d4a843] mb-2">
            Tierras Desconocidas
          </h2>
          <p className="text-[#9a978a] mb-10 italic">
            El horizonte se extiende ante ti, lleno de peligros y tesoros por descubrir...
          </p>

          {mensajeExploracion && (
            <div className="mb-10 p-6 rounded-xl bg-[#d4a843]/10 border border-[#d4a843]/30 animate-scale-in">
              <div className="flex items-start gap-4">
                <ScrollText className="w-6 h-6 text-[#d4a843] shrink-0" />
                <p className="text-[#e8e4d9] text-lg font-medieval leading-relaxed">
                  {mensajeExploracion}
                </p>
              </div>
            </div>
          )}

          <div className="flex flex-col items-center justify-center py-12 border-2 border-dashed border-[#2a2a35] rounded-3xl bg-[#0a0a0f]/40">
            <div className={`w-32 h-32 rounded-full border-2 border-[#d4a843]/20 flex items-center justify-center mb-8 bg-[#d4a843]/5 ${explorando ? "animate-pulse" : ""}`}>
              <Map className={`w-14 h-14 text-[#9a978a] ${explorando ? "scale-110 text-[#d4a843]" : ""}`} />
            </div>

            <Button
              size="lg"
              onClick={onExplorar}
              disabled={explorando}
              className="min-w-64 py-6 text-xl shadow-[0_0_30px_rgba(212,168,67,0.15)] hover:shadow-[0_0_40px_rgba(212,168,67,0.25)] transition-all"
            >
              {explorando ? (
                <div className="flex items-center gap-3">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Explorando...</span>
                </div>
              ) : (
                "ADENTRARSE EN EL BOSQUE"
              )}
            </Button>
            <p className="text-[#9a978a]/50 text-xs mt-6 uppercase tracking-widest font-bold">
              Consume 10 de Stamina (Próximamente)
            </p>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
