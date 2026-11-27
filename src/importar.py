"""Importa avisos, fotos y fuentes desde la web actual (se ejecuta una vez; el resultado queda en el repo).

  py -X utf8 src/importar.py <carpeta-con-posts.json> <carpeta-cache-de-imagenes>
"""
import concurrent.futures as cf
import hashlib
import html
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parents[1]
ASSETS = RAIZ / "docs" / "assets"
API, CACHE = Path(sys.argv[1]), Path(sys.argv[2])
SITIO = "https://www.scristom.es/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}


def bajar(url: str) -> bytes:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / hashlib.sha1(url.encode()).hexdigest()
    if not f.exists():
        p = urllib.parse.urlsplit(url)
        segura = urllib.parse.urlunsplit(p._replace(path=urllib.parse.quote(p.path, safe="/%")))
        f.write_bytes(urllib.request.urlopen(urllib.request.Request(segura, headers=UA), timeout=60).read())
    return f.read_bytes()


def webp(url: str, nombre: str, anchos, calidad=76) -> dict | None:
    """Guarda la imagen en varios anchos. Devuelve {nombre, anchos, w, h}."""
    try:
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(bajar(url))))
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
    except Exception as e:  # imagen rota en el origen: se omite y se avisa
        print("  imagen omitida:", url, type(e).__name__)
        return None
    hechos = []
    for a in anchos:
        w = min(a, im.width)
        if w in hechos:
            continue
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(ASSETS / "img" / f"{nombre}-{w}.webp", quality=calidad, method=6)
        hechos.append(w)
    return {"nombre": nombre, "anchos": hechos, "w": hechos[-1], "h": round(im.height * hechos[-1] / im.width)}


# ---------- fotos de la web ----------
FOTOS = {
    "retablo": "2023/06/154A3724.jpg", "cristo": "2024/02/154A3616-scaled-e1708075558946.jpg",
    "templo": "2020/04/IWJP4822.jpg", "patio": "2020/04/IWJP5041.jpg", "entrada": "2020/04/IWJP5056.jpg",
    "forma": "2020/04/IWJP4963-e1587593533970.jpg", "libro": "2020/04/IWJP4787.jpg", "campana": "2020/04/IWJP4877.jpg",
    "flores": "2020/04/IWJP4920.jpg", "san-cristobal": "2020/04/IWJP4994.jpg", "comunion": "2023/11/comunion.jpg",
    "custodia": "2023/09/oracion-custodia-.jpg", "adoracion": "2024/02/visita-pastoral005-scaled.jpg",
    "visita": "2024/02/visita-pastoral141-scaled.jpg", "jovenes": "2020/04/lifeteen.jpg",
    "montana": "2020/06/fbc0e6f2-d27a-486a-82e5-c38c47325d5b.jpg", "columbarios": "2023/10/columbario.jpg",
    "sacerdotes": "2024/11/IWJ09161.jpg", "mision": "2022/12/154A5900-scaled.jpg",
}
LOGO = "2023/06/v2.png"


class Limpiar(HTMLParser):
    """Lista blanca estricta: el HTML de origen es contenido no fiable."""
    OK = {"p", "h2", "h3", "h4", "ul", "ol", "li", "strong", "b", "em", "i", "br", "a", "table", "tr", "td", "th", "tbody"}
    FUERA = {"script", "style", "svg", "form", "noscript", "iframe", "button", "select", "textarea"}

    def __init__(self, slugs, imagenes):
        super().__init__()
        self.out, self.pila, self.skip, self.slugs, self.imagenes = [], [], 0, slugs, imagenes

    def handle_starttag(self, t, attrs):
        a = dict(attrs)
        if t in self.FUERA:
            self.skip += 1
            return
        if self.skip:
            return
        if t == "img":
            src = a.get("data-src") or a.get("src") or ""
            if src.startswith(SITIO + "wp-content/uploads/"):
                self.imagenes.append(src)
                self.out.append(f"[[IMG{len(self.imagenes) - 1}]]")
            return
        if t == "h1":
            t = "h2"
        if t not in self.OK:
            return
        if t == "br":
            self.out.append("<br>")
            return
        extra = ""
        if t == "a":
            u = (a.get("href") or "").strip().replace("mailto:mailto:", "mailto:")
            if not re.match(r"^(https?://|mailto:|tel:)", u):
                return
            m = re.match(r"https?://(?:www\.)?scristom\.es/\d{4}/\d\d/\d\d/([^/?#]+)/?$", u)
            if m and urllib.parse.unquote(m[1]) in self.slugs:
                u = self.slugs[urllib.parse.unquote(m[1])] + ".html"
            extra = f' href="{html.escape(u, quote=True)}"' + (' rel="noopener"' if u.startswith("http") else "")
        self.pila.append(t)
        self.out.append(f"<{t}{extra}>")

    def handle_endtag(self, t):
        if t in self.FUERA:
            self.skip = max(0, self.skip - 1)
            return
        t = "h2" if t == "h1" else t
        if not self.skip and t in self.pila:
            while self.pila:
                x = self.pila.pop()
                self.out.append(f"</{x}>")
                if x == t:
                    break

    def handle_data(self, d):
        if not self.skip:
            self.out.append(html.escape(d, quote=False))

    def resultado(self):
        s = "".join(self.out) + "".join(f"</{t}>" for t in reversed(self.pila))
        s = s.replace("\xa0", " ")
        for _ in range(4):
            s = re.sub(r"<(p|h2|h3|h4|a|strong|b|em|i|li|ul)(?: [^>]*)?>(?:\s|<br>)*</\1>", "", s)
        return re.sub(r"\n\s*\n+", "\n", s).strip()


