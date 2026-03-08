"use client";

import { motion } from "framer-motion";
import { Package } from "lucide-react";
import { Card } from "@/components/ui/Card";
import type { DatosJuego } from "@/lib/types";

interface InventarioPanelProps {
  datos: DatosJuego;
}

export function InventarioPanel({ datos }: InventarioPanelProps) {
  return (
    <motion.div
      key="inventario"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
    >
      <Card className="p-10 bg-[#0a0a0f]/60 backdrop-blur-md border-[#2a2a35]">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6 mb-12">
          <div className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-[#d4a843]/10 text-[#d4a843]">
              <Package className="w-8 h-8" />
            </div>
            <div>
              <h2 className="font-medieval text-3xl text-[#d4a843]">Alforjas del Aventurero</h2>
              <p className="text-[#9a978a] text-sm uppercase tracking-widest">
                Capacidad: {datos.inventario.items.length} / {datos.inventario.slots_maximos}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-8 py-3 px-8 rounded-full bg-[#12121a] border border-[#d4a843]/20 shadow-[0_0_20px_rgba(212,168,67,0.05)]">
            <div className="flex items-center gap-2">
              <span className="text-2xl">💰</span>
              <span className="text-[#d4a843] font-medieval text-2xl tabular-nums">
                {datos.inventario.oro}
              </span>
              <span className="text-[#9a978a] text-[10px] ml-1 uppercase font-bold">oro</span>
            </div>
          </div>
        </div>

        {/* Grid de inventario */}
        <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-4">
          {Array.from({ length: datos.inventario.slots_maximos }).map((_, i) => {
            const item = datos.inventario.items[i];
            return (
              <div
                key={i}
                className={`aspect-square bg-[#0a0a0f] border-2 rounded-2xl flex items-center justify-center transition-all duration-300 cursor-pointer group relative shadow-inner ${
                  item
                    ? "border-[#d4a843]/30 hover:border-[#d4a843] bg-gradient-to-br from-[#12121a] to-[#0a0a0f]"
                    : "border-[#2a2a35] hover:border-[#3a3a45] opacity-40 hover:opacity-60"
                }`}
              >
                {item ? (
                  <div className="text-center group-hover:scale-110 transition-transform">
                    <span className="text-4xl drop-shadow-[0_0_10px_rgba(0,0,0,0.5)]">📦</span>
                    {item.cantidad > 1 && (
                      <span className="absolute bottom-2 right-2 bg-[#d4a843] text-[#0a0a0f] text-[10px] font-bold px-1.5 py-0.5 rounded-lg shadow-md">
                        x{item.cantidad}
                      </span>
                    )}
                  </div>
                ) : (
                  <div className="w-4 h-4 rounded-full border border-[#2a2a35]" />
                )}
              </div>
            );
          })}
        </div>

        {datos.inventario.items.length === 0 && (
          <div className="text-center py-20 border-t border-[#2a2a35] mt-10">
            <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
              <Package className="w-8 h-8 text-[#9a978a]/30" />
            </div>
            <p className="text-[#9a978a] italic">
              Tus alforjas están vacías por ahora...
            </p>
          </div>
        )}
      </Card>
    </motion.div>
  );
}
