---
name: excalidraw-diagram
description: Úsala cuando alguien pida dibujar un diagrama, hacer un diagrama en Excalidraw, o construir un diagrama editable. Opción por defecto para todas las peticiones de diagramas.
---

## Flujo de Trabajo

### Paso 1: Entender la petición
Antes de generar nada, asegúrate de saber:
- ¿Qué concepto o sistema están diagramando?
- ¿Cuáles son los componentes o secciones principales?
- ¿Cuál es el flujo o la relación entre ellos?

Si la petición es vaga (p. ej., "haz un diagrama de Docker"), haz 1-2 preguntas aclaratorias:
- ¿Qué aspecto específico? (arquitectura, redes, volúmenes, etc.)
- ¿Qué nivel de detalle? (visión general de alto nivel vs. detalles internos)

### Paso 2: Investigar si es necesario
Si no estás seguro de la precisión técnica del concepto, investígalo antes de diagramar. Verifica:
- Nombres correctos de los componentes y sus relaciones
- Jerarquía y anidamiento adecuados
- Dirección precisa del flujo de datos

### Paso 3: Planificar el layout
Antes de escribir cualquier JSON, esboza el layout mentalmente:
- ¿Cuáles son las secciones principales? (de izquierda a derecha o de arriba a abajo)
- ¿Qué está anidado dentro de qué?
- ¿Qué flechas conectan qué?

Anota el plan de secciones:
```
[Sección A: w=170] --hueco 40px-- [Sección B: w=170] --hueco 40px-- [Sección C: w=640]
```

### Paso 4: Generar los elementos
Construye los elementos en este orden:
1. Primero las cajas/contenedores exteriores
2. Texto de encabezado de sección
3. Elementos anidados (de arriba a abajo dentro de cada sección)
4. Flechas y etiquetas de flechas al final

### Paso 5: Guardar y entregar
1. Guarda como `[concepto-slug].excalidraw` en el directorio actual
2. Muestra el JSON completo en un bloque de código para que el usuario pueda copiarlo directamente
3. Describe brevemente qué muestra el diagrama y qué representa cada zona de color
4. Indica al usuario cómo usar el archivo:

> **Cómo ver y editar tu diagrama:**
> - Ve a excalidraw.com (gratis, sin necesidad de cuenta)
> - Opción A: Haz clic en el menú (icono de hamburguesa arriba a la izquierda) > "Open" > selecciona el archivo `.excalidraw`
> - Opción B: Copia el bloque de código JSON de arriba, abre excalidraw.com, y pégalo con Ctrl+V / Cmd+V
> - Todos los elementos son totalmente editables -- arrastra para mover, usa los tiradores para redimensionar, doble clic para editar el texto

### Paso 6: Gestionar el feedback
Si el usuario pide cambios:
- Mover un elemento = actualiza x/y en ese elemento + todos los elementos que dependen de él
- Cambiar texto = actualiza tanto el campo `text` como `originalText`
- Añadir una zona = asígnale un nuevo color de la paleta, mantén el espaciado consistente
- Si un diagrama se vuelve complejo (20+ elementos), constrúyelo sección por sección para evitar errores de coordenadas

---

## Regla Crítica: Contraste de Texto

El texto dentro de formas coloreadas debe ser legible. Usa `#1e1e1e` (casi negro) o `#343a40` (gris carbón oscuro) para todo el texto dentro de formas rellenas. Nunca uses el color de trazo (stroke) de la zona para el texto que está sobre el fondo de esa zona (p. ej., texto amarillo sobre una tarjeta amarilla es ilegible). Reserva el `strokeColor` de la zona únicamente para los bordes de las formas y las flechas.

---

## Principios de Diseño

**El color cuenta la historia:** Un color por zona lógica. Todo lo que esté en la zona de "entrada" es azul. Todo lo que esté en la zona de "salida" es verde. Quien lo mire debería entender la estructura antes de leer una palabra.

**El anidamiento muestra contención:** Si X vive dentro de Y, la caja de X se dibuja dentro de la caja de Y con un padding consistente. Las coordenadas son absolutas, no relativas: `child_x = parent_x + padding`.

**Las etiquetas son cortas:** 2-5 palabras por etiqueta. Las explicaciones más largas se convierten en anotaciones con un `fontSize` menor y color apagado (`#868e96`).

**El espacio en blanco es estructura:** Hueco mínimo de 15px entre elementos hermanos. Mínimo de 40px entre secciones principales.

**Las flechas transmiten intención:** Colorea las flechas según su propósito. Etiqueta toda flecha que no sea obvia.

---

## Sistema de Layout

Planifica siempre las coordenadas antes de escribir el JSON.

1. Identifica las secciones principales (de izquierda a derecha o de arriba a abajo)
2. Asigna un ancho fijo y una x inicial a cada sección
3. Calcula los huecos: 40-60px entre secciones principales, 15-25px entre elementos hermanos
4. Trabaja de arriba a abajo dentro de cada sección: `next_y = current_y + current_height + gap`

