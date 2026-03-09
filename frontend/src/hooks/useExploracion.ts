"use client";

import { useState, useCallback } from "react";

const API_BASE = "http://localhost:5000/api/exploracion";

interface Zona {
  nombre: string;
  bioma: {
    key: string;
    nombre: string;
    nombre_unico: string;
    variacion: { tipo: string; modificador: string };
  };
  tamaño: number;
  estado: string;
  veces_explorada: number;
}

interface Clima {
  tipo: string;
  intensidad: string;
  duracion: number;
  efectos: string[];
  descripcion: string;
}

interface Ciclo {
  hora: number;
  fase: string;
  luz: number;
}

interface Evento {
  id: string;
  tipo: string;
  titulo: string;
  descripcion: string;
  opciones: Array<{
    texto: string;
    resultado_tipo: string;
  }>;
  rareza: string;
}

interface ResultadoExploracion {
  zona: string;
  bioma: string;
  variacion: string;
  descripcion: string;
  tiles_descubiertos: Array<{ x: number; y: number; terreno: string }>;
  encuentros: Array<{
    entidad_nombre: string;
    hostil: boolean;
    nivel: number;
  }>;
  poi_descubierto: { tipo: string; nombre: string } | null;
  estado_zona: string;
  veces_explorada: number;
}

interface ResultadoEvento {
  tipo_resultado: string;
  texto_resultado: string;
  recompensa: Record<string, unknown> | null;
  consecuencia: Record<string, unknown> | null;
}

interface ExploracionState {
  zona: Zona | null;
  clima: Clima | null;
  ciclo: Ciclo | null;
  evento: Evento | null;
  resultadoExploracion: ResultadoExploracion | null;
  resultadoEvento: ResultadoEvento | null;
  loading: boolean;
  error: string | null;
  log: string[];
  // Coordenadas actuales de exploración
  coordenadas: { x: number; y: number };
}

