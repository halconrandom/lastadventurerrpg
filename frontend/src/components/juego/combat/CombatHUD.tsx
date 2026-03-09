"use client";

import { motion } from "framer-motion";
import type { ParticipanteCombate } from "@/lib/types";

interface CombatHUDProps {
  participante: ParticipanteCombate;
  esJugador: boolean;
}

export function CombatHUD({ participante, esJugador }: CombatHUDProps) {
  const hpPercent = (participante.hp / participante.hp_max) * 100;
  const manaPercent = (participante.mana / participante.mana_max) * 100;
  const staminaPercent = (participante.stamina / participante.stamina_max) * 100;

  const hpColor = hpPercent > 50 ? "bg-green-500" : hpPercent > 25 ? "bg-yellow-500" : "bg-red-500";

  return (
    <div className={`p-4 rounded-xl ${esJugador ? "bg-[#1a2a1a]/80 border-[#4a8a4a]/30" : "bg-[#2a1a1a]/80 border-[#8a4a4a]/30"} border`}>
      {/* Nombre y Nivel */}
      <div className="flex justify-between items-center mb-3">
        <h3 className={`font-medieval text-lg ${esJugador ? "text-[#4a8a4a]" : "text-[#c44536]"}`}>
          {participante.nombre}
        </h3>
        <span className="text-xs bg-black/30 px-2 py-1 rounded text-[#9a978a]">
          NV. {participante.nivel}
        </span>
      </div>

      {/* HP Bar */}
      <div className="mb-2">
        <div className="flex justify-between text-xs mb-1">
          <span className="text-[#9a978a]">HP</span>
          <span className="text-white font-bold">
            {participante.hp}/{participante.hp_max}
          </span>
        </div>
        <div className="h-3 bg-black/50 rounded-full overflow-hidden">
          <motion.div
            className={`h-full ${hpColor}`}
            initial={{ width: 0 }}
            animate={{ width: `${hpPercent}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Mana Bar */}
      {participante.mana_max > 0 && (
        <div className="mb-2">
          <div className="flex justify-between text-xs mb-1">
            <span className="text-[#9a978a]">Mana</span>
            <span className="text-blue-400 font-bold">
              {participante.mana}/{participante.mana_max}
            </span>
          </div>
          <div className="h-2 bg-black/50 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-blue-500"
              initial={{ width: 0 }}
              animate={{ width: `${manaPercent}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>
      )}

      {/* Stamina Bar */}
      <div>
        <div className="flex justify-between text-xs mb-1">
          <span className="text-[#9a978a]">Stamina</span>
          <span className="text-yellow-400 font-bold">
            {participante.stamina}/{participante.stamina_max}
          </span>
        </div>
        <div className="h-2 bg-black/50 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-yellow-500"
            initial={{ width: 0 }}
            animate={{ width: `${staminaPercent}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Stats rápidos */}
      <div className="flex gap-4 mt-3 text-xs text-[#9a978a]">
        <span>ATK: {participante.ataque}</span>
        <span>DEF: {participante.defensa}%</span>
        <span>SPD: {participante.velocidad}</span>
      </div>

      {/* Estado */}
      {participante.esta_bloqueando && (
        <div className="mt-2 text-xs text-blue-400 flex items-center gap-1">
          <span>🛡️ Bloqueando</span>
        </div>
      )}
      {!participante.esta_vivo && (
        <div className="mt-2 text-xs text-red-400 font-bold">
          💀 Derrotado
        </div>
      )}
    </div>
  );
}