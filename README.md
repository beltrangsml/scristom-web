# Rediseño web · Parroquia Santo Cristo de la Misericordia

Propuesta de rediseño de scristom.es. **No es la web oficial**: el contenido y las fotos son de la parroquia.

## Ver en local
Doble clic en `VER-WEB.bat`, o `py -m http.server 8765 -d docs` y abrir http://localhost:8765.

## Editar
- Horarios, grupos, agenda, campamentos y contacto: `src/datos.py`.
- Avisos: `src/data/avisos.json`. Estilos: `src/estilos.css`. Páginas: `src/build.py`.
- Regenerar: `py -X utf8 src/build.py` (salida en `docs/`).
- `src/importar.py` vuelve a traer avisos y fotos de la web actual (requiere Pillow).

## Qué incluye
Inicio con próxima misa (hora de Madrid) y tiempo litúrgico, horarios, sacramentos, grupos con filtro, agenda con
exportación a calendario, 109 avisos con buscador, parroquia y galería, colabora, Cáritas, campamentos 2027,
contacto, letra grande y barra de accesos en móvil. Sin cookies ni rastreadores.

## Antes de publicar como web oficial
- Confirmar los horarios (ver `PROPUESTA.md`).
- La suscripción, su modificación y el curso de monitor enlazan a los formularios de la web actual. Si se sustituye,
  hay que recrearlos (con RGPD) y revisar privacidad y cookies con la parroquia.
- Carteles, PDF y fotos son de la parroquia o de bancos de imágenes que usa: confirmar derechos.
- Los PDF y algunos formularios siguen alojados en la web actual: moverlos antes de apagarla.
- Quitar la frase «Propuesta de rediseño» del pie (`src/build.py`).
- Hoy los avisos se añaden editando datos. Para que secretaría publique sola hace falta un gestor
  (tema de WordPress o CMS): segunda fase.
- GitHub Pages (Settings → Pages → rama `main`, carpeta `/docs`) publica la web a la vista de todos.
