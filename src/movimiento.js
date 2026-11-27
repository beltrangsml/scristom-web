/* Transiciones con GSAP + ScrollTrigger. Si la librería no carga o el usuario pide menos movimiento, la web se ve igual, sin animar. */
(() => {
  const cab = document.querySelector('.cab');
  const marcarCab = () => cab && cab.classList.toggle('con-sombra', scrollY > 8);
  addEventListener('scroll', marcarCab, { passive: true }); marcarCab();

  if (!window.gsap || !window.ScrollTrigger || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  const curva = 'expo.out';

  // Barra fina de progreso de lectura
  const barra = document.createElement('div');
  barra.className = 'barra-progreso'; barra.setAttribute('aria-hidden', 'true');
  document.body.prepend(barra);
  gsap.to(barra, { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: .3 } });

  // Entrada de la portada
  const heroe = document.querySelector('.heroe');
  if (heroe) {
    heroe.querySelectorAll('.heroe-in > *').forEach(el => { el.style.animation = 'none'; });
    const foto = heroe.querySelector('.heroe-foto');
    const tl = gsap.timeline({ defaults: { ease: curva } });
    if (foto) tl.fromTo(foto, { scale: 1.12 }, { scale: 1, duration: 2.4, ease: 'power2.out' }, 0);
    tl.from(heroe.querySelectorAll('.tiempo, h1, .heroe-texto > p, .botones'), { y: 34, autoAlpha: 0, duration: 1.1, stagger: .1 }, .15)
      .from(heroe.querySelector('.proxima'), { y: 50, autoAlpha: 0, duration: 1.2 }, .45);
    if (foto) gsap.to(foto, { yPercent: 12, ease: 'none', scrollTrigger: { trigger: heroe, start: 'top top', end: 'bottom top', scrub: true } });
  }

  // Cabeceras de página interiores (primer h1 fuera de la portada)
  const h1 = !heroe && document.querySelector('main h1');
  if (h1) gsap.from(h1, { y: 26, autoAlpha: 0, duration: 1, ease: curva });

  // Aparición al hacer scroll, en grupos escalonados
  const sel = '.g-card, .etapa-cab, .g-video, .sec-cab, .intro > *, .quiero li, .dia, .aviso, .tres > div, .intro-foto, .misas + *, .pie .ancho:not(.pie-legal) > *, main section .ancho > h2, main section .ancho > p';
  const items = gsap.utils.toArray(sel).filter(el => !el.closest('.heroe'));
  gsap.set(items, { autoAlpha: 0, y: 40 });
  let ultimo = 0, enGrupo = 0;
  items.forEach(el => ScrollTrigger.create({
    trigger: el, start: 'top 92%', once: true,
    onEnter: () => {
      const ahora = performance.now(); enGrupo = ahora - ultimo < 120 ? enGrupo + 1 : 0; ultimo = ahora;
      gsap.to(el, { autoAlpha: 1, y: 0, duration: 1, ease: curva, delay: Math.min(enGrupo, 6) * .08, clearProps: 'transform,opacity,visibility' });
    }
  }));

  // Fotos de avisos: ligero zoom de entrada
  gsap.utils.toArray('.aviso-foto img').forEach(img => {
    gsap.from(img, { scale: 1.15, duration: 1.6, ease: 'power3.out', scrollTrigger: { trigger: img, start: 'top 92%', once: true } });
  });

  addEventListener('load', () => ScrollTrigger.refresh());
  // Filtros y buscadores cambian la altura de la página: recalcular para que nada quede oculto
  ['input', 'click', 'change'].forEach(ev => document.addEventListener(ev, () => setTimeout(() => ScrollTrigger.refresh(), 60)));
})();
