"""Contenido de la parroquia, transcrito de www.scristom.es (consultada el 27/11/2026). Editar aquí."""

PARROQUIA = {
    "nombre": "Parroquia Santo Cristo de la Misericordia",
    "calle": "C/ Miguel de Unamuno, 10", "cp": "28660", "ciudad": "Boadilla del Monte", "provincia": "Madrid",
    "telefono": "+34 91 632 50 69", "tel": "+34916325069",
    "enfermos": "659 027 518", "enfermos_tel": "+34659027518",
    "email": "parrocomisericordia@gmail.com",
    "mapa": "https://goo.gl/maps/C8YZoxCFDgdqhscLA",
    "whatsapp": "https://chat.whatsapp.com/IDESOoR6EgsAZMokStrDXI",
    "youtube": "https://www.youtube.com/@consejopastoralscm/",
    "spotify": "https://open.spotify.com/show/3db6vsZbJgAVeXQMs1pHb7",
    "ivoox": "https://www.ivoox.com/podcast-accion-catolica-scm-boadilla_sq_f11361514_1.html",
    "iban": "ES65 0081 0640 6400 0252 3664", "bizum": "38375",
    "iban_caritas": "ES81 0075 0459 5406 0034 0020",
}
ORIGEN = "https://www.scristom.es"
FORM_SUSCRIPCION = ORIGEN + "/suscripcion-periodica/"
FORM_MODIFICAR = ORIGEN + "/modificacion-datos-suscripcion/"
FORM_MONITOR = ORIGEN + "/curso-monitor-de-ocio-y-tiempo-libre-2027/"
FOLLETO_COLUMBARIOS = ORIGEN + "/wp-content/uploads/2023/10/folleto-columbarios-v2.pdf"
FOLLETO_CURSILLOS = ORIGEN + "/wp-content/uploads/2023/02/Cursillos-prematrimoniales-en-la-web-de-SCMpdf.pdf"
FORM_LIFETEEN = "https://docs.google.com/forms/d/e/1FAIpQLScB47xdvGGsP4C9GDZgj74laMfdeF6ygvTBoCQWSvjRBGD4MQ/viewform"

# Misas. dias: 0 domingo ... 6 sábado. verano=False -> se suprime entre el 1 de julio y el 7 de septiembre.
TEMPLO, MONASTERIO = "Parroquia", "Monasterio del Santísimo Sacramento"
MISAS = [
    {"dias": [1, 2, 3, 4, 5], "hora": "08:00", "lugar": MONASTERIO},
    {"dias": [1, 2, 3, 4, 5], "hora": "18:30", "lugar": TEMPLO, "verano": False},
    {"dias": [1, 2, 3, 4, 5], "hora": "20:30", "lugar": TEMPLO},
    {"dias": [6], "hora": "08:00", "lugar": MONASTERIO},
    {"dias": [6], "hora": "10:30", "lugar": TEMPLO, "verano": False},
    {"dias": [6], "hora": "20:30", "lugar": TEMPLO},
    {"dias": [0], "hora": "10:00", "lugar": MONASTERIO},
    {"dias": [0], "hora": "11:00", "lugar": TEMPLO, "nota": "Misa de niños"},
    {"dias": [0], "hora": "12:30", "lugar": TEMPLO},
    {"dias": [0], "hora": "13:30", "lugar": TEMPLO, "verano": False},
    {"dias": [0], "hora": "20:30", "lugar": TEMPLO},
]
# Fiestas fijas en las que se usa el horario de domingo; las dos primeras misas extra son propias del día.
FESTIVOS = ["01-01", "01-06", "05-01", "08-15", "10-12", "11-01", "12-06", "12-08", "12-25"]
EXTRAS = {"12-25": {"hora": "00:00", "lugar": TEMPLO, "nota": "Misa del Gallo"},
          "01-01": {"hora": "01:30", "lugar": TEMPLO, "nota": "Misa de Año Nuevo"}}

ORACION = [
    ("Confesiones", "Media hora antes de cada misa, o siempre que estén los sacerdotes."),
    ("Santo Rosario", "De lunes a viernes a las 9:30 (excepto festivos)."),
    ("Exposición del Santísimo", "De lunes a viernes de 9:30 a 20:30 (excepto verano y festivos)."),
    ("Rosario de la Aurora", "Primeros sábados de mes a las 8:30 (excepto festivos)."),
    ("Comunión reparadora", "Primeros sábados de mes, de 10:00 a 11:30."),
    ("Oración de alabanza", "Lunes a las 20:00 (P. Pedro Pablo)."),
    ("La Hora de la Pasión", "Meditaciones los viernes a las 19:00."),
    ("Acompañando a Jesús", "Jueves de 23:00 a 00:00 (excepto festivos)."),
    ("Adoración de niños", "Primer viernes de mes."),
    ("Primer viernes de mes", "21:15 reparación al Sagrado Corazón · 22:15 alabanza · 23:00 Adoración Nocturna."),
    ("Adoración Nocturna Española", "Terceros viernes de mes, de 22:00 a 5:00."),
]

