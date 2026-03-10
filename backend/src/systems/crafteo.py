"""
Sistema de Crafteo - Last Adventurer

Gestiona recetas, estaciones y proceso de crafteo.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class TipoEstacion(Enum):
    YUNQUE = "yunque"
    MESA_TRABAJO = "mesa_trabajo"
    TALLER = "taller"
    HORNO = "horno"
    BANCO_CARPINTERO = "banco_carpintero"


@dataclass
class MaterialReceta:
    id: str
    cantidad: int

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "cantidad": self.cantidad}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MaterialReceta":
        return MaterialReceta(id=data["id"], cantidad=data["cantidad"])


@dataclass
class Receta:
    id: str
    nombre: str
    id_item: Optional[str] = None
    materiales: List[MaterialReceta] = field(default_factory=list)
    tiempo: int = 5
    nivel_requerido: int = 1
    herramienta: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "id_item": self.id_item,
            "materiales": [m.to_dict() for m in self.materiales],
            "tiempo": self.tiempo,
            "nivel_requerido": self.nivel_requerido,
            "herramienta": self.herramienta,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Receta":
        materiales = [MaterialReceta.from_dict(m) for m in data.get("materiales", [])]
        return Receta(
            id=data["id"],
            nombre=data["nombre"],
            id_item=data.get("id_item"),
            materiales=materiales,
            tiempo=data.get("tiempo", 5),
            nivel_requerido=data.get("nivel_requerido", 1),
            herramienta=data.get("herramienta"),
        )


@dataclass
class Estacion:
    tipo: TipoEstacion
    nombre: str
    descripcion: str
    recetas_craft: List[Receta] = field(default_factory=list)
    recetas_items: List[Receta] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": self.tipo.value,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "recetas_craft": [r.to_dict() for r in self.recetas_craft],
            "recetas_items": [r.to_dict() for r in self.recetas_items],
        }


class GestorCrafteo:
    def __init__(self):
        self.estaciones: Dict[TipoEstacion, Estacion] = {}
        self.recetas: Dict[str, Receta] = {}
        self._cargar_recetas()

    def _cargar_recetas(self):
        try:
            # Path relativo a este archivo
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ruta = os.path.join(current_dir, "..", "data", "recetas.json")
            
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)

            for estacion_id, estacion_data in data.get("estaciones", {}).items():
                try:
                    tipo = TipoEstacion(estacion_id)
                except ValueError:
                    continue

                recetas_craft = []
                for r in estacion_data.get("recetas_craft", []):
                    recetas_craft.append(Receta.from_dict(r))

                recetas_items = []
                for r in estacion_data.get("recetas_items", []):
                    recetas_items.append(Receta.from_dict(r))

                estacion = Estacion(
                    tipo=tipo,
                    nombre=estacion_data.get("nombre", ""),
                    descripcion=estacion_data.get("descripcion", ""),
                    recetas_craft=recetas_craft,
                    recetas_items=recetas_items,
                )

                self.estaciones[tipo] = estacion

                for r in recetas_craft + recetas_items:
                    self.recetas[r.id] = r

        except Exception as e:
            print(f"Error cargando recetas: {e}")

    def get_estacion(self, tipo: TipoEstacion) -> Optional[Estacion]:
        return self.estaciones.get(tipo)

    def get_receta(self, receta_id: str) -> Optional[Receta]:
        return self.recetas.get(receta_id)

    def get_recetas_por_estacion(self, tipo: TipoEstacion) -> List[Receta]:
        estacion = self.estaciones.get(tipo)
        if estacion:
            return estacion.recetas_craft + estacion.recetas_items
        return []

    def get_recetas_desbloqueadas(self, nivel_skill: int) -> Dict[str, List[Receta]]:
        resultado = {}
        for tipo, estacion in self.estaciones.items():
            recetas_disponibles = []
            for r in estacion.recetas_items:
                if r.nivel_requerido <= nivel_skill:
                    recetas_disponibles.append(r)
            if recetas_disponibles:
                resultado[tipo.value] = [r.to_dict() for r in recetas_disponibles]
        return resultado

    def verificar_materiales(
        self, materiales_necesarios: List[MaterialReceta], inventario: Dict[str, Any]
    ) -> tuple[bool, str]:
        alforjas = inventario.get("alforjas", [])

        materiales_inventario = {}
        for item in alforjas:
            if item and item.get("id_template"):
                item_id = item.get("id_template")
                cantidad = item.get("cantidad", 1)
                materiales_inventario[item_id] = (
                    materiales_inventario.get(item_id, 0) + cantidad
                )

        for mat in materiales_necesarios:
            cantidad_inv = materiales_inventario.get(mat.id, 0)
            if cantidad_inv < mat.cantidad:
                return False, f"Faltan {mat.cantidad - cantidad_inv} x {mat.id}"

        return True, "Materiales suficientes"

    def consumir_materiales(
        self, materiales_necesarios: List[MaterialReceta], inventario: Dict[str, Any]
    ) -> Dict[str, Any]:
        alforjas = inventario.get("alforjas", [])

        materiales_consumidos = {}
        for mat in materiales_necesarios:
            materiales_consumidos[mat.id] = mat.cantidad

        alforjas_actualizadas = []
        for item in alforjas:
            if item and item.get("id_template"):
                item_id = item.get("id_template")
                cantidad_actual = item.get("cantidad", 1)
                cantidad_necesaria = materiales_consumidos.get(item_id, 0)

                if cantidad_necesaria > 0:
                    if cantidad_actual > cantidad_necesaria:
                        item["cantidad"] = cantidad_actual - cantidad_necesaria
                        materiales_consumidos[item_id] = 0
                        alforjas_actualizadas.append(item)
                    else:
                        materiales_consumidos[item_id] -= cantidad_actual
                else:
                    alforjas_actualizadas.append(item)
            else:
                alforjas_actualizadas.append(item)

        inventario["alforjas"] = alforjas_actualizadas
        return inventario


gestor_crafteo = GestorCrafteo()
