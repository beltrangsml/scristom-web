"""Genera la web estática en docs/.   py -X utf8 src/build.py"""
import datetime as dt
import html
import json
import re
from pathlib import Path

import datos as D

RAIZ = Path(__file__).resolve().parents[1]
SRC, OUT = RAIZ / "src", RAIZ / "docs"
P = D.PARROQUIA
AVISOS = json.loads((SRC / "data" / "avisos.json").read_text(encoding="utf-8"))
FOTOS = json.loads((SRC / "data" / "fotos.json").read_text(encoding="utf-8"))
MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()
HOY = dt.date.today().isoformat()
CAIDOS = json.loads((SRC / "data" / "enlaces_caidos.json").read_text(encoding="utf-8"))  # ya no responden en origen
e = lambda s: html.escape(str(s), quote=True)

NAV = [("horarios", "Horarios"), ("sacramentos", "Sacramentos"), ("grupos", "Grupos"),
       ("avisos", "Avisos"), ("parroquia", "La parroquia"), ("contacto", "Contacto")]

ICONOS = {
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "fuera": '<path d="M7 17 17 7M8 7h9v9"/>',
    "tel": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mapa": '<path d="M12 21s-7-5.7-7-11.5a7 7 0 0 1 14 0C19 15.3 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "reloj": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "corazon": '<path d="M12 20S3 14.5 3 8.8A4.8 4.8 0 0 1 12 6.5a4.8 4.8 0 0 1 9 2.3C21 14.5 12 20 12 20Z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def ico(n):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICONOS[n]}</svg>'


def fecha(iso, anio=True):
    a, m, d = map(int, iso.split("-"))
    return f"{d} de {MESES[m - 1]}" + (f" de {a}" if anio else "")


def img(ref, alt, r, sizes="100vw", clase="", prioridad=False):
    f = FOTOS[ref] if isinstance(ref, str) else ref
    base = f"{r}assets/img/{f['nombre']}"
    srcset = ", ".join(f"{base}-{w}.webp {w}w" for w in f["anchos"])
    carga = 'fetchpriority="high"' if prioridad else 'loading="lazy" decoding="async"'
    return (f'<img class="{clase}" src="{base}-{f["anchos"][min(1, len(f["anchos"]) - 1)]}.webp" srcset="{srcset}" '
            f'sizes="{sizes}" width="{f["w"]}" height="{f["h"]}" alt="{e(alt)}" {carga}>')


def enlace(texto, url, r, clase="mas"):
    fuera = url.startswith("http")
    destino = url if re.match(r"^(https?:|mailto:|tel:|#)", url) else r + url
    return (f'<a class="{clase}" href="{e(destino)}"{" rel=noopener target=_blank" if fuera else ""}>{e(texto)}'
            f'{ico("fuera" if fuera else "flecha")}</a>')


def jsonld():
    return json.dumps({
        "@context": "https://schema.org", "@type": "CatholicChurch", "name": P["nombre"], "telephone": P["tel"],
        "email": P["email"], "url": D.ORIGEN,
        "address": {"@type": "PostalAddress", "streetAddress": P["calle"], "postalCode": P["cp"],
                    "addressLocality": P["ciudad"], "addressRegion": P["provincia"], "addressCountry": "ES"},
    }, ensure_ascii=False)


def pagina(ruta, titulo, desc, cuerpo, activa="", extra_head="", portada=False):
    r = "../" * ruta.count("/")
    if ruta == "404.html":
        r = ""
    nav = "".join(f'<li><a href="{r}{k}.html"{" aria-current=page" if k == activa else ""}>{t}</a></li>' for k, t in NAV)
    titulo_full = titulo if portada else f"{titulo} · Santo Cristo de la Misericordia"
    doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo_full)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#172a54">
<meta property="og:type" content="website"><meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(titulo_full)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{r}assets/img/og.jpg">
<link rel="icon" href="{r}assets/img/icono-48.png"><link rel="apple-touch-icon" href="{r}assets/img/icono-180.png">
<link rel="preload" href="{r}assets/fonts/marcellus.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/sourcesans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/estilos.css">
<script>try{{if(localStorage.getItem('letra')==='grande')document.documentElement.classList.add('grande')}}catch(e){{}}</script>
<script type="application/ld+json">{jsonld()}</script>{extra_head}
</head>
<body>
<a class="saltar" href="#contenido">Ir al contenido</a>
<header class="cab">
  <div class="ancho cab-in">
    <a class="marca" href="{r}index.html"><img src="{r}assets/img/logo-112.webp" width="56" height="56" alt="">
      <span><strong>Santo Cristo de la Misericordia</strong><small>Parroquia · Boadilla del Monte</small></span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{ico("menu")}<span>Menú</span></button>
    <nav id="menu" aria-label="Principal"><ul>{nav}</ul>
      <div class="nav-extra"><button class="letra" type="button" aria-pressed="false" title="Aumentar el tamaño de la letra">A<b>A</b><span class="solo">Letra grande</span></button>
      <a class="btn btn-rojo" href="{r}colabora.html">Donar</a></div></nav>
  </div>
