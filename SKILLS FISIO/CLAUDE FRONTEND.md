# CLAUDE.md — Reglas de Frontend para el Sitio Web

## Hacer Siempre Primero
- **Invoca la skill `frontend-design`** antes de escribir cualquier código de frontend, en cada sesión, sin excepciones.

## Imágenes de Referencia
- Si se proporciona una imagen de referencia: iguala exactamente el layout, el espaciado, la tipografía y el color. Sustituye el contenido por contenido de relleno (imágenes vía `https://placehold.co/`, copy genérico). No mejores ni añadas nada al diseño.
- Si no hay imagen de referencia: diseña desde cero con alto nivel de cuidado (ver las guardrails más abajo).
- Haz una captura de tu resultado, compárala con la referencia, corrige las discrepancias y vuelve a capturar. Haz al menos 2 rondas de comparación. Detente solo cuando no queden diferencias visibles o cuando el usuario lo indique.

## Servidor Local
- **Sirve siempre en localhost** — nunca hagas una captura de una URL `file:///`.
- Inicia el servidor de desarrollo: `node serve.mjs` (sirve la raíz del proyecto en `http://localhost:3000`)
- `serve.mjs` está en la raíz del proyecto. Inícialo en segundo plano antes de hacer cualquier captura.
- Si el servidor ya está en marcha, no inicies una segunda instancia.

## Flujo de Trabajo de Capturas
- Puppeteer está instalado en `C:/Users/nateh/AppData/Local/Temp/puppeteer-test/`. La caché de Chrome está en `C:/Users/nateh/.cache/puppeteer/`.
- **Haz siempre la captura desde localhost:** `node screenshot.mjs http://localhost:3000`
- Las capturas se guardan automáticamente en `./temporary screenshots/screenshot-N.png` (numeración automática, nunca se sobrescriben).
- Sufijo de etiqueta opcional: `node screenshot.mjs http://localhost:3000 label` → se guarda como `screenshot-N-label.png`
- `screenshot.mjs` está en la raíz del proyecto. Úsalo tal cual.
- Después de hacer la captura, lee el PNG desde `temporary screenshots/` con la herramienta Read — Claude puede ver y analizar la imagen directamente.
- Al comparar, sé específico: "el encabezado tiene 32px pero la referencia muestra ~24px", "el espacio entre tarjetas es de 16px pero debería ser 24px"
- Revisa: espaciado/padding, tamaño de fuente/peso/altura de línea, colores (hex exacto), alineación, border-radius, sombras, dimensionado de imágenes

## Valores por Defecto de Salida
- Un único archivo `index.html`, todos los estilos en línea, salvo que el usuario indique lo contrario
- Tailwind CSS vía CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Imágenes de relleno: `https://placehold.co/ANCHOxALTO`
- Responsive mobile-first

## Recursos de Marca
- Comprueba siempre la carpeta `brand_assets/` antes de diseñar. Puede contener logos, guías de color, guías de estilo o imágenes.
- Si hay recursos ahí, úsalos. No uses contenido de relleno donde haya recursos reales disponibles.
- Si hay un logo presente, úsalo. Si hay una paleta de colores definida, usa esos valores exactos — no inventes colores de marca.

## Guardrails Anti-Genéricas
- **Colores:** Nunca uses la paleta por defecto de Tailwind (indigo-500, blue-600, etc.). Elige un color de marca personalizado y deriva a partir de él.
- **Sombras:** Nunca uses un `shadow-md` plano. Usa sombras por capas, teñidas de color, con opacidad baja.
- **Tipografía:** Nunca uses la misma fuente para encabezados y cuerpo de texto. Combina una fuente display/serif con una sans limpia. Aplica tracking ajustado (`-0.03em`) en encabezados grandes, altura de línea generosa (`1.7`) en el cuerpo.
- **Gradientes:** Superpón varios gradientes radiales. Añade grano/textura mediante un filtro de ruido SVG para dar profundidad.
- **Animaciones:** Anima únicamente `transform` y `opacity`. Nunca uses `transition-all`. Usa un easing estilo spring.
- **Estados interactivos:** Todo elemento clicable necesita estados hover, focus-visible y active. Sin excepciones.
- **Imágenes:** Añade una superposición de gradiente (`bg-gradient-to-t from-black/60`) y una capa de tratamiento de color con `mix-blend-multiply`.
- **Espaciado:** Usa tokens de espaciado intencionados y consistentes — no pasos aleatorios de Tailwind.
- **Profundidad:** Las superficies deben tener un sistema de capas (base → elevada → flotante), no estar todas en el mismo plano z.

## Reglas Estrictas
- No añadas secciones, funcionalidades o contenido que no estén en la referencia
- No "mejores" un diseño de referencia — iguálalo
- No te detengas tras una sola ronda de capturas
- No uses `transition-all`
- No uses el azul/indigo por defecto de Tailwind como color primario
