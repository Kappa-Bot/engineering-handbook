# Codex local — OpenDesign pilot seguro

Ejecuta esta adopción en el **Windows local del usuario**, sin Cloud Work, sin modificar repositorios de productos y sin cargos incrementales.

## Fuente y objetivo

- Fuente: `Kappa-Bot/engineering-handbook` `main` actualizado.
- Normativa: `playbooks/open-design-local-adoption.md`.
- Kit: `brands/melodiq-systems/open-design/`.
- Resultado: instalar/configurar OpenDesign en Windows de forma segura, importar el sistema corporativo como **copia derivada**, abrir/revisar el one-pager local y generar una muestra A4 de prueba con datos ficticios.

## Preflight

1. Confirma Windows, Codex local activo, `CODEX_HOME`, ruta del checkout del Handbook, modelo/auth existentes, backups y permisos.
2. Revisa `README.md`, `check.py`, manifest, `DESIGN.md`, `tokens.css` y demo. Ejecuta `python brands/melodiq-systems/open-design/check.py`.
3. Detecta instalaciones previas de OpenDesign; preserva proyectos, credenciales, configuración y modificaciones. Verifica última **release estable oficial** para Windows, firma/editor y SHA256 publicado antes de ejecutar el instalador. Usa solo la fuente oficial; si no puedes demostrar integridad, detén solo ese paso y reporta el bloqueo.
4. No descargues plugins, modelos ni proveedores adicionales. No habilites API billing, OpenDesign Cloud/AMR, créditos ni suscripciones.

## Privacidad y seguridad

5. Abre OpenDesign y desactiva **Anonymous metrics** y **Conversation and tool content** en Settings → Privacy; confirma el resultado. Ten presente que el canal de diagnóstico de seguridad puede seguir activo.
6. **No lances Codex desde OpenDesign en Windows/WSL**. El adaptador upstream puede usar `danger-full-access` y aprobaciones no interactivas. Conserva Codex normal, sus políticas y la instalación de Agency Agents. No cambies el sandbox ni configures una excepción global.
7. Para esta primera ejecución **NO instales `od mcp install codex`**. Puedes usar `od mcp install codex --print` para inspección, pero su servidor incluye tools de escritura y la allowlist de Codex debe verificarse antes de usar MCP con contenido sensible. Mantén intercambio por ficheros locales aislados.
8. Crea un proyecto de prueba en una carpeta nueva sin acceso innecesario a checkout de producto, credenciales ni clientes reales. No alteres git/worktrees de ChurchOS, JobOps o Platform Core.

## Piloto funcional

9. Usa el importador de carpeta de Design Systems para importar `.../open-design/system/` (no metas el directorio completo del Handbook). Confirma identidad, tokens, contraste y ausencia de logo inventado. Si el importador exige cambios, no cambies el ADN canónico; diagnostica su contrato.
10. Abre `.../open-design/demo/alcance-del-servicio.html` como archivo local o incorpora copia a un proyecto de diseño aislado. Verifica edición, reset, ausencia de peticiones de red/storage, foco teclado, móvil, A4 y print-to-PDF **de prueba**. Mantén BORRADOR · DEMO.
11. No intentes sustituir los modelos de propuesta existentes en Gmail ni utilices datos de clientes. No envíes, publiques, despliegues ni compartas este borrador.
12. Limpia únicamente temporales creados en esta ejecución cuando esté permitido y no haya trabajo único; respeta denegaciones de borrado.

## Cierre

Informa una sola vez: versión y procedencia de OpenDesign, configuración de privacidad, kit importado, chequeos PASS/FAIL/NOT_VERIFIED, exportación de prueba, posible restricción de permisos, ubicación de los proyectos de prueba y bloqueos exactos. Diferencia instalación de app, integración MCP y ejecución Codex; nunca declares que están verificadas si no ocurrió. Termina sin ampliar a otros productos.
