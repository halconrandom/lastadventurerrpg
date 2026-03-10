"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  X, 
  Hammer, 
  Package, 
  ArrowRight, 
  Check,
  AlertCircle,
  Loader2,
  Hammer as Anvil,
  Scissors,
  Flame,
  Axe,
  Wrench
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { 
  getRecetasDesbloqueadas, 
  craftearItem,
  type RecetaCrafteo 
} from "@/lib/api";

interface CrafteoModalProps {
  isOpen: boolean;
  onClose: () => void;
  slot: number;
  nivelSkill: number;
  onCrafteoSuccess?: (item: any, inventario: any) => void;
}

const ICONOS_ESTACION: Record<string, React.ReactNode> = {
  yunque: <Anvil className="w-5 h-5" />,
  mesa_trabajo: <Wrench className="w-5 h-5" />,
  taller: <Hammer className="w-5 h-5" />,
  horno: <Flame className="w-5 h-5" />,
  banco_carpintero: <Axe className="w-5 h-5" />,
};

const NOMBRE_ESTACION: Record<string, string> = {
  yunque: "Yunque",
  mesa_trabajo: "Mesa de Trabajo",
  taller: "Taller",
  horno: "Horno",
  banco_carpintero: "Banco de Carpintero",
};

export function CrafteoModal({ 
  isOpen, 
  onClose, 
  slot, 
  nivelSkill,
  onCrafteoSuccess 
}: CrafteoModalProps) {
  const [recetas, setRecetas] = useState<Record<string, RecetaCrafteo[]>>({});
  const [estacionSeleccionada, setEstacionSeleccionada] = useState<string>("yunque");
  const [recetaSeleccionada, setRecetaSeleccionada] = useState<RecetaCrafteo | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      cargarRecetas();
    }
  }, [isOpen, nivelSkill]);

  const cargarRecetas = async () => {
    try {
      const data = await getRecetasDesbloqueadas(nivelSkill);
      setRecetas(data);
      if (Object.keys(data).length > 0) {
        setEstacionSeleccionada(Object.keys(data)[0]);
      }
    } catch (err) {
      console.error("Error cargando recetas:", err);
    }
  };

  const handleCraftear = async () => {
    if (!recetaSeleccionada) return;
    
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await craftearItem(slot, recetaSeleccionada.id);
      
      if (result.success) {
        setSuccess(`¡Crafteado: ${recetaSeleccionada.nombre}!`);
        if (result.inventario && onCrafteoSuccess) {
          onCrafteoSuccess(result.item, result.inventario);
        }
        setTimeout(() => {
          onClose();
        }, 1500);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError("Error al craftear");
    } finally {
      setLoading(false);
    }
  };

  const recetasActuales = recetas[estacionSeleccionada] || [];

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="w-full max-w-2xl max-h-[80vh] bg-background border border-border rounded-xl shadow-2xl overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border bg-muted/30">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-primary/10">
                  <Hammer className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h2 className="text-lg font-semibold">Crafteo</h2>
                  <p className="text-xs text-muted-foreground">
                    Nivel de Herrería: {nivelSkill}
                  </p>
                </div>
              </div>
              <Button variant="ghost" size="icon" onClick={onClose}>
                <X className="w-5 h-5" />
              </Button>
            </div>

            {/* Estaciones */}
            <div className="flex gap-2 p-3 border-b border-border overflow-x-auto bg-muted/20">
              {Object.keys(recetas).map((estacion) => (
                <Button
                  key={estacion}
                  variant={estacionSeleccionada === estacion ? "default" : "ghost"}
                  size="sm"
                  onClick={() => setEstacionSeleccionada(estacion)}
                  className="flex items-center gap-2 whitespace-nowrap"
                >
                  {ICONOS_ESTACION[estacion]}
                  {NOMBRE_ESTACION[estacion] || estacion}
                </Button>
              ))}
              {Object.keys(recetas).length === 0 && (
                <p className="text-sm text-muted-foreground p-2">
                  No hay recetas disponibles para tu nivel
                </p>
              )}
            </div>

            {/* Contenido */}
            <div className="p-4 overflow-y-auto max-h-[50vh]">
              {error && (
                <div className="flex items-center gap-2 p-3 mb-4 rounded-lg bg-destructive/10 text-destructive">
                  <AlertCircle className="w-4 h-4" />
                  <span className="text-sm">{error}</span>
                </div>
              )}

              {success && (
                <div className="flex items-center gap-2 p-3 mb-4 rounded-lg bg-green-500/10 text-green-500">
                  <Check className="w-4 h-4" />
                  <span className="text-sm">{success}</span>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {recetasActuales.map((receta) => (
                  <Card
                    key={receta.id}
                    className={cn(
                      "cursor-pointer transition-all hover:border-primary/50",
                      recetaSeleccionada?.id === receta.id 
                        ? "border-primary bg-primary/5" 
                        : "border-border"
                    )}
                    onClick={() => setRecetaSeleccionada(receta)}
                  >
                    <CardContent className="p-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-medium text-sm">{receta.nombre}</h3>
                          <p className="text-xs text-muted-foreground mt-1">
                            Requiere nivel {receta.nivel_requerido}
                          </p>
                        </div>
                        {recetaSeleccionada?.id === receta.id && (
                          <div className="p-1 rounded-full bg-primary/20">
                            <Check className="w-4 h-4 text-primary" />
                          </div>
                        )}
                      </div>

                      {/* Materiales necesarios */}
                      <div className="mt-2 flex flex-wrap gap-1">
                        {receta.materiales.map((mat, idx) => (
                          <span
                            key={idx}
                            className="text-xs px-2 py-0.5 rounded bg-muted text-muted-foreground"
                          >
                            {mat.cantidad}x {mat.id}
                          </span>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {recetasActuales.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Package className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p>No hay recetas disponibles</p>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between p-4 border-t border-border bg-muted/30">
              <div className="text-sm text-muted-foreground">
                {recetaSeleccionada ? (
                  <span>Tiempo: {recetaSeleccionada.tiempo}s</span>
                ) : (
                  <span>Selecciona una receta</span>
                )}
              </div>
              <Button
                onClick={handleCraftear}
                disabled={!recetaSeleccionada || loading}
                className="flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Crafting...
                  </>
                ) : (
                  <>
                    <Hammer className="w-4 h-4" />
                    Craftear
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
