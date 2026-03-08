"""
Last Adventurer - Backend API
FastAPI server para el frontend
"""
import sys
import os
from pathlib import Path

# Añadir src al path para imports
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json

from systems.save_manager import SaveManager
from models.stats import Stats
from models.personaje import Personaje
from models.experiencia import SistemaHabilidades

# Crear la aplicación FastAPI
app = FastAPI(
    title="Last Adventurer API",
    description="Backend API para el juego Last Adventurer",
    version="1.0.0"
)

# Configurar CORS para permitir requests del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del SaveManager
save_manager = SaveManager()


# ============== MODELOS PYDANTIC ==============

class CrearPersonajeRequest(BaseModel):
    """Request para crear un nuevo personaje"""
    nombre: str
    genero: str = "no_especificar"
    dificultad: str = "normal"


class GuardarPartidaRequest(BaseModel):
    """Request para guardar una partida"""
    datos: Dict[str, Any]


class ApiResponse(BaseModel):
    """Respuesta estándar de la API"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


# ============== ENDPOINTS ==============

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {"message": "Last Adventurer API", "version": "1.0.0"}


@app.get("/api/slots")
async def obtener_slots():
    """Obtiene información de todos los slots de guardado"""
    slots = []
    for slot_num in range(1, SaveManager.NUM_SLOTS + 1):
        info = save_manager.obtener_info_slot(slot_num)
        slots.append({
            "numero": slot_num,
            "ocupado": info is not None,
            "info": info
        })
    return {"slots": slots}


@app.get("/api/slots/{slot_num}")
async def obtener_slot(slot_num: int):
    """Obtiene información de un slot específico"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        raise HTTPException(status_code=400, detail=f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    info = save_manager.obtener_info_slot(slot_num)
    return {
        "numero": slot_num,
        "ocupado": info is not None,
        "info": info
    }


@app.post("/api/partida/nueva")
async def nueva_partida(request: CrearPersonajeRequest):
    """Crea una nueva partida"""
    # Validar nombre
    if len(request.nombre) < 3:
        raise HTTPException(status_code=400, detail="El nombre debe tener al menos 3 caracteres")
    
    # Validar género
    generos_validos = ["masculino", "femenino", "no_especificar"]
    if request.genero.lower() not in generos_validos:
        raise HTTPException(status_code=400, detail=f"Género inválido. Debe ser uno de: {generos_validos}")
    
    # Validar dificultad
    dificultades_validas = ["facil", "normal", "dificil"]
    if request.dificultad.lower() not in dificultades_validas:
        raise HTTPException(status_code=400, detail=f"Dificultad inválida. Debe ser una de: {dificultades_validas}")
    
    # Buscar slot libre
    slot_libre = None
    for slot_num in range(1, SaveManager.NUM_SLOTS + 1):
        if not save_manager.slot_existe(slot_num):
            slot_libre = slot_num
            break
    
    if slot_libre is None:
        raise HTTPException(status_code=400, detail="Todos los slots están ocupados")
    
    # Crear datos de la partida
    datos = save_manager.crear_save_vacio(
        nombre=request.nombre,
        genero=request.genero.lower(),
        dificultad=request.dificultad.lower()
    )
    
    # Guardar
    exito, mensaje = save_manager.guardar(slot_libre, datos)
    
    if not exito:
        raise HTTPException(status_code=500, detail=mensaje)
    
    return {
        "success": True,
        "message": mensaje,
        "data": {
            "slot": slot_libre,
            "datos": datos
        }
    }


@app.get("/api/partida/{slot_num}")
async def cargar_partida(slot_num: int):
    """Carga una partida desde un slot"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        raise HTTPException(status_code=400, detail=f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    datos, mensaje = save_manager.cargar(slot_num)
    
    if not datos:
        raise HTTPException(status_code=404, detail=mensaje)
    
    return {
        "success": True,
        "message": mensaje,
        "data": datos
    }


@app.put("/api/partida/{slot_num}")
async def guardar_partida(slot_num: int, request: GuardarPartidaRequest):
    """Guarda una partida en un slot"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        raise HTTPException(status_code=400, detail=f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    exito, mensaje = save_manager.guardar(slot_num, request.datos)
    
    if not exito:
        raise HTTPException(status_code=500, detail=mensaje)
    
    return {
        "success": True,
        "message": mensaje
    }


@app.delete("/api/partida/{slot_num}")
async def eliminar_partida(slot_num: int):
    """Elimina una partida de un slot"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        raise HTTPException(status_code=400, detail=f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    exito, mensaje = save_manager.eliminar(slot_num)
    
    if not exito:
        raise HTTPException(status_code=404, detail=mensaje)
    
    return {
        "success": True,
        "message": mensaje
    }


@app.get("/api/personaje/{slot_num}")
async def obtener_personaje(slot_num: int):
    """Obtiene los datos del personaje de una partida"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        raise HTTPException(status_code=400, detail=f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    datos, _ = save_manager.cargar(slot_num)
    
    if not datos:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    
    return {
        "success": True,
        "data": datos.get("personaje", {})
    }


# ============== ENDPOINTS DE DATOS ==============

@app.get("/api/data/items")
async def obtener_items():
    """Obtiene la lista de items del juego"""
    items_path = src_dir / "data" / "items.json"
    
    if not items_path.exists():
        raise HTTPException(status_code=404, detail="Archivo de items no encontrado")
    
    with open(items_path, "r", encoding="utf-8") as f:
        items = json.load(f)
    
    return {"items": items}


@app.get("/api/data/arquetipos")
async def obtener_arquetipos():
    """Obtiene la lista de arquetipos del juego"""
    arquetipos_path = src_dir / "data" / "arquetipos.json"
    
    if not arquetipos_path.exists():
        raise HTTPException(status_code=404, detail="Archivo de arquetipos no encontrado")
    
    with open(arquetipos_path, "r", encoding="utf-8") as f:
        arquetipos = json.load(f)
    
    return {"arquetipos": arquetipos}


# ============== INICIO DEL SERVIDOR ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)