</header>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie">
  <div class="ancho pie-in">
    <div><img src="{r}assets/img/logo-112.webp" width="72" height="72" alt="" class="pie-logo" loading="lazy">
      <p class="pie-nombre">{P["nombre"]}</p><p>Diócesis de Getafe</p></div>
    <div><h2>Dónde estamos</h2><p>{P["calle"]}<br>{P["cp"]} {P["ciudad"]}, {P["provincia"]}</p>
      <p>{enlace("Cómo llegar", P["mapa"], r)}</p></div>
    <div><h2>Secretaría</h2><p><a href="tel:{P["tel"]}">{P["telefono"]}</a><br><a href="mailto:{P["email"]}">{P["email"]}</a></p>
      <p>Lunes a viernes, de 17:00 a 19:00.<br>Cerrada festivos, julio y agosto.</p></div>
    <div><h2>Síguenos</h2><ul class="lista-pie">
      <li><a href="{P["whatsapp"]}" rel="noopener" target="_blank">Avisos por WhatsApp</a></li>
      <li><a href="{P["youtube"]}" rel="noopener" target="_blank">YouTube</a></li>
      <li><a href="{P["spotify"]}" rel="noopener" target="_blank">Spotify</a></li>
      <li><a href="{P["ivoox"]}" rel="noopener" target="_blank">iVoox</a></li></ul></div>
  </div>
  <div class="ancho pie-legal"><span>Propuesta de rediseño. No es la web oficial: <a href="{D.ORIGEN}/" rel="noopener">scristom.es</a>.</span>
    <span><a href="{r}privacidad.html">Privacidad</a> · <a href="{r}cookies.html">Cookies</a></span></div>
</footer>
<nav class="barra" aria-label="Accesos rápidos">
  <a href="{r}horarios.html">{ico("reloj")}Misas</a><a href="tel:{P["tel"]}">{ico("tel")}Llamar</a>
  <a href="{P["mapa"]}" rel="noopener" target="_blank">{ico("mapa")}Llegar</a><a href="{r}colabora.html">{ico("corazon")}Donar</a>
</nav>
<script src="{r}assets/app.js" defer></script>
</body>
</html>
"""
    destino = OUT / ruta
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(doc, encoding="utf-8")


def cabecera(titulo, entrada, foto, r="", alt=""):
    return f"""<section class="titulo">
  <div class="ancho titulo-in"><div><h1>{e(titulo)}</h1><p>{e(entrada)}</p></div>
  <figure>{img(foto, alt, r, "(min-width: 860px) 46vw, 100vw", prioridad=True)}</figure></div>
</section>"""


def tabla_misas():
    grupos = [("Lunes a viernes", 1), ("Sábados", 6), ("Domingos y festivos", 0)]
    cols = []
    for nombre, dia in grupos:
        filas = ""
        for m in D.MISAS:
            if dia not in m["dias"]:
                continue
            marcas = [m.get("nota", "")]
            if m["lugar"] == D.MONASTERIO:
                marcas.append("Monasterio")
            if m.get("verano") is False:
                marcas.append("no en verano")
            detalle = " · ".join(x for x in marcas if x)
            filas += f'<li><time>{m["hora"].lstrip("0")}</time><span>{e(detalle)}</span></li>'
        cols.append(f'<div class="dia" data-dia="{dia}"><h3>{nombre}</h3><ul>{filas}</ul></div>')
    return f"""<div class="misas">{"".join(cols)}</div>
<p class="nota">Del 1 de julio al 7 de septiembre se suprimen las misas marcadas «no en verano». El monasterio es el del Santísimo Sacramento.
En Navidad, Semana Santa y otras fechas el horario puede cambiar: consulta los avisos.</p>"""


def tarjeta_aviso(a, r="", nivel="h3"):
    foto = img(a["portada"], "", r, "(min-width: 900px) 30vw, 100vw") if a["portada"] else \
        f'<span class="sin-foto"><img src="{r}assets/img/logo-112.webp" width="112" height="112" alt="" loading="lazy"></span>'
    return f"""<li class="aviso" data-cat="{e(a['categoria'])}" data-t="{e(a['titulo'].lower())}">
<a href="{r}avisos/{a['slug']}.html"><span class="aviso-foto">{foto}</span>
<span class="aviso-meta"><time datetime="{a['fecha']}">{fecha(a['fecha'])}</time> · {e(a['categoria'])}</span>
<{nivel}>{e(a['titulo'])}</{nivel}></a></li>"""


def agenda(limite, r=""):
    filas = ""
    for ini, fin, titulo, gid in D.AGENDA:
        if fin < HOY:
            continue
        a1, m1, d1 = map(int, ini.split("-"))
        _, m2, d2 = map(int, fin.split("-"))
        rango = f"Del {d1} al {d2} de {MESES[m2 - 1]}" if m1 == m2 else f"Del {d1} de {MESES[m1 - 1]} al {d2} de {MESES[m2 - 1]}"
        mas = f'<a href="{r}grupos.html#{gid}">Información<span class="solo"> sobre {e(titulo)}</span></a>' if gid else \
              (f'<a href="{r}campamentos.html">Información<span class="solo"> sobre {e(titulo)}</span></a>' if "Campamento" in titulo or "Loyola" in titulo else "")
        filas += f"""<li data-ini="{ini}" data-fin="{fin}"><span class="fecha" aria-hidden="true"><b>{d1}</b>{MESES[m1 - 1][:3]}</span>
