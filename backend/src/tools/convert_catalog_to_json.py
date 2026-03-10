#!/usr/bin/env python3
"""
Catalógo a JSON Converter
Lee CATALOGO_OBJETOS.md y genera backend/src/data/objetos.json
Reglas simplificadas:
- Cada fila de las tablas representa un objeto.
- Campos mapeados: id, nombre, tipo, subtipo, rareza, durabilidad (max/actual), efecto, descripcion, peso, valor, stackeable, stack_max, cantidad, favorito.
- Durabilidad se infiere de la columna y se deja null si no es numérica o infinita.
- Valor se extrae de la columna 'Valor' (número). Si no se puede extraer, se deja null.
- Tipo y subtipo se deducen por la sección del catálogo (p.ej. Herramientas -> herramienta, Exploración -> exploracion).
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import List, Optional, Dict


MD_PATH_DEFAULT = Path("docs/CATALOGO_OBJETOS.md")
OUTPUT_JSON = Path("backend/src/data/objetos.json")


def parse_value_cell(cell: str) -> Optional[int]:
    if not cell:
        return None
    m = re.search(r"(\d+)", cell.replace(".", ""))
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return None
    return None


def to_snake_case(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_")


def deduce_type_subtype(section_header: str, row_index_in_section: int) -> (str, str):
    # Basic mapping based on common sections
    sec = section_header.lower()
    if "herramientas" in sec:
        if "exploración" in sec:
            return "herramienta", "exploracion"
        if "recolección" in sec:
            return "herramienta", "recoleccion"
        if "supervivencia" in sec:
            return "herramienta", "supervivencia"
        return "herramienta", "general"
    if "consumibles" in sec:
        return "consumible", "utilidad"
    if "materiales" in sec:
        return "material", "general"
    if "misceláneos" in sec:
        return "miscelaneo", "general"
    if "objetos especiales" in sec:
        return "accesorio", "general"
    # Fallback
    return "item", "general"


def parse_markdown(md_text: str) -> List[Dict]:
    lines = md_text.splitlines()
    items: List[Dict] = []
    current_section = ""
    in_table = False
    header = []
    for i, line in enumerate(lines):
        # Track sections by headings like '## 1. Herramientas' or '### 1.1 Herramientas de Exploración'
        m_sec = re.match(r"^#{2,}\s*(.*)$", line)
        if m_sec:
            current_section = m_sec.group(1).strip()
            in_table = False
            header = []
            continue

        # Detect start of a table header line
        if line.strip().startswith("| ID | Nombre ") or line.strip().startswith(
            "|----|--------"
        ):
            in_table = True
            header = [h.strip() for h in line.strip().split("|") if h.strip()]
            continue

        if in_table:
            # A separator line after header
            if line.strip().startswith("|----|") or line.strip().startswith("|----|"):
                continue
            # Stop if empty or a new section starts
            if (
                line.strip().startswith("---")
                or line.strip().startswith("## ")
                or line.strip().startswith("### ")
            ):
                in_table = False
                continue
            # Parse a row line
            if line.strip().startswith("|"):
                cols = [c.strip() for c in line.strip().split("|") if c.strip() != ""]
                # Expect at least 7 columns
                if len(cols) >= 7:
                    raw_id = cols[0].strip("`")
                    nombre = cols[1]
                    rareza = cols[2]
                    durab = cols[3]
                    efecto = cols[4]
                    obtener = cols[5]
                    valor_col = cols[6]
                    dur_max = None
                    dur_actual = None
                    if durab.lower() not in ("infinita", "—", "-"):
                        # Try to extract a number of usos
                        meses = re.findall(r"(\d+)", durab)
                        if meses:
                            dur_max = int(meses[0])
                            dur_actual = dur_max
                    valor = parse_value_cell(valor_col)
                    # Determine type/subtype from section
                    t, st = deduce_type_subtype(current_section, len(items))
                    item = {
                        "id": raw_id,
                        "nombre": nombre,
                        "tipo": t,
                        "subtipo": st,
                        "rareza": rareza.lower() if rareza else None,
                        "durabilidad_max": dur_max,
                        "durabilidad_actual": dur_actual,
                        "efecto": efecto,
                        "descripcion": "",
                        "peso": None,
                        "valor": valor,
                        "stackeable": None,
                        "stack_max": None,
                        "cantidad": 1,
                        "favorito": False,
                    }
                    # Teoricamente los efectos son la descripcion
                    if not item.get("descripcion"):
                        item["descripcion"] = item.get("efecto", "")
                    # Normalizar: si ya hay una descripcion, vaciar el campo efecto
                    if item.get("descripcion"):
                        item["efecto"] = ""
                    items.append(item)
    return items


def main():
    md_path = Path(__file__).resolve().parents[3] / MD_PATH_DEFAULT
    if not md_path.exists():
        md_path = MD_PATH_DEFAULT
    if not md_path.exists():
        print(f"MD no encontrado: {md_path}")
        return
    text = md_path.read_text(encoding="utf-8")
    objs = parse_markdown(text)
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(objs, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Generado {len(objs)} objetos en {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
