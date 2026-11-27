(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const pad = n => String(n).padStart(2, '0');

  // Menú móvil
  const btn = $('.menu-btn'), menu = $('#menu');
  const abrir = v => { btn.setAttribute('aria-expanded', v); menu.classList.toggle('abierto', v); };
  btn?.addEventListener('click', () => abrir(btn.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', ev => {
    if (ev.key === 'Escape' && menu?.classList.contains('abierto')) { abrir(false); btn.focus(); }
  });

  // Letra grande
  const letra = $('.letra');
  if (letra) {
    const pinta = () => letra.setAttribute('aria-pressed', document.documentElement.classList.contains('grande'));
    pinta();
    letra.addEventListener('click', () => {
      const on = document.documentElement.classList.toggle('grande');
      try { localStorage.setItem('letra', on ? 'grande' : ''); } catch (e) { /* modo privado */ }
      pinta();
    });
  }

  // Hora de Madrid, esté donde esté el visitante. Se devuelve como fecha "en UTC" para operar sin husos.
  const madrid = () => {
    const forzada = new URLSearchParams(location.search).get('ahora'); // para pruebas: ?ahora=2026-12-24T23:00
    if (forzada) return new Date(forzada + (forzada.length === 16 ? ':00Z' : 'Z'));
    const p = Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Madrid', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
      .formatToParts(new Date()).map(x => [x.type, x.value]));
    return new Date(Date.UTC(+p.year, p.month - 1, +p.day, +p.hour, +p.minute));
  };
  const ahora = madrid();
  const DIA = 864e5;
  const iso = d => d.toISOString().slice(0, 10);
  const utc = (a, m, d) => new Date(Date.UTC(a, m - 1, d));
  const hoy = utc(ahora.getUTCFullYear(), ahora.getUTCMonth() + 1, ahora.getUTCDate());

  // Tiempo litúrgico
  const pascua = a => {
    const g = a % 19, c = Math.floor(a / 100), h = (c - Math.floor(c / 4) - Math.floor((8 * c + 13) / 25) + 19 * g + 15) % 30,
      i = h - Math.floor(h / 28) * (1 - Math.floor(29 / (h + 1)) * Math.floor((21 - g) / 11)),
      j = (a + Math.floor(a / 4) + i + 2 - c + Math.floor(c / 4)) % 7, l = i - j,
      m = 3 + Math.floor((l + 40) / 44);
    return utc(a, m, l + 28 - 31 * Math.floor(m / 4));
  };
  const tiempo = d => {
    const a = d.getUTCFullYear(), P = +pascua(a), t = +d;
    const navidad = utc(a, 12, 25);
    const adviento = +navidad - ((navidad.getUTCDay() || 7) + 21) * DIA;
    const epifania = utc(a, 1, 6);
    const bautismo = +epifania + (7 - epifania.getUTCDay()) * DIA;
    if (t >= +navidad || t <= bautismo) return ['Tiempo de Navidad', '#f2e3b3'];
    if (t >= adviento) return ['Tiempo de Adviento', '#b79ad6'];
    if (t >= P - 3 * DIA && t < P) return ['Triduo Pascual', '#e48b8b'];
    if (t >= P - 46 * DIA && t < P) return ['Tiempo de Cuaresma', '#b79ad6'];
    if (t >= P && t <= P + 49 * DIA) return ['Tiempo de Pascua', '#f2e3b3'];
    return ['Tiempo Ordinario', '#8fcf9d'];
  };

  // Próxima misa
  const datos = $('#misas');
  if (datos) {
    const { misas, festivos, extras } = JSON.parse(datos.textContent);
    const nombres = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
    const delDia = d => {
      const md = iso(d).slice(5);
      const verano = md >= '07-01' && md <= '09-07';
      const dia = festivos.includes(md) ? 0 : d.getUTCDay();
      const lista = misas.filter(m => m.dias.includes(dia) && !(verano && m.verano === false));
      if (extras[md]) lista.push(extras[md]);
      return lista.map(m => {
        const [h, min] = m.hora.split(':').map(Number);
        return { ...m, cuando: new Date(+d + (h * 60 + min) * 6e4) };
      });
    };
    const pinta = () => {
      const t = madrid();
      const base = utc(t.getUTCFullYear(), t.getUTCMonth() + 1, t.getUTCDate());
      const futuras = [0, 1, 2, 3].flatMap(i => delDia(new Date(+base + i * DIA))).filter(m => m.cuando > t).sort((a, b) => a.cuando - b.cuando);
      if (!futuras.length) return;
      const cuandoTxt = m => {
        const dif = Math.round((utc(m.cuando.getUTCFullYear(), m.cuando.getUTCMonth() + 1, m.cuando.getUTCDate()) - base) / DIA);
        return dif === 0 ? 'Hoy' : dif === 1 ? 'Mañana' : nombres[m.cuando.getUTCDay()].replace(/^./, c => c.toUpperCase());
      };
      const hora = m => m.hora.replace(/^0/, '');
      const [p, ...resto] = futuras;
      const falta = Math.round((p.cuando - t) / 6e4);
      $('#prox-hora').textContent = hora(p);
      $('#prox-dia').textContent = `${cuandoTxt(p)} · ${p.lugar}${p.nota ? ' · ' + p.nota : ''}`;
      $('#prox-falta').textContent = falta < 60 ? `Empieza en ${falta} min` : falta < 720 ? `Empieza en ${Math.floor(falta / 60)} h ${falta % 60} min` : '';
      $('#prox-lista').replaceChildren(...resto.slice(0, 3).map(m => {
        const li = document.createElement('li'), a = document.createElement('span'), b = document.createElement('b');
        a.textContent = `${cuandoTxt(m)}${m.lugar.startsWith('Monasterio') ? ' · Monasterio' : ''}`;
        b.textContent = hora(m);
        li.append(a, b);
        return li;
      }));
      const md = iso(base).slice(5);
      const col = festivos.includes(md) ? 0 : [0, 6].includes(base.getUTCDay()) ? base.getUTCDay() : 1;
      $(`.dia[data-dia="${col}"]`)?.classList.add('hoy');
    };
    pinta();
    setInterval(pinta, 30000);
    const [nombre, color] = tiempo(hoy);
    const chip = $('#tiempo');
    chip.textContent = nombre;
    chip.style.setProperty('--liturgico', color);
    chip.classList.add('con-color');
  }

  // Agenda: fuera lo pasado, límite, y exportación .ics
  $$('.agenda').forEach(lista => {
    $$('li', lista).filter(li => li.dataset.fin < iso(hoy)).forEach(li => li.remove());
    $$('li', lista).slice(+lista.dataset.limite).forEach(li => li.remove());
  });
  $$('.ics').forEach(b => b.addEventListener('click', () => {
    const li = b.closest('li');
    const f = s => s.replaceAll('-', '');
    const fin = iso(new Date(+new Date(li.dataset.fin + 'T00:00:00Z') + DIA));
    const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//SCM//Agenda//ES', 'BEGIN:VEVENT',
      `UID:${f(li.dataset.ini)}-${b.dataset.titulo.replace(/\W/g, '')}@scm`, `DTSTAMP:${f(iso(hoy))}T000000Z`,
      `DTSTART;VALUE=DATE:${f(li.dataset.ini)}`, `DTEND;VALUE=DATE:${f(fin)}`, `SUMMARY:${b.dataset.titulo}`,
      'LOCATION:Parroquia Santo Cristo de la Misericordia (confirmar lugar)', 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' }));
    a.download = 'evento-parroquia.ics';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }));

  // Copiar IBAN / Bizum
  $$('.copiar').forEach(b => b.addEventListener('click', async () => {
    const texto = b.firstChild.textContent;
    try { await navigator.clipboard.writeText(b.dataset.copiar); b.firstChild.textContent = 'Copiado'; }
    catch (e) { const r = document.createRange(); r.selectNodeContents(b.previousElementSibling); getSelection().removeAllRanges(); getSelection().addRange(r); b.firstChild.textContent = 'Seleccionado'; }
    setTimeout(() => { b.firstChild.textContent = texto; }, 2000);
  }));

  // Filtro de grupos
  const etapas = $$('.etapa');
  if (etapas.length) $$('.filtros button[data-f]').forEach(b => b.addEventListener('click', () => {
    $$('.filtros button[data-f]').forEach(x => x.setAttribute('aria-pressed', x === b));
    etapas.forEach(s => { s.hidden = b.dataset.f !== 'todos' && s.dataset.etapa !== b.dataset.f; });
  }));

  // Cuota de suscripción
  $$('.cuota button[data-m]').forEach(b => b.addEventListener('click', () => {
    $$('.cuota button[data-m]').forEach(x => x.setAttribute('aria-pressed', x === b));
    $('#cuota').textContent = `${b.dataset.m} €`;
    $('#anual').textContent = `${b.dataset.m * 12} €`;
  }));

  // Buscador de avisos
  const lista = $('#lista');
  if (lista) {
    const q = $('#q'), cat = $('#cat'), mas = $('#mas'), items = $$('.aviso', lista);
    const norm = s => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
    let visibles = 12;
    const filtrar = () => {
      const t = norm(q.value.trim());
      const ok = items.filter(li => (!cat.value || li.dataset.cat === cat.value) && norm(li.dataset.t).includes(t));
      items.forEach(li => { li.hidden = true; });
      ok.slice(0, visibles).forEach(li => { li.hidden = false; });
      mas.hidden = ok.length <= visibles;
      $('#cuantos').textContent = ok.length ? `${ok.length} ${ok.length === 1 ? 'aviso' : 'avisos'}` : 'No hay avisos con esa búsqueda. Prueba otra palabra o elige «Todos».';
    };
    [q, cat].forEach(x => x.addEventListener('input', () => { visibles = 12; filtrar(); }));
    mas.addEventListener('click', () => { visibles += 12; filtrar(); });
    filtrar();
  }
})();