<div><h3>{e(titulo)}</h3><p>{rango} de {a1}</p></div><div class="acc">{mas}<button type="button" class="ics" data-titulo="{e(titulo)}">Añadir al calendario<span class="solo">: {e(titulo)}</span></button></div></li>"""
    return f'<ul class="agenda" data-limite="{limite}">{filas}</ul>'


# ---------------------------------------------------------------- páginas
def inicio():
    r = ""
    quiero = [
        ("Bautizar a mi hijo", "Charlas previas y solicitud en secretaría", "sacramentos.html#bautismo"),
        ("Apuntar a catequesis", "Comunión, LifeTeen y Light Up", "grupos.html#iniciacion"),
        ("Confesarme", "Media hora antes de cada misa", "sacramentos.html#confesion"),
        ("Casarme", "Cursillos prematrimoniales y novios", "sacramentos.html#matrimonio"),
        ("Comunión en casa", "Para enfermos y personas impedidas", "sacramentos.html#enfermos"),
        ("Pedir ayuda", "Cáritas parroquial", "caritas.html"),
        ("Hacer un retiro", "Emaús, Effetá, Bartimeo y más", "grupos.html"),
        ("Echar una mano", "Catequista, voluntario o donante", "colabora.html"),
    ]
    q = "".join(f'<li><a href="{u}"><span><strong>{t}</strong><small>{s}</small></span>{ico("flecha")}</a></li>' for t, s, u in quiero)
    cuerpo = f"""
<section class="heroe">
  {img("retablo", "El retablo y el Cristo del templo durante una celebración, con los fieles en los bancos", r, "100vw", "heroe-foto", True)}
  <div class="ancho heroe-in">
    <div class="heroe-texto"><p class="tiempo" id="tiempo">Diócesis de Getafe</p>
      <h1>Una casa abierta en Boadilla del Monte</h1>
      <p>Parroquia Santo Cristo de la Misericordia. Misa todos los días, adoración, catequesis y comunidad para cada edad.</p>
      <p class="botones"><a class="btn btn-claro" href="horarios.html">Todos los horarios</a><a class="btn btn-linea" href="{P["mapa"]}" rel="noopener" target="_blank">Cómo llegar</a></p></div>
    <aside class="proxima" aria-live="polite">
      <h2>Próxima misa</h2>
      <p class="prox-hora" id="prox-hora">20:30</p>
      <p class="prox-dia" id="prox-dia">Consulta el horario completo</p>
      <p class="prox-falta" id="prox-falta"></p>
      <ol id="prox-lista" aria-label="Siguientes misas"></ol>
    </aside>
  </div>
</section>

<section class="seccion"><div class="ancho dos">
  <div class="intro"><h2>¿Qué necesitas?</h2><p>Lo más habitual, a un toque. Si no lo encuentras, llama a secretaría al <a href="tel:{P["tel"]}">{P["telefono"]}</a>, de lunes a viernes de 17:00 a 19:00.</p></div>
  <ul class="quiero">{q}</ul>
</div></section>

<section class="seccion piedra" aria-labelledby="h-misas"><div class="ancho">
  <div class="sec-cab"><h2 id="h-misas">Horarios de misa</h2>{enlace("Confesiones, rosario y adoración", "horarios.html", r)}</div>
  {tabla_misas()}
</div></section>

<section class="seccion"><div class="ancho">
  <div class="sec-cab"><h2>Avisos de la parroquia</h2>{enlace("Todos los avisos", "avisos.html", r)}</div>
  <ul class="avisos destacados">{"".join(tarjeta_aviso(a) for a in AVISOS[:3])}</ul>
  <p class="whats"><span>Recibe los avisos en el móvil.</span>{enlace("Unirme a la lista de WhatsApp", P["whatsapp"], r, "btn btn-petroleo")}</p>
</div></section>

<section class="seccion noche"><div class="ancho dos">
  <div class="intro"><h2>Próximas fechas</h2><p>Retiros, cursillos y campamentos. Las fechas pasadas desaparecen solas.</p>
    <figure class="intro-foto">{img("custodia", "Custodia con el Santísimo expuesto", r, "(min-width: 860px) 32vw, 100vw")}</figure></div>
  {agenda(5)}
</div></section>

<section class="seccion"><div class="ancho">
  <div class="sec-cab"><h2>Una comunidad para cada edad</h2>{enlace("Ver todos los grupos", "grupos.html", r)}</div>
  <div class="edades">
    <a href="grupos.html#ninos">{img("san-cristobal", "", r, "(min-width: 760px) 32vw, 100vw")}<h3>Niños</h3><p>Iniciación Cristiana y Grupo Lázaro.</p></a>
    <a href="grupos.html#jovenes">{img("jovenes", "", r, "(min-width: 760px) 32vw, 100vw")}<h3>Jóvenes</h3><p>LifeTeen, Light Up, Bartimeo, Effetá y Nicodemo.</p></a>
    <a href="grupos.html#adultos">{img("mision", "", r, "(min-width: 760px) 32vw, 100vw")}<h3>Adultos y familias</h3><p>Emaús, Acción Católica, matrimonios, novios y Cáritas.</p></a>
  </div>
  <a class="banda" href="campamentos.html">{img("montana", "", r, "(min-width: 760px) 40vw, 100vw")}<span><strong>Campamentos 2027</strong><span>San Martín de Don y Loyola, del 20 de junio al 19 de julio. Requisitos y fechas para monitores.</span></span>{ico("flecha")}</a>
</div></section>

<section class="seccion pergamino"><div class="ancho dos donar">
  <figure>{img("comunion", "Un sacerdote entrega la comunión en la mano", r, "(min-width: 860px) 45vw, 100vw")}</figure>
  <div><h2>Sostén tu parroquia</h2>
    <p>La parroquia cubre sus propias necesidades y, por su vocación misionera, ayuda a otras personas y realidades.</p>
    {datos_donativo()}
    <p class="botones"><a class="btn btn-rojo" href="colabora.html">Formas de colaborar</a></p></div>
</div></section>