def slug_seguro(s: str) -> str:
    s = urllib.parse.unquote(s).replace("·", "-")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9-]", "-", s.lower())).strip("-")[:80]


def main():
    (ASSETS / "img").mkdir(parents=True, exist_ok=True)
    (ASSETS / "fonts").mkdir(parents=True, exist_ok=True)
    (RAIZ / "src" / "data").mkdir(parents=True, exist_ok=True)

    posts = json.loads((API / "posts.json").read_text(encoding="utf-8"))
    cats = {c["id"]: html.unescape(c["name"]) for c in json.loads((API / "categories.json").read_text(encoding="utf-8"))}
    slugs = {urllib.parse.unquote(p["slug"]): slug_seguro(p["slug"]) for p in posts}

    def aviso(p):
        slug = slugs[urllib.parse.unquote(p["slug"])]
        imgs = []
        lim = Limpiar(slugs, imgs)
        lim.feed(p["content"]["rendered"])
        cuerpo = lim.resultado()
        fm = (p.get("_embedded", {}).get("wp:featuredmedia") or [{}])[0].get("source_url")
        portada = webp(fm, f"a-{slug}", (480, 960)) if fm else None
        figuras = []
        for i, u in enumerate(imgs[:8]):
            if fm and u.rsplit(".", 1)[0].split("-scaled")[0] in fm:
                figuras.append(None)
                continue
            figuras.append(webp(u, f"a-{slug}-{i}", (960,)))
        return {
            "slug": slug, "fecha": p["date"][:10], "titulo": html.unescape(p["title"]["rendered"]).strip().rstrip("."),
            "categoria": next((cats[c] for c in p.get("categories", []) if c in cats), "Avisos"),
            "html": cuerpo, "portada": portada, "figuras": figuras, "origen": p["link"],
        }

    with cf.ThreadPoolExecutor(8) as ex:
        avisos = list(ex.map(aviso, posts))
    avisos.sort(key=lambda a: a["fecha"], reverse=True)
    (RAIZ / "src" / "data" / "avisos.json").write_text(json.dumps(avisos, ensure_ascii=False, indent=1), encoding="utf-8")
    print("avisos:", len(avisos))

    base = SITIO + "wp-content/uploads/"
    with cf.ThreadPoolExecutor(6) as ex:
        res = dict(zip(FOTOS, ex.map(lambda kv: webp(base + kv[1], kv[0], (640, 1100, 1800), 72), FOTOS.items())))
    (RAIZ / "src" / "data" / "fotos.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("fotos:", sum(bool(v) for v in res.values()), "/", len(FOTOS))

    logo = Image.open(io.BytesIO(bajar(base + LOGO))).convert("RGBA")
    for n in (112, 256):
        logo.resize((n, round(n * logo.height / logo.width)), Image.LANCZOS).save(ASSETS / "img" / f"logo-{n}.webp", quality=90)
    fav = Image.open(io.BytesIO(bajar(base + "2020/04/favicon.png"))).convert("RGBA")
    for n in (48, 180):
        fondo = Image.new("RGBA", (n, n), (255, 255, 255, 255))
        mini = fav.copy()
        mini.thumbnail((n - n // 8, n - n // 8), Image.LANCZOS)
        fondo.alpha_composite(mini, ((n - mini.width) // 2, (n - mini.height) // 2))
        fondo.save(ASSETS / "img" / f"icono-{n}.png")
    ImageOps.fit(Image.open(io.BytesIO(bajar(base + FOTOS["retablo"]))).convert("RGB"), (1200, 630)).save(
        ASSETS / "img" / "og.jpg", quality=80)

    css = urllib.request.urlopen(urllib.request.Request(
        "https://fonts.googleapis.com/css2?family=Marcellus&family=Source+Sans+3:wght@400..700&display=swap",
        headers=UA), timeout=60).read().decode()
    caras = []
    for subset, bloque in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S):
        if subset != "latin":
            continue
        u = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", bloque)[1]
        nombre = ("marcellus" if "Marcellus" in bloque else "sourcesans") + ".woff2"
        (ASSETS / "fonts" / nombre).write_bytes(bajar(u))
        caras.append(bloque.replace(u, f"fonts/{nombre}"))
    (RAIZ / "src" / "fuentes.css").write_text("\n".join(caras), encoding="utf-8")
    print("fuentes:", len(caras))


if __name__ == "__main__":
    main()
