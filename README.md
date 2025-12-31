# Lucia Artist Tools - Addon para Blender

Este addon proporciona un conjunto de herramientas esenciales para artistas 3D, enfocadas en la limpieza de topología, modelado hard-surface y gestión rápida de escenas.

## Instalación

1. Descarga el archivo `addon_lucia_final.py` de este repositorio.
2. Abre Blender y ve a **Edit > Preferences > Add-ons**.
3. Pulsa **Install...** y selecciona el archivo descargado.
4. Activa la casilla del addon "Lucia Artist Tools".
5. Encontrarás el panel en la barra lateral de la Vista 3D (Tecla N) en la pestaña **Lucia Tools**.
6. **Atajo Rápido:** Pulsa `Shift + Q` para abrir el Pie Menu.

## Objetivos SMART (Operadores Implementados)

Siguiendo la metodología SMART, se han definido los siguientes objetivos para mejorar el flujo de trabajo del artista:

1.  **Gestión de Origen (Obligatorio):** Implementar un operador que permita mover el origen de cualquier objeto seleccionado al origen del mundo (0,0,0) en un solo clic, reduciendo el tiempo de preparación para exportación a motores de juego.
2.  **Aplanado de Malla:** Desarrollar tres operadores independientes (X, Y, Z) que alineen los vértices seleccionados en un eje global, permitiendo corregir imperfecciones en superficies planas (hard-surface) de manera instantánea (similar al Make Planar del 3ds Max).
3.  **Selección de Loops Avanzada:** Crear herramientas de selección para "Expandir" y "Contraer" loops paralelos (edge rings) paso a paso, emulando el comportamiento de software como 3ds Max para facilitar la selección de patrones complejos.
4.  **Corrección de Topología:** Programar un sistema de navegación que detecte, cuente y enfoque automáticamente (Focus) triángulos y N-Gons uno por uno, asegurando una malla 100% quads antes de la entrega final.