<section class="seccion"><div class="ancho tres">
  <div><h2>Reza con nosotros</h2><p>La meditación del día y las charlas, donde las escuches.</p><ul class="enlaces">
    <li>{enlace("Meditaciones en YouTube", P["youtube"], r)}</li><li>{enlace("Meditación en Spotify", P["spotify"], r)}</li><li>{enlace("Charlas de Acción Católica", P["ivoox"], r)}</li></ul></div>
  <div><h2>Seminario</h2><p>En el seminario de Getafe hay 5 chicos de la parroquia. Acompáñalos con tu oración.</p><ul class="enlaces"><li>{enlace("Web del seminario", "https://www.seminariodegetafe.es/", r)}</li></ul></div>
  <div><h2>Columbarios</h2><p>Un lugar de descanso en el patio de la Virgen María, junto a la comunidad que reza.</p><ul class="enlaces"><li>{enlace("Folleto de los columbarios (PDF)", D.FOLLETO_COLUMBARIOS, r)}</li></ul></div>
</div></section>
"""
    pagina("index.html", f"{P['nombre']} · Boadilla del Monte",
           "Horarios de misa, sacramentos, catequesis, grupos y avisos de la parroquia Santo Cristo de la Misericordia, en Boadilla del Monte (Madrid).",
           cuerpo, portada=True,
           extra_head=f'\n<script type="application/json" id="misas">{json.dumps({"misas": D.MISAS, "festivos": D.FESTIVOS, "extras": D.EXTRAS}, ensure_ascii=False)}</script>')


def datos_donativo(caritas=False):
    iban = P["iban_caritas"] if caritas else P["iban"]
    concepto = " (concepto «cáritas»)" if caritas else ""
    return f"""<dl class="cuenta">
<div><dt>Transferencia</dt><dd><span class="num">{iban}</span><button type="button" class="copiar" data-copiar="{iban.replace(" ", "")}">Copiar<span class="solo"> IBAN</span></button></dd></div>
<div><dt>Bizum{concepto}</dt><dd><span class="num">{P["bizum"]}</span><button type="button" class="copiar" data-copiar="{P["bizum"]}">Copiar<span class="solo"> código Bizum</span></button></dd></div>
</dl>"""


def horarios():
    oracion = "".join(f"<div><dt>{e(t)}</dt><dd>{e(x)}</dd></div>" for t, x in D.ORACION)
    semana = "".join(f'<tr><th scope="row">{e(t)}</th><td>{e(x)}</td></tr>' for t, x in D.SEMANA)
    cuerpo = cabecera("Horarios", "Misas, confesiones, oración y actividades de la semana.", "campana", alt="Campana de bronce junto a una puerta del templo") + f"""
<section class="seccion"><div class="ancho"><h2>Misas</h2>{tabla_misas()}
<p class="nota">1 de enero: misa de Año Nuevo a la 1:30. 25 de diciembre: misa del Gallo a las 0:00.</p></div></section>
<section class="seccion piedra"><div class="ancho dos"><div class="intro"><h2>Confesión y oración</h2><p>El horario puede cambiar en verano, Navidad y Semana Santa.</p>
<figure class="intro-foto">{img("adoracion", "Una persona reza de rodillas ante el Santísimo", "", "(min-width: 860px) 32vw, 100vw")}</figure></div>
<dl class="filas">{oracion}</dl></div></section>
<section class="seccion"><div class="ancho"><h2>La semana en la parroquia</h2><table class="tabla"><tbody>{semana}</tbody></table>
<p class="nota">Secretaría: de lunes a viernes, de 17:00 a 19:00. Cerrada festivos y del 1 de julio al 31 de agosto.</p></div></section>"""
    pagina("horarios.html", "Horarios de misa y confesiones",
           "Horarios de misas, confesiones, rosario, adoración y catequesis en la parroquia Santo Cristo de la Misericordia de Boadilla del Monte.", cuerpo, "horarios")


def sacramentos():
    t, r = P["tel"], ""
    S = [
        ("bautismo", "Bautismo", f"""<p>Antes del bautizo, padre y madre asisten a la charla bautismal, que es obligatoria salvo causa grave.</p>
<ol class="pasos"><li>Apúntate en secretaría con antelación, con el nombre de los padres y del niño y un teléfono.</li><li>Recoge allí la «Solicitud de Bautismo», cumpliméntala y entrégala en persona antes de la charla.</li><li>Asistid a la charla: dos viernes al mes, de 19:00 a 20:00.</li></ol>
<p>{enlace("Llamar a secretaría", "tel:" + t, r)}</p>"""),
        ("comunion", "Primera comunión y catequesis", f"""<p>La Iniciación Cristiana dura tres años, de septiembre a junio. En el segundo reciben la Confesión y la Confirmación; en el tercero, la Eucaristía.</p>
<p>También hay Oratorio para niños de 5 a 7 años.</p><p>{enlace("Horarios y contacto de catequesis", "grupos.html#iniciacion", r)}</p>"""),
        ("confirmacion", "Confirmación de adultos", f"""<p>Catequesis los jueves, de 21:00 a 22:00. Pregunta en secretaría para incorporarte.</p><p>{enlace("Escribir a la parroquia", "mailto:" + P["email"], r)}</p>"""),
        ("confesion", "Confesión", "<p>Media hora antes de las misas, o siempre que estén los sacerdotes en la parroquia.</p>"),
        ("matrimonio", "Matrimonio", f"""<p>Los cursillos prematrimoniales se hacen en un fin de semana, con familias y el párroco, en formato de charla-coloquio.</p>