export function useExploracion(slot: number) {
  const [state, setState] = useState<ExploracionState>({
    zona: null,
    clima: null,
    ciclo: null,
    evento: null,
    resultadoExploracion: null,
    resultadoEvento: null,
    loading: false,
    error: null,
    log: [],
    coordenadas: { x: 0, y: 0 },
  });

  const addLog = useCallback((mensaje: string) => {
    setState((prev) => ({
      ...prev,
      log: [...prev.log.slice(-19), mensaje],
    }));
  }, []);

  const iniciarExploracion = useCallback(
    async (x: number = 0, y: number = 0) => {
      setState((prev) => ({ ...prev, loading: true, error: null }));

      try {
        const response = await fetch(`${API_BASE}/iniciar`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ slot, x, y }),
        });

        const data = await response.json();

        if (!data.success) {
          throw new Error(data.message);
        }

        setState((prev) => ({
          ...prev,
          zona: data.data.zona,
          clima: data.data.clima,
          ciclo: data.data.ciclo,
          coordenadas: { x, y },
          loading: false,
        }));

        addLog(`Llegaste a ${data.data.zona.nombre}`);
        addLog(data.data.descripcion);

        return data.data;
      } catch (error) {
        const mensaje = error instanceof Error ? error.message : "Error desconocido";
        setState((prev) => ({ ...prev, loading: false, error: mensaje }));
        addLog(`Error: ${mensaje}`);
        return null;
      }
    },
    [slot, addLog]
  );

  const explorar = useCallback(async () => {
    if (!state.zona) {
      addLog("Debes llegar a una zona primero");
      return null;
    }

    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      // Usar las coordenadas guardadas en el estado
      const { x, y } = state.coordenadas;

      const response = await fetch(`${API_BASE}/explorar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ slot, x, y }),
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.message);
      }

      const resultado: ResultadoExploracion = data.data;

      setState((prev) => ({
        ...prev,
        resultadoExploracion: resultado,
        zona: prev.zona
          ? { ...prev.zona, estado: resultado.estado_zona, veces_explorada: resultado.veces_explorada }
          : null,
        loading: false,
      }));

      // Agregar al log
      addLog(`Exploraste ${resultado.tiles_descubiertos.length} tiles`);

      if (resultado.encuentros.length > 0) {
        const encuentro = resultado.encuentros[0];
        addLog(`Encuentro: ${encuentro.entidad_nombre} (nv.${encuentro.nivel})`);
      }

      if (resultado.poi_descubierto) {
        addLog(`Descubriste: ${resultado.poi_descubierto.nombre}`);
      }

      return resultado;
    } catch (error) {
      const mensaje = error instanceof Error ? error.message : "Error desconocido";
      setState((prev) => ({ ...prev, loading: false, error: mensaje }));
      addLog(`Error: ${mensaje}`);
      return null;
    }
  }, [slot, state.zona, state.coordenadas, addLog]);

  const obtenerEvento = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true }));

    try {
      const response = await fetch(`${API_BASE}/evento?slot=${slot}&x=0&y=0`);
      const data = await response.json();

      if (!data.success) {
        throw new Error(data.message);
      }

      setState((prev) => ({
        ...prev,
        evento: data.data,
        loading: false,
      }));

      addLog(`Evento: ${data.data.titulo}`);
      return data.data;
    } catch (error) {
      const mensaje = error instanceof Error ? error.message : "Error desconocido";
      setState((prev) => ({ ...prev, loading: false, error: mensaje }));
      return null;
    }
  }, [slot, addLog]);

  const resolverEvento = useCallback(
    async (opcionIndex: number) => {
      if (!state.evento) return null;

      setState((prev) => ({ ...prev, loading: true }));

      try {
        const response = await fetch(`${API_BASE}/evento/resolver`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            evento_id: state.evento.id,
            opcion: opcionIndex,
            contexto: `slot_${slot}`,
          }),
        });

        const data = await response.json();

        if (!data.success) {
          throw new Error(data.message);
        }

        const resultado: ResultadoEvento = data.data;

        setState((prev) => ({
          ...prev,
          resultadoEvento: resultado,
          evento: null,
          loading: false,
        }));

        addLog(resultado.texto_resultado);

        if (resultado.recompensa) {
          const recompensas = Object.entries(resultado.recompensa)
            .filter(([k, v]) => typeof v === "number" && v > 0)
            .map(([k, v]) => `${v} ${k}`)
            .join(", ");
          if (recompensas) addLog(`Recibiste: ${recompensas}`);
        }

        if (resultado.consecuencia) {
          const consecuencias = Object.entries(resultado.consecuencia)
            .filter(([k, v]) => typeof v === "number" && v < 0)
            .map(([k, v]) => `${Math.abs(v as number)} ${k}`)
            .join(", ");
          if (consecuencias) addLog(`Perdiste: ${consecuencias}`);
        }

        return resultado;
      } catch (error) {
        const mensaje = error instanceof Error ? error.message : "Error desconocido";
        setState((prev) => ({ ...prev, loading: false, error: mensaje }));
        addLog(`Error: ${mensaje}`);
        return null;
      }
    },
    [slot, state.evento, addLog]
  );

  const obtenerClima = useCallback(
    async (x: number = 0, y: number = 0, hora: number = 12) => {
      try {
        const response = await fetch(
          `${API_BASE}/clima/${x}/${y}?slot=${slot}&hora=${hora}`
        );
        const data = await response.json();

        if (!data.success) {
          throw new Error(data.message);
        }

        setState((prev) => ({
          ...prev,
          clima: data.data.clima,
          ciclo: data.data.ciclo,
        }));

        return data.data;
      } catch (error) {
        console.error("Error obteniendo clima:", error);
        return null;
      }
    },
    [slot]
  );

  const clearEvento = useCallback(() => {
    setState((prev) => ({
      ...prev,
      evento: null,
      resultadoEvento: null,
    }));
  }, []);

  const clearLog = useCallback(() => {
    setState((prev) => ({ ...prev, log: [] }));
  }, []);

  return {
    ...state,
    iniciarExploracion,
    explorar,
    obtenerEvento,
    resolverEvento,
    obtenerClima,
    clearEvento,
    clearLog,
    addLog,
  };
}