SEMANA = [
    ("Catequesis de Iniciación Cristiana", "Lunes a jueves 17:30–18:30 · lunes y martes 18:30–19:30 · sábados 11:00–12:00"),
    ("LifeTeen · 5º y 6º de Primaria y 1º de ESO", "Viernes 17:30–19:00"),
    ("LifeTeen · 2º, 3º y 4º de ESO", "Viernes 19:30–21:00"),
    ("Grupo Lázaro", "Lunes 18:30–19:30"),
    ("Confirmación de adultos", "Jueves 21:00–22:00"),
    ("Aula de Teología", "Jueves cada 15 días, 19:00–20:00"),
    ("Grupos de adultos de Acción Católica", "Distintos horarios según el grupo"),
    ("Vida Ascendente", "Jueves alternos 10:30"),
    ("Reuniones de Emaús", "Mujeres: martes 19:30 · hombres: jueves 21:15"),
    ("Coro de adultos", "Ensayo los miércoles 21:30"),
    ("Taller de costura", "Martes 10:30–13:30 (excepto festivos)"),
    ("Cáritas parroquial", "Despacho: viernes 11:00–13:00 · alimentos: miércoles y jueves 11:00–13:00 · S.O.L.: miércoles 11:00–13:00"),
]

# etapa: ninos | jovenes | adultos
GRUPOS = [
    {"id": "iniciacion", "etapa": "ninos", "nombre": "Catequesis de Iniciación Cristiana",
     "texto": "Tres años, de septiembre a la primera semana de junio, para que los niños conozcan y vivan la fe. 1º: la historia de la Salvación. 2º: primera parte del catecismo; reciben la Confesión y la Confirmación. 3º: segunda parte; reciben la Eucaristía.",
     "cuando": "Lunes a jueves 17:30–18:30 · lunes y martes 18:30–19:30 · sábados 11:00–12:00", "email": "catequesisscm@gmail.com"},
    {"id": "lifeteen", "etapa": "jovenes", "nombre": "LifeTeen",
     "texto": "Juveniles de 5º de Primaria a 4º de ESO. Conocen al Señor con juegos, catequesis conjuntas y momentos de oración. La inscripción incluye 10 € de material.",
     "cuando": "Viernes 17:30–19:00 (5º EP a 1º ESO) · 19:30–21:00 (2º a 4º ESO)", "email": "juvenilespscm@gmail.com",
     "enlace": ("Inscripción 2026/27", FORM_LIFETEEN)},
    {"id": "lazaro", "etapa": "ninos", "nombre": "Grupo Lázaro",
     "texto": "Catequesis y oración para niños, adolescentes y jóvenes con discapacidad intelectual, animadas por jóvenes voluntarios, con actividades de ocio compartido.",
     "cuando": "Lunes 18:30–19:30"},
    {"id": "lightup", "etapa": "jovenes", "nombre": "Light Up",
     "texto": "De 1º de Bachillerato a 1º de carrera: formación y catequesis sobre los temas que más preocupan hoy.",
     "cuando": "Viernes 19:30–21:15, en el Cerro del Mosquito", "email": "lightup.scm@gmail.com"},
    {"id": "bartimeo", "etapa": "jovenes", "nombre": "Bartimeo",
     "texto": "Retiro parroquial de jóvenes para jóvenes de 1º y 2º de Bachillerato: una fuerte experiencia del amor de Dios, basada en Mc 10, 46-52.",
     "cuando": "Reuniones de preparación: domingos 18:30", "email": "bartimeo.boadilla@gmail.com"},
    {"id": "effeta", "etapa": "jovenes", "nombre": "Effetá",
     "texto": "Retiro católico de jóvenes para jóvenes para vivir un encuentro personal con Dios. Las reuniones son para quienes ya lo han hecho.",
     "cuando": "Reuniones de preparación: miércoles 21:00", "email": "effetascmboadilla@gmail.com"},
    {"id": "nicodemo", "etapa": "jovenes", "nombre": "Nicodemo",
     "texto": "Retiro de fin de semana para jóvenes profesionales de 24 a 35 años, organizado por laicos. Como caminante se hace una sola vez.",
     "cuando": "Reuniones de preparación: martes 21:00", "email": "nicodemo.boadilla@gmail.com"},
    {"id": "emaus-m", "etapa": "adultos", "nombre": "Emaús mujeres",
     "texto": "Retiro de fin de semana para adultas, organizado por laicas. Como caminante se hace una sola vez.",
     "cuando": "Reuniones: martes", "email": "emausmujeresboadilla@gmail.com"},
    {"id": "emaus-h", "etapa": "adultos", "nombre": "Emaús hombres",
     "texto": "Retiro de fin de semana para adultos, organizado por laicos. Como caminante se hace una sola vez.",
     "cuando": "Reuniones: jueves 21:15", "email": "emaus_hombres@emausboadilla.org"},
    {"id": "accion-catolica", "etapa": "adultos", "nombre": "Acción Católica",
     "texto": "Cada mes el párroco presenta un tema que se trabaja en pequeños grupos con el método de revisión de vida.",
     "cuando": "Reunión mensual", "email": "juntaac.scm@gmail.com",
     "enlace": ("Escuchar las charlas", PARROQUIA["ivoox"])},
    {"id": "amor-conyugal", "etapa": "adultos", "nombre": "Proyecto Amor Conyugal",
     "texto": "Matrimonios que profundizan en su vocación con las catequesis de la Teología del Cuerpo de san Juan Pablo II.",
     "cuando": "Grupos 1, 2, 4, 5, 6 y 7: viernes tras la misa de 20:30 (2º, 3º o 4º del mes) · grupo 3: 3er sábado tras la de 10:30",
     "enlace": ("Inscripciones e información", "https://proyectoamorconyugal.es/misiones-y-noticias/")},
    {"id": "novios", "etapa": "adultos", "nombre": "Grupos de novios",
     "texto": "Charlas e itinerarios tutelados por matrimonios, en grupos de 5 o 6 parejas como máximo.",
     "email": "novioscristom@gmail.com"},
    {"id": "tortugas", "etapa": "adultos", "nombre": "Tortugas",
     "texto": "Padres con hijos en el Cielo, que lo viven con la certeza de la vida eterna. Comparten y se apoyan con la guía del P. Javier Siegrist.",
     "cuando": "Cada tres semanas"},
    {"id": "adoracion", "etapa": "adultos", "nombre": "Adoración Nocturna Española",
     "texto": "Vigilia con misa, charla espiritual, oficio divino, turnos de adoración, rosario y reserva del Santísimo.",
     "cuando": "Terceros viernes de mes, 22:00–5:00"},
    {"id": "caritas", "etapa": "adultos", "nombre": "Cáritas parroquial",
     "texto": "Voluntarios que escuchan, orientan y ayudan a las personas necesitadas de nuestro entorno más próximo.",
     "email": "scmcaritasboadilla@gmail.com", "enlace": ("Conocer Cáritas", "caritas.html")},
]