<p>Próximos: 5–7 de febrero, 9–11 de abril y 4–6 de junio de 2027.</p>
<p>{enlace("Información de los cursillos (PDF)", D.FOLLETO_CURSILLOS, r)} {enlace("Escribir al equipo de novios", "mailto:novioscristom@gmail.com", r)}</p>"""),
        ("enfermos", "Comunión en casa", f"""<p>Si tú o un familiar estáis enfermos o impedidos y necesitáis recibir la comunión en casa, llámanos.</p>
<p><a class="btn btn-rojo" href="tel:{P["enfermos_tel"]}">Llamar al {P["enfermos"]}</a></p>"""),
        ("columbarios", "Columbarios", f"""<p>Columbarios en el patio de la Virgen María.</p>{img("columbarios", "Columbarios de piedra junto a una imagen de la Virgen en el patio", r, "(min-width: 860px) 55vw, 100vw")}
<p>{enlace("Folleto informativo (PDF)", D.FOLLETO_COLUMBARIOS, r)}</p>"""),
    ]
    indice = "".join(f'<li><a href="#{i}">{n}</a></li>' for i, n, _ in S)
    bloques = "".join(f'<section class="bloque" id="{i}"><h2>{n}</h2>{c}</section>' for i, n, c in S)
    cuerpo = cabecera("Sacramentos", "Qué hay que hacer, cuándo y con quién hablar.", "forma", alt="Las manos de un sacerdote elevan la forma consagrada") + \
        f'<div class="seccion"><div class="ancho dos"><nav class="indice" aria-label="En esta página"><ul>{indice}</ul></nav><div>{bloques}</div></div></div>'
    pagina("sacramentos.html", "Sacramentos: bautismo, comunión, matrimonio",
           "Bautismo, comunión, confirmación, confesión, matrimonio, comunión a enfermos y columbarios en la parroquia Santo Cristo de la Misericordia.", cuerpo, "sacramentos")


def grupos():
    etapas = [("ninos", "Niños"), ("jovenes", "Jóvenes"), ("adultos", "Adultos y familias")]
    secciones = ""
    for k, nombre in etapas:
        items = ""
        for g in D.GRUPOS:
            if g["etapa"] != k:
                continue
            acciones = ""
            if g.get("enlace"):
                acciones += enlace(*g["enlace"], "")
            if g.get("email"):
                acciones += f'<a class="mas" href="mailto:{g["email"]}">Escribir<span class="solo"> a {e(g["nombre"])}</span>{ico("flecha")}</a>'
            if not acciones:
                acciones = f'<a class="mas" href="contacto.html">Preguntar en secretaría<span class="solo"> por {e(g["nombre"])}</span>{ico("flecha")}</a>'
            fechas = [f'{fecha(i, False)} {i[:4]}' for i, f, _, gid in D.AGENDA if gid == g["id"] and f >= HOY][:2]
            prox = f'<p class="prox">Próximo: {" · ".join(fechas)}</p>' if fechas else ""
            cuando = f'<p class="cuando">{ico("reloj")}{e(g["cuando"])}</p>' if g.get("cuando") else ""
            items += f'<li class="grupo" id="{g["id"]}"><h3>{e(g["nombre"])}</h3><p>{e(g["texto"])}</p>{cuando}{prox}<p class="acciones">{acciones}</p></li>'
        secciones += f'<section class="etapa" id="{k}" data-etapa="{k}"><h2>{nombre}</h2><ul class="grupos">{items}</ul></section>'
    botones = '<button type="button" aria-pressed="true" data-f="todos">Todos</button>' + \
        "".join(f'<button type="button" aria-pressed="false" data-f="{k}">{n}</button>' for k, n in etapas)
    cuerpo = cabecera("Grupos", "De los más pequeños a los matrimonios: encuentra tu sitio y escribe a quien lo coordina.", "jovenes", alt="Jóvenes cantando durante un encuentro") + f"""
<div class="seccion"><div class="ancho"><div class="filtros" role="group" aria-label="Filtrar por edad">{botones}</div>{secciones}
<p>{enlace("Ver el vídeo de la comunidad parroquial", "https://youtu.be/nCb8TmvUHMg", "")}</p></div></div>
<section class="seccion noche"><div class="ancho dos"><div class="intro"><h2>Próximas fechas</h2><p>Añádelas a tu calendario.</p></div>{agenda(20)}</div></section>"""
    pagina("grupos.html", "Grupos y catequesis", "Catequesis, LifeTeen, Light Up, Emaús, Effetá, Bartimeo, Acción Católica, matrimonios y Cáritas en Boadilla del Monte.", cuerpo, "grupos")


def avisos():
    cats = sorted({a["categoria"] for a in AVISOS})
    opciones = "".join(f'<option value="{e(c)}">{e(c)}</option>' for c in cats)
    cuerpo = f"""<div class="seccion"><div class="ancho"><h1>Avisos</h1>
