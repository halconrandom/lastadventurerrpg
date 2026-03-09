"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { 
  Package, 
  Shield, 
  Sword, 
  Wrench, 
  Star,
  ChevronRight,
  Trash2,
  Info
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { Item, RarezaItem, Equipamiento, Manos } from "@/lib/types";

// Colores por rareza
const RARITY_COLORS: Record<RarezaItem, string> = {
  comun: "border-gray-500/50 bg-gray-500/10",
  poco_comun: "border-green-500/50 bg-green-500/10",
  raro: "border-blue-500/50 bg-blue-500/10",
  epico: "border-purple-500/50 bg-purple-500/10",
  legendario: "border-orange-500/50 bg-orange-500/10",
  unico: "border-red-500/50 bg-red-500/10",
};

const RARITY_GLOW: Record<RarezaItem, string> = {
  comun: "",
  poco_comun: "shadow-[0_0_10px_rgba(34,197,94,0.3)]",
  raro: "shadow-[0_0_15px_rgba(59,130,246,0.4)]",
  epico: "shadow-[0_0_20px_rgba(168,85,247,0.5)]",
  legendario: "shadow-[0_0_25px_rgba(249,115,22,0.5)]",
  unico: "shadow-[0_0_30px_rgba(239,68,68,0.6)]",
};

// Datos mock para demostración
const MOCK_ITEMS: Item[] = [
  {
    id: "espada_hierro_001",
    base_id: "espada_hierro",
    nombre: "Espada de Hierro",
    descripcion: "Una espada forjada con hierro común. Resistente y efectiva.",
    tipo: "arma",
    subtipo: "espada_una_mano",
    rareza: "comun",
    cantidad: 1,
    stats: { dano_min: 10, dano_max: 15, velocidad: 1.0 },
    peso: 5,
    valor: 100,
    favorito: false,
    identificado: true,
    durabilidad: 100,
    durabilidad_max: 100,
  },
  {
    id: "pocion_hp_001",
    base_id: "pocion_hp_pequena",
    nombre: "Poción de Vida Pequeña",
    descripcion: "Restaura 25 HP al consumirla.",
    tipo: "consumible",
    rareza: "comun",
    cantidad: 5,
    stats: { hp: 25 },
    peso: 0.5,
    valor: 25,
    favorito: true,
    identificado: true,
  },
  {
    id: "casco_cuero_001",
    base_id: "casco_cuero",
    nombre: "Casco de Cuero",
    descripcion: "Protección ligera para la cabeza.",
    tipo: "armadura",
    subtipo: "casco",
    rareza: "poco_comun",
    cantidad: 1,
    stats: { defensa: 5, evasion: 2 },
    peso: 3,
    valor: 75,
    favorito: false,
    identificado: true,
    durabilidad: 80,
    durabilidad_max: 80,
  },
  {
    id: "hierro_001",
    base_id: "hierro",
    nombre: "Hierro",
    descripcion: "Material de forja común.",
    tipo: "material",
    rareza: "comun",
    cantidad: 15,
    stats: {},
    peso: 1,
    valor: 10,
    favorito: false,
    identificado: true,
  },
];

const MOCK_EQUIPMENT: Equipamiento = {
  casco: null,
  peto: null,
  guantes: null,
  botas: null,
};

const MOCK_HANDS: Manos = {
  izquierda: null,
  derecha: MOCK_ITEMS[0], // Espada equipada
};

// Componente de slot de item
interface ItemSlotProps {
  item: Item | null;
  onClick?: () => void;
  size?: "sm" | "md" | "lg";
  showQuantity?: boolean;
}