# (inicio, fin, título, id de grupo)
AGENDA = [
    ("2026-09-11", "2026-09-13", "Retiro Talitha Qumi", None),
    ("2026-12-11", "2026-12-13", "Retiro Bartimeo", "bartimeo"),
    ("2026-12-16", "2026-12-17", "Retiro Simeón y Ana", None),
    ("2027-01-29", "2027-01-31", "Retiro Talitha Qumi", None),
    ("2027-02-05", "2027-02-07", "Cursillo prematrimonial", "novios"),
    ("2027-03-12", "2027-03-14", "Retiro de Emaús mujeres", "emaus-m"),
    ("2027-03-19", "2027-03-21", "Retiro Effetá", "effeta"),
    ("2027-04-09", "2027-04-11", "Cursillo prematrimonial", "novios"),
    ("2027-04-17", "2027-04-18", "Retiro Simeón y Ana", None),
    ("2027-06-04", "2027-06-06", "Cursillo prematrimonial", "novios"),
    ("2027-06-20", "2027-06-30", "Campamento San Martín 1", None),
    ("2027-06-30", "2027-07-11", "Campamento San Martín XL", None),
    ("2027-07-11", "2027-07-18", "Campamento San Martín XL2", None),
    ("2027-07-12", "2027-07-19", "Peregrinación a Loyola", None),
    ("2027-10-01", "2027-10-03", "Retiro de Emaús mujeres", "emaus-m"),
    ("2027-10-22", "2027-10-24", "Retiro de Emaús hombres", "emaus-h"),
    ("2027-11-19", "2027-11-21", "Retiro Bartimeo", "bartimeo"),
]