<form class="buscar" role="search" onsubmit="return false"><label>Buscar<input type="search" id="q" placeholder="Semana Santa, retiro, catequesis…" autocomplete="off"></label>
<label>Tema<select id="cat"><option value="">Todos</option>{opciones}</select></label></form>
<p id="cuantos" role="status">{len(AVISOS)} avisos</p>
<ul class="avisos" id="lista">{"".join(tarjeta_aviso(a, nivel="h2") for a in AVISOS)}</ul>
<p class="centro"><button type="button" class="btn btn-petroleo" id="mas" hidden>Ver más avisos</button></p></div></div>"""
    pagina("avisos.html", "Avisos parroquiales", "Todos los avisos de la parroquia: horarios especiales, inscripciones, retiros y peregrinaciones.", cuerpo, "avisos")
    for i, a in enumerate(AVISOS):
        r = "../"
        cuerpo_a = a["html"].replace("\u200b", "")
        cuerpo_a = re.sub(r'<a [^>]*>(<a [^>]*>.*?</a>)</a>', r"\1", cuerpo_a, flags=re.S)  # enlaces anidados en origen
        cuerpo_a = re.sub(r'<a href="[^"]*"[^>]*>\s*</a>', "", cuerpo_a)
        usadas = set()
        for j, f in enumerate(a["figuras"]):
            marca = f"[[IMG{j}]]"
            if f:
                usadas.add(j)
                cuerpo_a = cuerpo_a.replace(marca, img(f, f"Imagen del aviso «{a['titulo']}»", r, "(min-width: 800px) 720px, 100vw"))
        cuerpo_a = re.sub(r"\[\[IMG\d+\]\]", "", cuerpo_a)
        for u in CAIDOS:
            cuerpo_a = re.sub(r'<a href="' + re.escape(e(u)) + r'"[^>]*>(.*?)</a>', r"\1 (enlace ya no disponible)", cuerpo_a, flags=re.S)
        cuerpo_a = re.sub(r"<a [^>]*>(?:\s|<br>|<(?:strong|b|em|i)>\s*</(?:strong|b|em|i)>)*</a>", "", cuerpo_a)
        portada = img(a["portada"], f"Cartel de «{a['titulo']}»", r, "(min-width: 800px) 720px, 100vw", "portada", True) if a["portada"] and not usadas else ""
        viejo = (dt.date.today() - dt.date.fromisoformat(a["fecha"])).days > 120
        archivo = '<p class="archivo">Aviso de archivo: las fechas e inscripciones pueden haber terminado.</p>' if viejo else ""
        desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>|\[\[IMG\d+\]\]", " ", a["html"])).strip()
        desc = html.unescape(desc)[:150] or a["titulo"]
        otros = "".join(tarjeta_aviso(x, r) for x in [x for x in AVISOS[:4] if x is not a][:3])
        pagina(f"avisos/{a['slug']}.html", a["titulo"], desc, f"""<article class="seccion"><div class="ancho lectura">
<p><a class="volver" href="{r}avisos.html">Todos los avisos</a></p><h1>{e(a["titulo"])}</h1>
<p class="aviso-meta"><time datetime="{a["fecha"]}">{fecha(a["fecha"])}</time> · {e(a["categoria"])}</p>{archivo}{portada}<div class="prosa">{cuerpo_a}</div></div></article>
<section class="seccion piedra"><div class="ancho"><h2>Últimos avisos</h2><ul class="avisos destacados">{otros}</ul></div></section>""", "avisos")


def parroquia():
    galeria = [("templo", "Interior del templo, con lucernarios y el altar mayor"), ("patio", "Patio con un ciprés y la torre con la cruz"),
               ("entrada", "Entrada principal y atrio"), ("cristo", "Talla del Cristo crucificado"), ("libro", "Misal abierto sobre un atril de madera"),
               ("flores", "Imagen de santa Teresa de Calcuta entre flores"), ("visita", "El obispo conversa con unos niños durante la visita pastoral"),
               ("sacerdotes", "Cuatro sacerdotes de la parroquia")]
    g = "".join(f"<figure>{img(f, a, '', '(min-width: 760px) 46vw, 100vw')}<figcaption>{a}</figcaption></figure>" for f, a in galeria)
    cuerpo = cabecera("La parroquia", "Nacida en 2001 en la diócesis de Getafe, por petición de su primer obispo.", "patio", alt="Patio de la parroquia con un ciprés y la torre") + f"""
<section class="seccion"><div class="ancho dos"><div class="intro"><h2>Bienvenido al Santo Cristo</h2></div><div class="prosa">
<p>La parroquia Santo Cristo de la Misericordia nació en el seno de la diócesis de Getafe, por petición de su primer obispo, don Francisco José Pérez y Fernández Golfín, en el año 2001.</p>
<p>Diseñada y construida por los arquitectos Del Río Sánchez, es el centro de una gran cantidad de fieles de Boadilla del Monte y de todo Madrid. Está en el sector B de la localidad y forma parte del arciprestazgo de Villaviciosa, que abarca Boadilla, Brunete, Villaviciosa de Odón, Villanueva de la Cañada y Quijorna.</p>
<p>En ella se pueden venerar reliquias de distintos santos y contemplar esculturas de la artista Elena Pilar Palomino-Borbón.</p></div></div>
<div class="ancho"><dl class="cifras"><div><dt>Templos</dt><dd>2</dd></div><div><dt>Aforo del templo dominical</dt><dd>800</dd></div><div><dt>Aforo del templo de diario</dt><dd>200</dd></div><div><dt>Patios exteriores</dt><dd>3</dd></div></dl></div></section>
<section class="seccion piedra"><div class="ancho"><h2>La casa, por dentro</h2><div class="galeria">{g}</div></div></section>"""
    pagina("parroquia.html", "La parroquia: historia y templos", "Historia, templos y vida de la parroquia Santo Cristo de la Misericordia de Boadilla del Monte, fundada en 2001.", cuerpo, "parroquia")


def colabora():
    r = ""
    montos = "".join(f'<button type="button" data-m="{m}" aria-pressed="{str(m == 12).lower()}">{m} €</button>' for m in (9, 12, 20, 50))
    formas = [("Ser catequista", "Una manera preciosa de transmitir la fe a niños, jóvenes y adultos. Pásate y descubre la pastoral de catequesis.", "mailto:" + P["email"] + "?subject=Quiero%20ser%20catequista", "Quiero ser catequista"),
              ("Ser misionero", "La parroquia apoya, entre otras realidades, retiros de Effetá y Emaús por todo el mundo.", "mailto:" + P["email"] + "?subject=Misiones", "Pedir información"),
              ("Voluntario de Cáritas", "Un grupo de voluntarios atiende cada semana a quienes tienen necesidades urgentes.", "caritas.html", "Conocer Cáritas"),
              ("Fundación Golfín", "Su prioridad es acoger las vidas en riesgo de aborto.", "https://www.fundaciongolfin.org/", "Web de la fundación"),
              ("Monitor de campamentos", "Jóvenes que quieran formarse, rezar y trabajar en equipo.", "campamentos.html", "Requisitos")]
    f = "".join(f'<li class="grupo"><h3>{t}</h3><p>{x}</p><p class="acciones">{enlace(b, u, r)}</p></li>' for t, x, u, b in formas)
    cuerpo = cabecera("Colabora", "La parroquia está siempre en activo. Puedes ayudar con tu tiempo y también económicamente.", "comunion", alt="Un sacerdote entrega la comunión") + f"""