function ItemSlot({ item, onClick, size = "md", showQuantity = true }: ItemSlotProps) {
  const sizeClasses = {
    sm: "w-12 h-12",
    md: "w-16 h-16",
    lg: "w-20 h-20",
  };

  if (!item) {
    return (
      <div
        className={cn(
          "rounded-lg border-2 border-dashed border-border/30 bg-muted/20",
          "flex items-center justify-center",
          sizeClasses[size]
        )}
      >
        <div className="size-2 rounded-full bg-border/30" />
      </div>
    );
  }

  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={cn(
        "rounded-lg border-2 cursor-pointer relative group",
        "flex items-center justify-center overflow-hidden",
        "transition-all duration-200",
        sizeClasses[size],
        RARITY_COLORS[item.rareza],
        RARITY_GLOW[item.rareza],
        item.favorito && "ring-2 ring-yellow-500/50"
      )}
    >
      {/* Icono del item */}
      <span className="text-2xl drop-shadow-lg">
        {item.tipo === "arma" && "⚔️"}
        {item.tipo === "armadura" && "🛡️"}
        {item.tipo === "consumible" && "🧪"}
        {item.tipo === "material" && "💎"}
        {item.tipo === "herramienta" && "🔧"}
        {item.tipo === "misc" && "📦"}
      </span>

      {/* Cantidad */}
      {showQuantity && item.cantidad > 1 && (
        <span className="absolute bottom-0.5 right-0.5 bg-black/80 text-white text-[10px] font-bold px-1 rounded">
          x{item.cantidad}
        </span>
      )}

      {/* Favorito */}
      {item.favorito && (
        <Star className="absolute top-0.5 right-0.5 size-3 text-yellow-500 fill-yellow-500" />
      )}

      {/* Durabilidad */}
      {item.durabilidad !== undefined && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-black/50">
          <div
            className="h-full bg-green-500"
            style={{ width: `${(item.durabilidad / (item.durabilidad_max || 100)) * 100}%` }}
          />
        </div>
      )}

      {/* Tooltip en hover */}
      <div className="absolute inset-0 bg-black/80 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
        <Info className="size-4 text-white/70" />
      </div>
    </motion.div>
  );
}

// Componente de slot de equipamiento
interface EquipSlotProps {
  slotName: string;
  item: Item | null;
  icon: React.ReactNode;
  onClick?: () => void;
}

function EquipSlot({ slotName, item, icon, onClick }: EquipSlotProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold">
        {slotName}
      </div>
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onClick}
        className={cn(
          "w-16 h-16 rounded-lg border-2 flex items-center justify-center relative group",
          "transition-all duration-200 cursor-pointer",
          item
            ? cn(RARITY_COLORS[item.rareza], RARITY_GLOW[item.rareza])
            : "border-border/30 bg-muted/20 border-dashed"
        )}
      >
        {item ? (
          <>
            <span className="text-2xl">🛡️</span>
            {item.favorito && (
              <Star className="absolute top-0.5 right-0.5 size-3 text-yellow-500 fill-yellow-500" />
            )}
          </>
        ) : (
          <div className="text-muted-foreground/30">{icon}</div>
        )}
      </motion.div>
    </div>
  );
}

// Componente de slot de mano
interface HandSlotProps {
  slotName: string;
  item: Item | null;
  onClick?: () => void;
}

function HandSlot({ slotName, item, onClick }: HandSlotProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold">
        {slotName}
      </div>
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onClick}
        className={cn(
          "w-20 h-20 rounded-lg border-2 flex items-center justify-center relative group",
          "transition-all duration-200 cursor-pointer",
          item
            ? cn(RARITY_COLORS[item.rareza], RARITY_GLOW[item.rareza])
            : "border-border/30 bg-muted/20 border-dashed"
        )}
      >
        {item ? (
          <>
            <span className="text-3xl">⚔️</span>
            {item.favorito && (
              <Star className="absolute top-0.5 right-0.5 size-3 text-yellow-500 fill-yellow-500" />
            )}
          </>
        ) : (
          <div className="text-muted-foreground/30">
            <Sword className="size-6" />
          </div>
        )}
      </motion.div>
    </div>
  );
}