CAMPAMENTOS = [
    ("San Martín 1", "20–30 de junio", "4º, 5º y 6º de Primaria", "Hasta 12 monitores"),
    ("San Martín XL", "30 de junio – 11 de julio", "1º y 2º de ESO", "Hasta 12 monitores"),
    ("San Martín XL2", "11–18 de julio", "1º y 2º de ESO", "Hasta 12 monitores"),
    ("PEJ Loyola", "12–19 de julio", "3º y 4º de ESO · peregrinación", "Entre 12 y 20 monitores"),
]
REQUISITOS = [
    "Vida de oración y vida apostólica: participar en las catequesis o actividades de la parroquia. Es la condición principal.",
    "Tener 18 años durante el campamento. Los menores de 18 no pueden ser monitores.",
    "Título oficial de monitor de ocio y tiempo libre. Si no lo tienes: curso con Linkceo, 4 fines de semana, 350 €.",
    "Asistir a la reunión introductoria y a la preparación: convivencia de Navidad y Anleo Zero.",
    "Firmar el contrato de voluntario si eres seleccionado.",
]
CAMINO = [
    ("Reunión introductoria", "Imprescindible para ser monitor."),
    ("Candidatura", "Formulario de la parroquia (ahora cerrado)."),
    ("Curso de monitor", "Si no tienes el título: 4 fines de semana con Linkceo, en Boadilla. Fecha por determinar."),
    ("Convivencia de Navidad", "Formación, oración y equipo."),
    ("Selección y contrato", "Los seleccionados firman el contrato de voluntario."),
    ("Anleo Zero", "Mayo–junio: preparamos los campamentos en San Martín de Don."),
    ("Campamentos", "Del 20 de junio al 19 de julio."),
]
FAQ = [
    ("¿Quién puede ser monitor?", "Quien tenga 18 años durante el campamento, el título oficial de monitor de ocio y tiempo libre y participe en la vida de la parroquia."),
    ("Tengo 17 años, ¿puedo ser monitor?", "No. Hay que tener 18 años durante el campamento."),
    ("¿Puedo ir a más de un campamento?", "No. Cada monitor va a un solo campamento: los turnos se encadenan o se solapan."),
    ("¿Puedo elegir campamento?", "Indica tu preferencia en el formulario. La asignación definitiva se hace en la selección."),
    ("No tengo el título, ¿qué hago?", "Puedes hacer el curso con Linkceo: son 4 fines de semana."),
    ("¿Cuánto cuesta el curso y quién lo paga?", "Cuesta 350 € y lo paga cada asistente. La parroquia organizará actividades para ayudar a financiarlo en la medida de lo posible."),
    ("¿Qué significa «vida de oración y vida apostólica»?", "Que la fe forma parte de tu vida y participas en las catequesis o actividades de la parroquia."),
    ("¿Es obligatoria la reunión introductoria?", "Sí. Si no pudiste ir, habla con los supervisores: Iván Jaques, Luis Izquierdo y Sergio Camino."),
    ("¿Qué es Anleo Zero?", "La preparación de los campamentos en San Martín de Don, entre mayo y junio."),
    ("¿Qué diferencia hay entre XL y XL2?", "Son para las mismas edades (1º y 2º de ESO) en fechas distintas."),
]

ORACION_VOLUNTARIO = [
    "Quiero ser, Padre, tus manos, tus ojos, tu corazón.",
    "Mirar al otro como Tú le miras: con una mirada rebosante de amor y de ternura.",
    "Mirarme a mí, también, desde esa plenitud con que Tú me amas, me llamas y me envías.",
    "Lo quiero hacer desde la experiencia del don recibido y con la gratuidad de la donación sencilla y cotidiana al servicio de todos, en especial de los más pobres.",
    "Envíame, Señor, y dame constancia, apertura y cercanía.",
    "Enséñame a caminar en los pies del que acompaño y me acompaña.",
    "Ayúdame a multiplicar el pan y curar heridas, a no dejar de sonreír y de compartir la esperanza.",
    "Quiero servir configurado contigo en tu diaconía.",
    "Gracias por las huellas de ternura y compasión que has dejado en mi vida.",
    "En tu Palabra encuentro la Luz que me ilumina. En la Oración, el Agua que me fecunda y purifica. En la Eucaristía, el Pan que fortalece mi entrega y me da Vida.",
    "Y en mi debilidad, Señor, encuentro tu fortaleza cada día. Amén.",
]
