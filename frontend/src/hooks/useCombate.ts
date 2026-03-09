"use client";

import { useState, useCallback } from "react";
import { useGame } from "@/lib/GameContext";
import type {
  EstadoCombate,
  ParticipanteCombate,
  EntradaLogCombate,
  ResultadoAccion,
  RecompensasCombate,
} from "@/lib/types";

interface UseCombateState {
  enCombate: boolean;
  estado: EstadoCombate | null;
  turno: number;
  jugadores: ParticipanteCombate[];
  enemigos: ParticipanteCombate[];
  log: EntradaLogCombate[];
  cargando: boolean;
  error: string | null;
}

interface UseCombateReturn extends UseCombateState {
  // Acciones
  atacar: (objetivoId?: string) => Promise<ResultadoAccion | null>;
  usarHabilidad: (habilidadNombre: string, objetivoId?: string) => Promise<ResultadoAccion | null>;
  usarItem: (itemId: string) => Promise<ResultadoAccion | null>;
  bloquear: () => Promise<ResultadoAccion | null>;
  huir: () => Promise<ResultadoAccion | null>;
  resolverTurnoEnemigos: () => Promise<void>;
  finalizarCombate: () => Promise<RecompensasCombate | null>;
  
  // Utilidades
  getJugadorActivo: () => ParticipanteCombate | null;
  getEnemigosVivos: () => ParticipanteCombate[];
  getJugadoresVivos: () => ParticipanteCombate[];
  esTurnoJugador: () => boolean;
  combateTerminado: () => boolean;
  victoria: () => boolean;
  derrota: () => boolean;
}

export function useCombate(): UseCombateReturn {
  const {
    enCombate,
    estadoCombate,
    cargandoCombate,
    iniciarCombate: startCombate,
    ejecutarAccionCombate,
    resolverTurnoEnemigos: resolverEnemigos,
    finalizarCombate: endCombate,
  } = useGame();

  const [error, setError] = useState<string | null>(null);

  // Extraer datos del estado
  const estado = estadoCombate?.estado ?? null;
  const turno = estadoCombate?.turno ?? 0;
  const jugadores = estadoCombate ? Object.values(estadoCombate.jugadores) : [];
  const enemigos = estadoCombate ? Object.values(estadoCombate.enemigos) : [];
  const log = estadoCombate?.log ?? [];

  // Acciones de combate
  const atacar = useCallback(async (objetivoId?: string): Promise<ResultadoAccion | null> => {
    try {
      setError(null);
      const resultado = await ejecutarAccionCombate("atacar", objetivoId);
      return resultado;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al atacar");
      return null;
    }
  }, [ejecutarAccionCombate]);

  const usarHabilidad = useCallback(async (
    habilidadNombre: string,
    objetivoId?: string
  ): Promise<ResultadoAccion | null> => {
    try {
      setError(null);
      const resultado = await ejecutarAccionCombate("habilidad", objetivoId, habilidadNombre);
      return resultado;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al usar habilidad");
      return null;
    }
  }, [ejecutarAccionCombate]);

  const usarItem = useCallback(async (itemId: string): Promise<ResultadoAccion | null> => {
    try {
      setError(null);
      const resultado = await ejecutarAccionCombate("item", undefined, undefined);
      return resultado;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al usar item");
      return null;
    }
  }, [ejecutarAccionCombate]);

  const bloquear = useCallback(async (): Promise<ResultadoAccion | null> => {
    try {
      setError(null);
      const resultado = await ejecutarAccionCombate("bloquear");
      return resultado;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al bloquear");
      return null;
    }
  }, [ejecutarAccionCombate]);

  const huir = useCallback(async (): Promise<ResultadoAccion | null> => {
    try {
      setError(null);
      const resultado = await ejecutarAccionCombate("huir");
      return resultado;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al huir");
      return null;
    }
  }, [ejecutarAccionCombate]);

  const resolverTurnoEnemigos = useCallback(async (): Promise<void> => {
    try {
      setError(null);
      await resolverEnemigos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al resolver turno enemigo");
    }
  }, [resolverEnemigos]);

  const finalizarCombate = useCallback(async (): Promise<RecompensasCombate | null> => {
    try {
      setError(null);
      const resultado = await endCombate();
      return resultado.recompensas ?? null;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al finalizar combate");
      return null;
    }
  }, [endCombate]);

  // Utilidades
  const getJugadorActivo = useCallback((): ParticipanteCombate | null => {
    return jugadores.find(j => j.es_jugador && j.esta_vivo) ?? null;
  }, [jugadores]);

  const getEnemigosVivos = useCallback((): ParticipanteCombate[] => {
    return enemigos.filter(e => e.esta_vivo);
  }, [enemigos]);

  const getJugadoresVivos = useCallback((): ParticipanteCombate[] => {
    return jugadores.filter(j => j.esta_vivo);
  }, [jugadores]);

  const esTurnoJugador = useCallback((): boolean => {
    return estado === "turno_jugador";
  }, [estado]);

  const combateTerminado = useCallback((): boolean => {
    return estado === "victoria" || estado === "derrota" || estado === "huida";
  }, [estado]);

  const victoria = useCallback((): boolean => {
    return estado === "victoria";
  }, [estado]);

  const derrota = useCallback((): boolean => {
    return estado === "derrota";
  }, [estado]);

  return {
    // Estado
    enCombate,
    estado,
    turno,
    jugadores,
    enemigos,
    log,
    cargando: cargandoCombate,
    error,

    // Acciones
    atacar,
    usarHabilidad,
    usarItem,
    bloquear,
    huir,
    resolverTurnoEnemigos,
    finalizarCombate,

    // Utilidades
    getJugadorActivo,
    getEnemigosVivos,
    getJugadoresVivos,
    esTurnoJugador,
    combateTerminado,
    victoria,
    derrota,
  };
}