// Panel principal
export function InventarioPanel() {
  const [selectedItem, selectedItemSet] = useState<Item | null>(null);
  const [alforjasItems] = useState<Item[]>(MOCK_ITEMS);
  const [equipamiento] = useState(MOCK_EQUIPMENT);
  const [manos] = useState(MOCK_HANDS);
  const [oro] = useState(250);
  const [slotsMaximos] = useState(10);

  return (
    <motion.div
      key="inventario"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="h-full"
    >
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
        
        {/* COLUMNA 1: ALFORJAS */}
        <Card className="bg-card/60 backdrop-blur-md border-border/50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-[#d4a843]/10 text-[#d4a843]">
                  <Package className="size-5" />
                </div>
                <div>
                  <h3 className="font-medieval text-xl text-[#d4a843]">Alforjas</h3>
                  <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                    {alforjasItems.length} / {slotsMaximos} slots
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2 bg-muted/30 px-3 py-1.5 rounded-full">
                <span className="text-lg">💰</span>
                <span className="text-[#d4a843] font-medieval text-lg tabular-nums">{oro}</span>
              </div>
            </div>

            {/* Grid de items */}
            <div className="grid grid-cols-4 gap-2">
              {Array.from({ length: slotsMaximos }).map((_, i) => (
                <ItemSlot
                  key={i}
                  item={alforjasItems[i] || null}
                  onClick={() => selectedItemSet(alforjasItems[i] || null)}
                />
              ))}
            </div>

            {/* Peso total */}
            <div className="mt-4 pt-4 border-t border-border/30">
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>Peso total:</span>
                <span>{alforjasItems.reduce((acc, item) => acc + item.peso * item.cantidad, 0).toFixed(1)} kg</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* COLUMNA 2: EQUIPAMIENTO */}
        <Card className="bg-card/60 backdrop-blur-md border-border/50">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400">
                <Shield className="size-5" />
              </div>
              <div>
                <h3 className="font-medieval text-xl text-blue-400">Equipamiento</h3>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                  Defensa total: {Object.values(equipamiento).reduce((acc: number, item) => acc + (item?.stats?.defensa || 0), 0)}
                </p>
              </div>
            </div>

            {/* Slots de equipamiento */}
            <div className="flex flex-col items-center gap-4">
              <EquipSlot
                slotName="Casco"
                item={equipamiento.casco}
                icon={<Shield className="size-5" />}
              />
              <EquipSlot
                slotName="Peto"
                item={equipamiento.peto}
                icon={<Shield className="size-5" />}
              />
              <EquipSlot
                slotName="Guantes"
                item={equipamiento.guantes}
                icon={<Shield className="size-5" />}
              />
              <EquipSlot
                slotName="Botas"
                item={equipamiento.botas}
                icon={<Shield className="size-5" />}
              />
            </div>

            {/* Stats de defensa */}
            <div className="mt-6 pt-4 border-t border-border/30 space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-muted-foreground">Defensa física:</span>
                <span className="text-blue-400">0</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-muted-foreground">Resistencia mágica:</span>
                <span className="text-purple-400">0</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-muted-foreground">Evasión:</span>
                <span className="text-green-400">+0%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* COLUMNA 3: ARMAS/HERRAMIENTAS */}
        <Card className="bg-card/60 backdrop-blur-md border-border/50">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-red-500/10 text-red-400">
                <Sword className="size-5" />
              </div>
              <div>
                <h3 className="font-medieval text-xl text-red-400">Armas / Herramientas</h3>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                  En mano
                </p>
              </div>
            </div>

            {/* Slots de manos */}
            <div className="flex justify-center gap-8 mb-6">
              <HandSlot
                slotName="Mano Izq."
                item={manos.izquierda}
                onClick={() => selectedItemSet(manos.izquierda)}
              />
              <HandSlot
                slotName="Mano Der."
                item={manos.derecha}
                onClick={() => selectedItemSet(manos.derecha)}
              />
            </div>

            {/* Herramienta activa */}
            <div className="border-t border-border/30 pt-4">
              <div className="flex items-center gap-2 mb-3">
                <Wrench className="size-4 text-muted-foreground" />
                <span className="text-xs uppercase tracking-wider text-muted-foreground font-bold">
                  Herramienta Activa
                </span>
              </div>
              <div className="flex items-center justify-center">
                <div className="w-20 h-20 rounded-lg border-2 border-dashed border-border/30 bg-muted/20 flex items-center justify-center">
                  <span className="text-muted-foreground/30 text-xs">Ninguna</span>
                </div>
              </div>
            </div>

            {/* Stats de arma */}
            {manos.derecha && (
              <div className="mt-6 pt-4 border-t border-border/30 space-y-2">
                <div className="text-xs font-bold text-muted-foreground uppercase mb-2">
                  {manos.derecha.nombre}
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-muted-foreground">Daño:</span>
                  <span className="text-red-400">
                    {manos.derecha.stats.dano_min}-{manos.derecha.stats.dano_max}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-muted-foreground">Velocidad:</span>
                  <span className="text-green-400">{manos.derecha.stats.velocidad?.toFixed(1)}x</span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Panel de información del item seleccionado */}
      {selectedItem && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50"
        >
          <Card className="bg-card/95 backdrop-blur-md border-border/50 shadow-xl min-w-[400px]">
            <CardContent className="p-4">
              <div className="flex items-start gap-4">
                <div className={cn(
                  "w-16 h-16 rounded-lg border-2 flex items-center justify-center",
                  RARITY_COLORS[selectedItem.rareza],
                  RARITY_GLOW[selectedItem.rareza]
                )}>
                  <span className="text-3xl">
                    {selectedItem.tipo === "arma" && "⚔️"}
                    {selectedItem.tipo === "armadura" && "🛡️"}
                    {selectedItem.tipo === "consumible" && "🧪"}
                    {selectedItem.tipo === "material" && "💎"}
                    {selectedItem.tipo === "herramienta" && "🔧"}
                    {selectedItem.tipo === "misc" && "📦"}
                  </span>
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h4 className="font-medieval text-lg text-[#d4a843]">{selectedItem.nombre}</h4>
                    {selectedItem.favorito && <Star className="size-4 text-yellow-500 fill-yellow-500" />}
                  </div>
                  <p className="text-xs text-muted-foreground mb-2">{selectedItem.descripcion}</p>
                  <div className="flex gap-4 text-xs">
                    <span className="text-muted-foreground">Tipo: <span className="text-white">{selectedItem.tipo}</span></span>
                    <span className="text-muted-foreground">Peso: <span className="text-white">{selectedItem.peso} kg</span></span>
                    <span className="text-muted-foreground">Valor: <span className="text-[#d4a843]">{selectedItem.valor} oro</span></span>
                  </div>
                </div>
                <button
                  onClick={() => selectedItemSet(null)}
                  className="text-muted-foreground hover:text-white transition-colors"
                >
                  ✕
                </button>
              </div>
              
              {/* Stats del item */}
              {Object.keys(selectedItem.stats).length > 0 && (
                <div className="mt-3 pt-3 border-t border-border/30 grid grid-cols-3 gap-2">
                  {selectedItem.stats.dano_min !== undefined && (
                    <div className="text-xs">
                      <span className="text-muted-foreground">Daño: </span>
                      <span className="text-red-400">{selectedItem.stats.dano_min}-{selectedItem.stats.dano_max}</span>
                    </div>
                  )}
                  {selectedItem.stats.defensa !== undefined && (
                    <div className="text-xs">
                      <span className="text-muted-foreground">Defensa: </span>
                      <span className="text-blue-400">+{selectedItem.stats.defensa}</span>
                    </div>
                  )}
                  {selectedItem.stats.velocidad !== undefined && (
                    <div className="text-xs">
                      <span className="text-muted-foreground">Velocidad: </span>
                      <span className="text-green-400">{selectedItem.stats.velocidad}x</span>
                    </div>
                  )}
                </div>
              )}

              {/* Acciones */}
              <div className="mt-3 pt-3 border-t border-border/30 flex gap-2">
                {(selectedItem.tipo === "arma" || selectedItem.tipo === "armadura") && (
                  <button className="flex-1 py-2 px-4 bg-[#d4a843]/20 hover:bg-[#d4a843]/30 text-[#d4a843] rounded-lg text-sm font-bold transition-colors">
                    Equipar
                  </button>
                )}
                {selectedItem.tipo === "consumible" && (
                  <button className="flex-1 py-2 px-4 bg-green-500/20 hover:bg-green-500/30 text-green-400 rounded-lg text-sm font-bold transition-colors">
                    Usar
                  </button>
                )}
                <button className="py-2 px-4 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg text-sm font-bold transition-colors flex items-center gap-2">
                  <Trash2 className="size-4" />
                  Tirar
                </button>
                <button className="py-2 px-4 bg-muted/30 hover:bg-muted/50 text-muted-foreground rounded-lg text-sm font-bold transition-colors">
                  <Star className={cn("size-4", selectedItem.favorito && "fill-yellow-500 text-yellow-500")} />
                </button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </motion.div>
  );
}