<section class="seccion"><div class="ancho dos">
<div class="intro"><h2>Suscripción periódica</h2><p>La parroquia pide 600 personas que aporten 12 € al mes para cubrir un déficit medio mensual de 7.332 €.<br><small>Cifras publicadas por la parroquia en su página de suscripción.</small></p></div>
<div class="cuota"><div class="filtros" role="group" aria-label="Cuota mensual">{montos}</div>
<p class="total" aria-live="polite">Con <b id="cuota">12 €</b> al mes aportas <b id="anual">144 €</b> al año.</p>
<p>{enlace("Suscribirme en el formulario de la parroquia", D.FORM_SUSCRIPCION, r, "btn btn-rojo")}</p>
<p>{enlace("Modificar mi suscripción", D.FORM_MODIFICAR, r)}</p></div></div></section>
<section class="seccion pergamino"><div class="ancho dos"><div class="intro"><h2>Donativo puntual</h2></div><div>{datos_donativo()}
<h3>Desgravación fiscal</h3><p>Los donativos a la Iglesia Católica desgravan en la declaración de la renta; es imprescindible indicar el DNI. Escribe a <a href="mailto:admonscristom@gmail.com">admonscristom@gmail.com</a> con tu nombre, dos apellidos y número de DNI.</p></div></div></section>
<section class="seccion"><div class="ancho"><h2>Con tu tiempo</h2><ul class="grupos">{f}</ul></div></section>"""
    pagina("colabora.html", "Colabora y dona", "Donativos por transferencia o Bizum, suscripción periódica, desgravación fiscal y voluntariado en la parroquia.", cuerpo)


def caritas():
    r = ""
    oracion = "".join(f"<p>{e(x)}</p>" for x in D.ORACION_VOLUNTARIO)
    cuerpo = cabecera("Cáritas parroquial", "Escuchar, orientar y ayudar a las personas necesitadas de nuestro entorno más próximo.", "flores", alt="Imagen de santa Teresa de Calcuta entre flores") + f"""
<section class="seccion"><div class="ancho lectura"><blockquote><p>«Porque tuve hambre y me disteis de comer, tuve sed y me disteis de beber; fui forastero y me hospedasteis, estuve desnudo y me vestisteis; enfermo y me visitasteis, en la cárcel y vinisteis a verme».</p><cite>Mt 25, 35-36</cite></blockquote></div></section>
<section class="seccion piedra"><div class="ancho tres">
<div><h2>Si necesitas ayuda</h2><p>Despacho: viernes de 11:00 a 13:00.<br>Entrega de alimentos: miércoles y jueves de 11:00 a 13:00.<br>Cáritas S.O.L.: miércoles de 11:00 a 13:00.</p><p>{enlace("Escribir a Cáritas", "mailto:scmcaritasboadilla@gmail.com", r)}</p></div>
<div><h2>Hazte voluntario</h2><p>Somos oportunidad, somos esperanza. Servicio de entrega de alimentos y de acogida y acompañamiento.</p><p>{enlace("Quiero ayudar", "mailto:scmcaritasboadilla@gmail.com?subject=Voluntariado", r)}</p></div>
<div><h2>Dona alimentos</h2><p>Alimentos y productos de higiene. Escribe antes para saber qué es más urgente y acordar la entrega.</p><p>{enlace("Día de la Caridad (PDF)", "https://www.caritas.es/main-files/uploads/2023/06/DIPTICO-CARIDAD-2023.pdf", r)}</p></div></div></section>
<section class="seccion pergamino"><div class="ancho dos"><div class="intro"><h2>Donativo a Cáritas</h2><p>Puntual o con suscripción periódica.</p></div><div>{datos_donativo(True)}</div></div></section>
<section class="seccion"><div class="ancho lectura oracion"><h2>Oración del voluntario</h2>{oracion}</div></section>"""
    pagina("caritas.html", "Cáritas parroquial", "Cáritas en la parroquia Santo Cristo de la Misericordia: horarios de atención, voluntariado y donativos.", cuerpo)


def campamentos():
    r = ""
    tur = "".join(f'<li class="grupo"><h3>{n}</h3><p class="grande-fecha">{f}</p><p>{q}</p><p class="cuando">{m}</p></li>' for n, f, q, m in D.CAMPAMENTOS)
    req = "".join(f"<li>{e(x)}</li>" for x in D.REQUISITOS)
    cam = "".join(f"<li><strong>{e(t)}</strong> {e(x)}</li>" for t, x in D.CAMINO)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in D.FAQ)
    cuerpo = cabecera("Campamentos 2027", "Que los niños se acerquen a Dios a través de sus monitores, la naturaleza y la vida de oración.", "montana", alt="Una larga fila de caminantes sube por una ladera de montaña") + f"""