**Reglas de padding:**
- De la caja exterior a la etiqueta interior: desplazamiento superior de 8-10px
- De la caja exterior a la caja anidada: desplazamiento de 10-15px en todos los lados
- Elementos hermanos: hueco de 10-15px

**Truco del ancho de texto:** Fija el ancho del texto igual al ancho de la caja padre. El texto se centra automáticamente cuando `textAlign: "center"`.

**Etiquetas de flechas:** Colócalas como elementos de texto separados, 20-25px por encima del punto medio y de la flecha, con el ancho y la x coincidiendo con los de la flecha.

**Ejemplo de matemática de coordenadas:**
```
Sección A: x=30,  w=170  -> borde derecho = 200
Hueco:                      40px
Sección B: x=240, w=170  -> borde derecho = 410
Hueco:                      40px
Sección C: x=450, w=600  -> borde derecho = 1050
```

---

## Sistema de Color

| Zona | Úsala para | strokeColor | backgroundColor |
|------|---------|-------------|-----------------|
| Azul | Entrada, origen, servicios externos | `#1971c2` | `#e7f5ff` |
| Amarillo | Procesamiento, transformación | `#f59f00` | `#fff9db` |
| Verde | Salida, contenedores, éxito | `#2f9e44` | `#d3f9d8` |
| Morado | Capas compartidas, infraestructura | `#862e9c` | `#f3d9fa` |
| Rojo | SO anfitrión, avisos, errores | `#c92a2a` | `#ffe3e3` |
| Gris | Hardware, contenedores neutros | `#495057` | `#f8f9fa` |

Para elementos anidados, varía la intensidad del relleno:
- Exterior: más claro (p. ej., `#d3f9d8`)
- Interior: medio (p. ej., `#8ce99a`)
- Interior profundo: claro-medio (p. ej., `#b2f2bb`)

---

## Escala Tipográfica

| Rol | fontSize | fontFamily |
|------|----------|------------|
| Título del diagrama | 32-36 | 1 (Virgil) |
| Encabezado de sección | 20-24 | 1 |
| Etiqueta de elemento | 16-18 | 1 |
| Anotación | 14-15 | 1 |
| Nota pequeña | 12-13 | 1 |
| Etiqueta de código | 14-16 | 3 (Cascadia) |

Ancho del texto = ancho de la caja padre. Desplazamiento x/y del texto ~8-10px respecto a la x/y de la caja, para el padding.

---

## Esquema de Elementos

Todo elemento necesita estos campos base. No omitas ninguno.

### Campos base (todos los tipos)
```json
{
  "id": "unique-string",
  "type": "rectangle|ellipse|diamond|arrow|line|text|freedraw",
  "x": 0, "y": 0,
  "width": 100, "height": 50,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "boundElements": [],
  "updated": 1,
  "link": null,
  "locked": false
}
```

### Campos de texto (añadir a los base)
```json
{
  "text": "Label text",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "top",
  "containerId": null,
  "originalText": "Label text",
  "lineHeight": 1.25
}
```

### Campos de flecha (añadir a los base)
```json
{
  "points": [[0, 0], [100, 0]],
  "lastCommittedPoint": null,
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

### Valores clave
- **fontFamily:** 1 = Virgil (manuscrita, por defecto), 2 = Helvetica, 3 = Cascadia (monoespaciada)
- **roughness:** 0 = suave, 1 = ligeramente rugoso (aspecto por defecto de Excalidraw), 2 = muy rugoso
- **fillStyle:** `"solid"` para diagramas limpios, `"hachure"` para el sombreado clásico de Excalidraw
- **roundness:** `null` = esquinas afiladas, `{"type": 3}` = rectángulos redondeados, `{"type": 2}` = flechas curvas
- **strokeStyle:** `"solid"`, `"dashed"` (conexiones opcionales), `"dotted"`

---

## Patrones Comunes

### Caja con etiqueta
```
[Rect: x, y, w, h]
[Título texto: x, y+10, w, fontSize=18]
[Subtítulo: x, y+38, w, fontSize=14, strokeColor=#868e96]
```

### Contenedor anidado
```
[Rect anfitrión: x=0, y=0, w=640, h=500]
[Etiqueta anfitrión: x=0, y=10, w=640]
[Elemento 1: x=15, y=50, w=190, h=200]
[Elemento 2: x=225, y=50, w=190, h=200]
[Elemento 3: x=435, y=50, w=190, h=200]
```

### Flecha con etiqueta
```
[Flecha: x=start_x, y=mid_y, width=gap_width, points=[[0,0],[gap_width,0]]]
[Etiqueta: x=start_x, y=mid_y-25, width=gap_width, textAlign=center]
```

---

## Envoltorio JSON

Todo diagrama usa esta estructura:
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ... ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```
