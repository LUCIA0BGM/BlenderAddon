# Lucia Artist Tools - Addon para Blender

Herramientas esenciales para artistas 3D: limpieza de topología, modelado hard-surface y gestión de materiales.

## Instalación

1. Descarga el archivo `.py` de este repositorio.
2. En Blender: **Edit > Preferences > Add-ons > Install...**
3. Activa: **Lucia Artist Tools**.
4. **Ubicación:** Panel lateral (Tecla N) > Pestaña **Lucia Tools**.
5. **Atajo:** `Shift + Q` (Pie Menu).

---

## Objetivos SMART (Operadores)

1. **Gestión de Origen:** Implementar un operador que permita mover el origen de cualquier objeto seleccionado al origen del mundo (0,0,0) en un solo clic.
2. **Aplanado de Malla:** Desarrollar tres operadores independientes (X, Y, Z) que alineen los vértices seleccionados en un eje global (similar al Make Planar de 3ds Max).
3. **Selección de Loops Avanzada:** Crear herramientas para "Expandir" y "Contraer" loops paralelos paso a paso, facilitando la selección de patrones complejos.
4. **Corrección de Topología:** Programar un sistema de navegación que detecte, cuente y enfoque automáticamente (Focus) triángulos y N-Gons uno por uno.
5. **Gestión de Materiales:** Implementar un operador de transferencia de materiales mediante un **selector de fuente (cuentagotas)**. Esto permite elegir un objeto "origen" en el panel y copiar su material a toda la selección actual, evitando errores de selección activa.