<section class="seccion"><div class="ancho"><h2>Turnos del verano</h2><ul class="grupos cuatro">{tur}</ul>
<p class="nota">Los tres primeros se celebran en el monasterio de la parroquia en San Martín de Don (Burgos). Bachillerato y universitarios: campamento diocesano en Picos de Europa. Cada monitor va a un solo campamento.</p></div></section>
<section class="seccion piedra"><div class="ancho dos"><div class="intro"><h2>Requisitos para ser monitor</h2><p>El monitor no es un amigo para pasarlo bien, sino un referente que se entrega por la misión.</p><p class="archivo">El formulario de candidatura está cerrado.</p>
<p>{enlace("Inscripción al curso de monitor", D.FORM_MONITOR, r)}</p></div><ul class="pasos">{req}</ul></div></section>
<section class="seccion"><div class="ancho dos"><div class="intro"><h2>El camino del monitor</h2></div><ol class="pasos">{cam}</ol></div></section>
<section class="seccion pergamino"><div class="ancho lectura"><h2>Preguntas frecuentes</h2>{faq}</div></section>"""
    pagina("campamentos.html", "Campamentos 2027", "Fechas, turnos, requisitos y preguntas frecuentes de los campamentos de verano 2027 de la parroquia.", cuerpo)


def contacto():
    r = ""
    correos = [("Catequesis de iniciación", "catequesisscm@gmail.com")] + \
        [(g["nombre"], g["email"]) for g in D.GRUPOS if g.get("email") and g["id"] != "iniciacion"] + \
        [("Certificados de donación", "admonscristom@gmail.com")]
    filas = "".join(f'<tr><th scope="row">{e(n)}</th><td><a href="mailto:{m}">{m}</a></td></tr>' for n, m in correos)
    cuerpo = cabecera("Contacto", "Estamos en el sector B de Boadilla del Monte.", "entrada", alt="Entrada principal de la parroquia") + f"""
<section class="seccion"><div class="ancho tres">
<div><h2>Ven</h2><p>{P["calle"]}<br>{P["cp"]} {P["ciudad"]}, {P["provincia"]}</p><p>{enlace("Cómo llegar", P["mapa"], r, "btn btn-petroleo")}</p></div>
<div><h2>Secretaría</h2><p><a class="grande-fecha" href="tel:{P["tel"]}">{P["telefono"]}</a></p><p>Lunes a viernes, 17:00–19:00. Cerrada festivos, julio y agosto.</p><p>{enlace(P["email"], "mailto:" + P["email"], r)}</p></div>
<div><h2>Enfermos</h2><p>Para recibir la comunión en casa:</p><p><a class="grande-fecha" href="tel:{P["enfermos_tel"]}">{P["enfermos"]}</a></p></div></div></section>
<section class="seccion piedra"><div class="ancho"><h2>Escribe a cada grupo</h2><table class="tabla"><tbody>{filas}</tbody></table></div></section>"""
    pagina("contacto.html", "Contacto y cómo llegar", "Dirección, teléfono, secretaría y correos de los grupos de la parroquia Santo Cristo de la Misericordia.", cuerpo, "contacto")


def legales():
    api = RAIZ / "src" / "data" / "privacidad.html"
    pagina("privacidad.html", "Privacidad", "Política de privacidad de la parroquia.", f'<div class="seccion"><div class="ancho lectura prosa"><h1>Privacidad</h1>{api.read_text(encoding="utf-8")}</div></div>')
    pagina("cookies.html", "Cookies", "Esta web no utiliza cookies de seguimiento.", """<div class="seccion"><div class="ancho lectura prosa"><h1>Cookies</h1>
<p>Esta web no instala cookies ni usa herramientas de analítica o publicidad, por eso no te interrumpe con un aviso de consentimiento.</p>
<p>Si activas la letra grande, tu navegador guarda esa preferencia en su almacenamiento local. No sale de tu dispositivo.</p>
<p>Los enlaces a mapas, YouTube, Spotify, iVoox, WhatsApp y formularios abren sitios de terceros con sus propias políticas.</p></div></div>""")
    pagina("404.html", "Página no encontrada", "La página no existe.", """<div class="seccion"><div class="ancho lectura"><h1>No encontramos esa página</h1>
<p>Puede que se haya movido.</p><p class="botones"><a class="btn btn-petroleo" href="index.html">Ir al inicio</a><a class="btn btn-linea oscuro" href="avisos.html">Ver los avisos</a></p></div></div>""")


if __name__ == "__main__":
    (OUT / "assets" / "estilos.css").write_text((SRC / "fuentes.css").read_text(encoding="utf-8") + "\n" + (SRC / "estilos.css").read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / "assets" / "app.js").write_text((SRC / "app.js").read_text(encoding="utf-8"), encoding="utf-8")
    for f in (inicio, horarios, sacramentos, grupos, avisos, parroquia, colabora, caritas, campamentos, contacto, legales):
        f()
    (OUT / ".nojekyll").write_text("")
    print("páginas:", len(list(OUT.rglob("*.html"))))
