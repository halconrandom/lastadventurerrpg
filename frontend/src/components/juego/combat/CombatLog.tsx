"use client";

import { motion, AnimatePresence } from "framer-motion";
import type { EntradaLogCombate } from "@/lib/types";

interface CombatLogProps {
  log: EntradaLogCombate[];
}

export function CombatLog({ log }: CombatLogProps) {
  return (
    <div className="bg-[#0a0a0f]/80 border border-[#2a2a35] rounded-xl p-4 h-48 overflow-y-auto custom-scrollbar">
      <h4 className="font-medieval text-[#d4a843] mb-3 text-sm">Registro de Combate</h4>
      
      <div className="space-y-2">
        <AnimatePresence>
          {log.map((entrada, index) => (
            <motion.div
              key={`${entrada.turno}-${index}`}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0 }}
              className={`text-xs ${
                entrada.es_critico
                  ? "text-yellow-400 font-bold"
                  : entrada.es_evasion
                  ? "text-blue-400"
                  : entrada.accion === "inicio"
                  ? "text-[#d4a843]"
                  : "text-[#9a978a]"
              }`}
            >
              {entrada.es_critico && "⚡ "}
              {entrada.es_evasion && "💨 "}
              {entrada.mensaje}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {log.length === 0 && (
        <div className="text-xs text-[#9a978a]/50 italic">
          El combate aún no ha comenzado...
        </div>
      )}
    </div>
  );
}