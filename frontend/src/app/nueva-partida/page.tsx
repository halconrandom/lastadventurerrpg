"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { useGame } from "@/lib/GameContext";
import { Swords, Heart, Shield, Zap } from "lucide-react";

type Paso = "nombre" | "genero" | "dificultad" | "resumen";
type Genero = "masculino" | "femenino" | "no_especificar";
type Dificultad = "facil" | "normal" | "dificil";

export default function NuevaPartidaPage() {
  const router = useRouter();
  const { crearNuevaPartida } = useGame();

  const [paso, pasoSet] = useState<Paso>("nombre");
  const [nombre, nombreSet] = useState("");
  const [genero, generoSet] = useState<Genero | null>(null);
  const [dificultad, dificultadSet] = useState<Dificultad | null>(null);
  const [cargando, cargandoSet] = useState(false);
  const [error, errorSet] = useState<string | null>(null);

  const handleSiguiente = () => {
    if (paso === "nombre" && nombre.length >= 3) {
      pasoSet("genero");
    } else if (paso === "genero" && genero) {
      pasoSet("dificultad");
    } else if (paso === "dificultad" && dificultad) {
      pasoSet("resumen");
    }
  };

  const handleAnterior = () => {
    if (paso === "genero") pasoSet("nombre");
    else if (paso === "dificultad") pasoSet("genero");
    else if (paso === "resumen") pasoSet("dificultad");
  };

  const handleCrear = async () => {
    if (!nombre || !genero || !dificultad) return;

    cargandoSet(true);
    errorSet(null);

    try {
      await crearNuevaPartida(nombre, genero, dificultad);
      router.push("/juego");
    } catch (err) {
      errorSet(err instanceof Error ? err.message : "Error al crear partida");
    } finally {
      cargandoSet(false);
    }
  };

  const handleVolver = () => {
    router.push("/");
  };

  const dificultadesInfo = {
    facil: {
      titulo: "Fácil",
      descripcion: "+20% HP, -10% daño enemigo",
      color: "text-[#22c55e]",
      stats: "Ideal para nuevos jugadores",
    },
    normal: {
      titulo: "Normal",
      descripcion: "Sin modificadores",
      color: "text-[#d4a843]",
      stats: "Experiencia equilibrada",
    },
    dificil: {
      titulo: "Difícil",
      descripcion: "-10% HP, +10% daño enemigo",
      color: "text-[#c44536]",
      stats: "Para veteranos",
    },
  };

  return (
    <main className="min-h-screen bg-[#0a0a0f] relative overflow-hidden">
      {/* Fondo con patrón */}
      <div
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: `
            linear-gradient(90deg, rgba(42,42,53,0.3) 1px, transparent 1px),
            linear-gradient(rgba(42,42,53,0.3) 1px, transparent 1px)
          `,
          backgroundSize: "50px 50px",
        }}
      />

      {/* Contenido */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center p-8">
        {/* Título */}
        <h1 className="font-medieval text-4xl text-[#d4a843] mb-2 animate-fade-in">
          Crear Personaje
        </h1>
        <div className="h-[2px] w-48 bg-gradient-to-r from-transparent via-[#d4a843] to-transparent mb-8" />

        {/* Indicador de pasos */}
        <div className="flex items-center gap-2 mb-8 animate-fade-in" style={{ animationDelay: "0.1s" }}>
          {(["nombre", "genero", "dificultad", "resumen"] as Paso[]).map((p, i) => (
            <div key={p} className="flex items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center font-medieval text-sm transition-all duration-300 ${
                  paso === p
                    ? "bg-[#d4a843] text-[#0a0a0f]"
                    : i < ["nombre", "genero", "dificultad", "resumen"].indexOf(paso)
                    ? "bg-[#a67c00] text-[#0a0a0f]"
                    : "bg-[#1a1a25] text-[#9a978a] border border-[#2a2a35]"
                }`}
              >
                {i + 1}
              </div>
              {i < 3 && (
                <div
                  className={`w-12 h-[2px] transition-all duration-300 ${
                    i < ["nombre", "genero", "dificultad", "resumen"].indexOf(paso)
                      ? "bg-[#a67c00]"
                      : "bg-[#2a2a35]"
                  }`}
                />
              )}
            </div>
          ))}
        </div>

        {/* Paso: Nombre */}
        {paso === "nombre" && (
          <div className="w-full max-w-md animate-fade-in">
            <Card className="p-6">
              <h2 className="font-medieval text-2xl text-[#d4a843] text-center mb-6">
                ¿Cómo te llamas, aventurero?
              </h2>
              <input
                type="text"
                value={nombre}
                onChange={(e) => nombreSet(e.target.value)}
                placeholder="Tu nombre..."
                maxLength={20}
                className="w-full bg-[#0a0a0f] border border-[#2a2a35] rounded px-4 py-3 text-[#e8e4d9] font-medieval text-lg focus:border-[#d4a843] focus:outline-none focus:shadow-[0_0_10px_rgba(212,168,67,0.2)] transition-all"
              />
              {nombre.length > 0 && nombre.length < 3 && (
                <p className="text-[#c44536] text-sm mt-2 text-center">
                  El nombre debe tener al menos 3 caracteres
                </p>
              )}
              <div className="flex justify-end mt-6">
                <Button onClick={handleSiguiente} disabled={nombre.length < 3}>
                  Continuar
                </Button>
              </div>
            </Card>
          </div>
        )}

        {/* Paso: Género */}
        {paso === "genero" && (
          <div className="w-full max-w-2xl animate-fade-in">
            <h2 className="font-medieval text-2xl text-[#d4a843] text-center mb-6">
              ¿Cuál es tu género?
            </h2>
            <div className="grid grid-cols-3 gap-4">
              {(["masculino", "femenino", "no_especificar"] as Genero[]).map((g) => (
                <Card
                  key={g}
                  hoverable
                  selected={genero === g}
                  onClick={() => generoSet(g)}
                  className="p-6 cursor-pointer"
                >
                  <CardContent className="text-center">
                    <div className="text-4xl mb-3">
                      {g === "masculino" ? "♂" : g === "femenino" ? "♀" : "?"}
                    </div>
                    <p className="font-medieval text-lg text-[#d4a843]">
                      {g === "masculino"
                        ? "Masculino"
                        : g === "femenino"
                        ? "Femenino"
                        : "No especificar"}
                    </p>
                    <p className="text-sm text-[#9a978a] mt-2">
                      {g === "masculino"
                        ? "Él"
                        : g === "femenino"
                        ? "Ella"
                        : "El aventurero"}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
            <div className="flex justify-between mt-6">
              <Button variant="secondary" onClick={handleAnterior}>
                Anterior
              </Button>
              <Button onClick={handleSiguiente} disabled={!genero}>
                Continuar
              </Button>
            </div>
          </div>
        )}

        {/* Paso: Dificultad */}
        {paso === "dificultad" && (
          <div className="w-full max-w-2xl animate-fade-in">
            <h2 className="font-medieval text-2xl text-[#d4a843] text-center mb-6">
              Elige tu dificultad
            </h2>
            <div className="grid grid-cols-3 gap-4">
              {(["facil", "normal", "dificil"] as Dificultad[]).map((d) => (
                <Card
                  key={d}
                  hoverable
                  selected={dificultad === d}
                  onClick={() => dificultadSet(d)}
                  className="p-6 cursor-pointer"
                >
                  <CardContent className="text-center">
                    <div className="text-4xl mb-3">
                      {d === "facil" ? "🌱" : d === "normal" ? "⚔️" : "💀"}
                    </div>
                    <p className={`font-medieval text-lg ${dificultadesInfo[d].color}`}>
                      {dificultadesInfo[d].titulo}
                    </p>
                    <p className="text-sm text-[#9a978a] mt-2">
                      {dificultadesInfo[d].descripcion}
                    </p>
                    <p className="text-xs text-[#9a978a]/70 mt-1">
                      {dificultadesInfo[d].stats}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
            <div className="flex justify-between mt-6">
              <Button variant="secondary" onClick={handleAnterior}>
                Anterior
              </Button>
              <Button onClick={handleSiguiente} disabled={!dificultad}>
                Continuar
              </Button>
            </div>
          </div>
        )}

        {/* Paso: Resumen */}
        {paso === "resumen" && (
          <div className="w-full max-w-md animate-fade-in">
            <Card className="p-6">
              <h2 className="font-medieval text-2xl text-[#d4a843] text-center mb-6">
                Tu aventurero
              </h2>

              {/* Avatar placeholder */}
              <div className="w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-b from-[#1a1a25] to-[#12121a] border-2 border-[#d4a843] flex items-center justify-center">
                <Swords className="w-12 h-12 text-[#d4a843]" />
              </div>

              {/* Datos del personaje */}
              <div className="space-y-3 mb-6">
                <div className="flex justify-between items-center py-2 border-b border-[#2a2a35]">
                  <span className="text-[#9a978a]">Nombre</span>
                  <span className="font-medieval text-[#d4a843]">{nombre}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-[#2a2a35]">
                  <span className="text-[#9a978a]">Género</span>
                  <span className="font-medieval text-[#d4a843]">
                    {genero === "masculino"
                      ? "Masculino"
                      : genero === "femenino"
                      ? "Femenino"
                      : "No especificar"}
                  </span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-[#2a2a35]">
                  <span className="text-[#9a978a]">Dificultad</span>
                  <span className={`font-medieval ${dificultadesInfo[dificultad!].color}`}>
                    {dificultadesInfo[dificultad!].titulo}
                  </span>
                </div>
              </div>

              {/* Stats base */}
              <div className="bg-[#0a0a0f] rounded p-4 mb-6">
                <h3 className="font-medieval text-sm text-[#9a978a] mb-3">
                  Stats iniciales
                </h3>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="flex items-center gap-2">
                    <Heart className="w-4 h-4 text-[#c44536]" />
                    <span className="text-[#9a978a]">HP:</span>
                    <span className="text-[#e8e4d9]">100</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Swords className="w-4 h-4 text-[#d4a843]" />
                    <span className="text-[#9a978a]">ATK:</span>
                    <span className="text-[#e8e4d9]">10</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Shield className="w-4 h-4 text-[#3b82f6]" />
                    <span className="text-[#9a978a]">DEF:</span>
                    <span className="text-[#e8e4d9]">5%</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Zap className="w-4 h-4 text-[#22c55e]" />
                    <span className="text-[#9a978a]">Vel:</span>
                    <span className="text-[#e8e4d9]">10</span>
                  </div>
                </div>
              </div>

              {error && (
                <p className="text-[#c44536] text-sm text-center mb-4">{error}</p>
              )}

              <div className="flex justify-between">
                <Button variant="secondary" onClick={handleAnterior}>
                  Editar
                </Button>
                <Button onClick={handleCrear} disabled={cargando}>
                  {cargando ? "Creando..." : "¡Comenzar!"}
                </Button>
              </div>
            </Card>
          </div>
        )}

        {/* Botón de volver al menú */}
        <div className="mt-8">
          <Button variant="secondary" onClick={handleVolver}>
            Volver al Menú
          </Button>
        </div>
      </div>
    </main>
  );
}