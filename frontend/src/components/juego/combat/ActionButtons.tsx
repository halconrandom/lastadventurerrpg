"use client";

import { motion } from "framer-motion";
import { Sword, Shield, Zap, Package, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ActionButtonsProps {
  onAtacar: () => void;
  onHabilidad: () => void;
  onItem: () => void;
  onBloquear: () => void;
  onHuir: () => void;
  cargando: boolean;
  turnoJugador: boolean;
  staminaActual: number;
  manaActual: number;
}

export function ActionButtons({
  onAtacar,
  onHabilidad,
  onItem,
  onBloquear,
  onHuir,
  cargando,
  turnoJugador,
  staminaActual,
  manaActual,
}: ActionButtonsProps) {
  const disabled = cargando || !turnoJugador;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-[#12121a]/90 border border-[#2a2a35] rounded-xl p-4"
    >
      <div className="grid grid-cols-5 gap-3">
        {/* Atacar */}
        <Button
          variant="default"
          size="lg"
          onClick={onAtacar}
          disabled={disabled}
          className="flex flex-col items-center gap-2 py-4"
        >
          <Sword className="w-6 h-6" />
          <span className="text-xs">Atacar</span>
        </Button>

        {/* Habilidad */}
        <Button
          variant="secondary"
          size="lg"
          onClick={onHabilidad}
          disabled={disabled || (staminaActual < 10 && manaActual < 10)}
          className="flex flex-col items-center gap-2 py-4"
        >
          <Zap className="w-6 h-6" />
          <span className="text-xs">Habilidad</span>
        </Button>

        {/* Item */}
        <Button
          variant="secondary"
          size="lg"
          onClick={onItem}
          disabled={disabled}
          className="flex flex-col items-center gap-2 py-4"
        >
          <Package className="w-6 h-6" />
          <span className="text-xs">Item</span>
        </Button>

        {/* Bloquear */}
        <Button
          variant="secondary"
          size="lg"
          onClick={onBloquear}
          disabled={disabled || staminaActual < 5}
          className="flex flex-col items-center gap-2 py-4"
        >
          <Shield className="w-6 h-6" />
          <span className="text-xs">Bloquear</span>
        </Button>

        {/* Huir */}
        <Button
          variant="destructive"
          size="lg"
          onClick={onHuir}
          disabled={disabled}
          className="flex flex-col items-center gap-2 py-4"
        >
          <LogOut className="w-6 h-6" />
          <span className="text-xs">Huir</span>
        </Button>
      </div>

      {/* Indicador de turno */}
      <div className="mt-4 text-center">
        {cargando ? (
          <span className="text-[#d4a843] animate-pulse">Procesando...</span>
        ) : turnoJugador ? (
          <span className="text-green-400">Tu turno - Elige una acción</span>
        ) : (
          <span className="text-red-400">Turno del enemigo</span>
        )}
      </div>
    </motion.div>
  );
}