# Experiments - Playground

Esta carpeta contiene experimentos y prototipos de nuevos sistemas antes de integrarlos al backend principal.

## Propósito

- Probar nuevas ideas sin arriesgar el código funcional
- Prototipar sistemas complejos (NPCs, Relaciones, LLM, etc.)
- Validar arquitecturas antes de implementar

## Estructura

```
experiments/
├── README.md           # Este archivo
├── mapa/               # Experimentos del sistema de mapa
├── tiempo/             # Experimentos del sistema de tiempo
├── npcs/               # Experimentos del sistema de NPCs
├── relaciones/         # Experimentos del sistema de relaciones
├── llm/                # Experimentos de integración con LLM
└── utils/              # Utilidades compartidas
```

## Cómo usar

1. Crear una subcarpeta para el sistema que quieres experimentar
2. Implementar el prototipo con tests
3. Validar que funciona correctamente
4. Mover al backend principal cuando esté listo

## Reglas

- NO importar desde `backend/src` directamente
- Cada experimento debe ser autocontenido
- Incluir tests de validación
- Documentar decisiones de diseño