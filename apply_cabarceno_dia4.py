import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

INDEX_PATH = "index.html"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Hero description in Cantabria
content = re.sub(
    r'<p style="max-width: 850px; margin: 0 auto 20px; font-size: 1.05rem; color: #E2E8F0; font-weight: 300;">.*?</p>',
    r'<p style="max-width: 850px; margin: 0 auto 20px; font-size: 1.05rem; color: #E2E8F0; font-weight: 300;">Salida cómoda desde Quer (Guadalajara) en el Volvo XC60. Base céntrica en casona rural del Valle del Saja con chimenea. Secuoyas de 40m, Poblado Navideño de Cartes, Picos de Europa y Fuente Dé con nieve, Santander y La Magdalena (pingüinos y carabelas gratis), Balneario de Solares a 34°C con piscina infantil para Marco, y el último día Cabárceno Safari a primera hora antes de volver directos por la A-67 a Quer con luz de tarde.</p>',
    content,
    flags=re.DOTALL
)

# 2. Update Route description
content = content.replace(
    "• <strong>Ida (Sábado 5)</strong>: Quer ➔ Cabárceno (directo 1ª hora): <strong>378 km · 3h 45m</strong> (salida 05:15 h, A-1 y A-67 con parada en Lerma, llegada 09:25 h para apertura taquillas 09:30 h).<br>\n              • <strong>Vuelta (Martes 8)</strong>: Santander ➔ Quer (Guadalajara): <strong>378 km · 3h 45m</strong> (salida 17:15 h, llegada 21:00 h).",
    "• <strong>Ida (Sábado 5)</strong>: Quer ➔ Casona del Saja / Secuoyas: <strong>378 km · 3h 45m</strong> (salida tranquila 07:45 h por A-1 y A-67 con parada en Lerma, llegada 12:15 h).<br>\n              • <strong>Vuelta (Martes 8)</strong>: Cabárceno ➔ Quer (Guadalajara): <strong>375 km · 3h 45m</strong> (salida directa 15:30 h por A-67 hacia el sur sin entrar a Santander, llegada a Quer 19:15 h con luz de tarde)."
)

# 3. Update Timeline
timeline_start = '<div class="timeline" id="timeline-cantabria">'
timeline_end = '<!-- TABLA DE PRESUPUESTO DINÁMICA -->'

tl_idx_start = content.find(timeline_start)
tl_idx_end = content.find(timeline_end, tl_idx_start)

if tl_idx_start == -1 or tl_idx_end == -1:
    print("ERROR: Timeline markers not found!")
    sys.exit(1)

new_timeline_html = """<div class="timeline" id="timeline-cantabria">

          <!-- DÍA 1 -->
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#059669;"></div>
            <div class="timeline-content">
              <span class="timeline-day" style="color:#059669;">DÍA 1 · SÁBADO 5 DE DICIEMBRE · SALIDA CÓMODA, SECUOYAS & POBLADO NAVIDEÑO DE CARTES</span>
              <h3 style="margin: 4px 0 10px 0; font-size: 1.15rem; color: #0F172A;">Ruta en Volvo XC60 desde Quer, Bosque de Secuoyas de 40m, Cocido Montañés, Descanso en Casona & Poblado Navideño de Cartes</h3>
              <p style="font-size: 0.9rem; color: #475569; line-height: 1.5; margin-bottom: 12px;">
                • <strong>07:45 h - 08:30 h</strong>: ☕ <strong>Desayuno en Casa y Salida en Volvo XC60</strong>: Desayuno caliente en Quer (Guadalajara), carga de maletas sin prisas y salida cómoda por la N-320 conectando con la autovía A-1 directa hacia Burgos y la A-67 hacia Torrelavega (378 km, 3h 45m sin peajes, con parada en Lerma para estirar piernas y café). Marco duerme el primer tramo.<br>
                • <strong>12:15 h - 13:30 h</strong>: 🌲 <strong>Monumento Natural de las Secuoyas de Monte Corona</strong> (Cabezón de la Sal): Nada más llegar de la autovía, sendero llano de pasarelas de madera entre 848 secuoyas gigantes de más de 40 metros de altura. Terreno 100% llano, accesible y perfecto para que Marco corra libremente y abrace troncos gigantes tras el viaje.<br>
                • <strong>13:45 h - 15:15 h</strong>: 🥘 <strong>Comida / Almuerzo Montañés en el Valle del Saja</strong>: Puchero tradicional humeante de <strong>Cocido Montañés cántabro</strong> con alubia blanca fina, berza de huerta y compango artesano en cazuela de barro en mesón rústico con chimenea (Casa Cofiño en Caviedes o El Jardín en Cabezón).<br>
                • <strong>15:30 h - 17:00 h</strong>: 🏡 <strong>Check-in en la Casona del Saja & Siesta de Marco</strong>: Llegada a vuestra casona montañesa independiente con chimenea y jardín cerrado, desempaque de maletas y siesta reparadora junto al fuego.<br>
                • <strong>17:15 h - 19:45 h</strong>: 🎄 <strong>El Famoso Poblado Navideño de Cartes & Árbol Gigante de 65m</strong> (a solo 12 min): El pueblo medieval de cuento de hadas más viral de España. Camino Real iluminado al anochecer, soldados cascanueces gigantes, casitas de madera de los elfos, túnel de luces en Parque del Ánsar y visita a la <strong>Casa de Papá Noel</strong> para que Marco le entregue su carta en mano.<br>
                • <strong>20:15 h - 21:30 h</strong>: 🌙 <strong>Cena Familiar & Chimenea de Leña</strong>: Regreso en 12 min a la casona rural de Cabezón, cena reconfortante al calor del fuego y descanso temprano para empezar el domingo con máxima energía.
              </p>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span style="background:#DCFCE7;color:#166534;padding:3px 8px;border-radius:6px;font-size:0.75rem;font-weight:700;">⭐ Momento Marco: Entregar la carta en mano a Papá Noel en Cartes y correr entre los troncos gigantes de secuoyas</span>
              </div>
            </div>
          </div>

          <!-- DÍA 2 -->
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#059669;"></div>
            <div class="timeline-content">
              <span class="timeline-day" style="color:#059669;">DÍA 2 · DOMINGO 6 DE DICIEMBRE · PICOS DE EUROPA, FUENTE DÉ CON NIEVE & POTES</span>
              <h3 style="margin: 4px 0 10px 0; font-size: 1.15rem; color: #0F172A;">Desfiladero de La Hermida, Teleférico Fuente Dé a 1.823m con Nieve, Festín de Cocido Lebaniego en Potes, Cueva de El Soplao & Santillana</h3>
              <p style="font-size: 0.9rem; color: #475569; line-height: 1.5; margin-bottom: 12px;">
                • <strong>08:00 h - 08:45 h</strong>: ☕ <strong>Desayuno Energético de Montaña</strong>: Sobaos pasiegos artesanos, tostadas de pan de hogaza y café caliente en la casona.<br>
                • <strong>10:00 h - 12:45 h</strong>: 🚠 <strong>Picos de Europa & Teleférico de Fuente Dé (1.823m)</strong>:<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• Espectacular ruta escénica por el Desfiladero de La Hermida en el Volvo XC60.<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• Ascenso vertiginoso salvando 753m de desnivel en 4 minutos hasta la estación alta de El Cable.<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• Mirador acristalado sobre las nubes y juego seguro con la nieve para Marco.<br>
                • <strong>13:10 h - 15:10 h</strong>: 🍲 <strong>Comida / Festín de Cocido Lebaniego en Potes</strong>:<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• Paseo por el barrio medieval de la Solana de Potes y puentes empedrados sobre el río Quivieso.<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• Gran almuerzo de gala en mesón típico: sopa de cabello de ángel, garbanzos finos de Liébana, relleno de miga, cecina y compango artesano.<br>
                • <strong>16:00 h - 17:30 h</strong>: 🚂 <strong>Cueva de El Soplao en Tren Minero Subterráneo</strong> (o Neocueva de Altamira): Viaje en trenecito bajo tierra descubriendo la 'Capilla Sixtina' de las formaciones excéntricas.<br>
                • <strong>18:05 h - 19:30 h</strong>: 🏘️ <strong>Santillana del Mar Medieval</strong>: Calles empedradas peatonales sin coches, Colegiata románica iluminada y degustación de sobaos pasiegos calientes.<br>
                • <strong>20:00 h - 21:20 h</strong>: 🌙 <strong>Cena Montañesa & Tertulia Familiar</strong>: Cena relajada en la casona rural y descanso al calor del fuego.
              </p>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span style="background:#E0F2FE;color:#0369A1;padding:3px 8px;border-radius:6px;font-size:0.75rem;font-weight:700;">⭐ Momento Marco: Tocar la nieve y hacer un muñeco en el Mirador de Fuente Dé a 1.823m y viajar en el tren minero bajo tierra</span>
              </div>
            </div>
          </div>

          <!-- DÍA 3 -->
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#059669;"></div>
            <div class="timeline-content">
              <span class="timeline-day" style="color:#059669;">DÍA 3 · LUNES 7 DE DICIEMBRE · SANTANDER CAPITAL, RABAS & BALNEARIO INFANTIL SOLARES</span>
              <h3 style="margin: 4px 0 10px 0; font-size: 1.15rem; color: #0F172A;">Península de La Magdalena (Pingüinos, Focas & Carabelas 100% Gratis), Rabas en la Bahía, Balneario de Solares a 34°C & Liérganes</h3>
              <p style="font-size: 0.9rem; color: #475569; line-height: 1.5; margin-bottom: 12px;">
                • <strong>08:30 h - 09:15 h</strong>: ☕ <strong>Desayuno Montañés</strong>: Sobaos pasiegos y café recién hecho en la casona antes de salir hacia Santander (35 min por A-67).<br>
                • <strong>10:00 h - 12:45 h</strong>: 🐬 <strong>Península de La Magdalena en Santander (¡100% Gratis!)</strong>:<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <strong>Parque Marino Natural en Acantilados</strong>: Piscinas de roca natural donde entra el Cantábrico con focas grises, leones marinos y pingüinos de Humboldt a un palmo de los niños.<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <strong>Las 3 Carabelas Piratas de Vital Alsar</strong> a escala real para que Marco suba a cubierta, más parque infantil con columpios marítimos frente a la playa.<br>
                • <strong>13:00 h - 14:30 h</strong>: 🐟 <strong>Comida / Almuerzo Marinero de Rabas en la Bahía / Puerto Chico</strong>: Rabas frescas de calamar recién fritas, mejillones al vapor y pescado del Cantábrico frente al mar.<br>
                • <strong>14:45 h - 15:45 h</strong>: ⛸️ <strong>Santander Navideño</strong>: Paseo por la Plaza Porticada iluminada y subida a la Noria gigante panorámica sobre la bahía.<br>
                • <strong>16:05 h - 18:35 h</strong>: ♨️ <strong>Castilla Termal Balneario de Solares (Aguas a 34°C)</strong> (a solo 15 min de Santander):<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• 2h30 de máximo bienestar y relajación en agua caliente mineromedicinal para desconectar y entrar en calor en familia.<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• Piscina termal con cuellos de cisne para los adultos y acceso exclusivo al <strong>Balnea Infantil</strong>: piscina climatizada de baja profundidad con toboganes acuáticos y juegos para Marco.<br>
                • <strong>18:45 h - 19:45 h</strong>: 🏘️ <strong>Paseo Histórico por Liérganes</strong> (a solo 5 min de Solares): Puente Romano sobre el río Miera y merienda de chocolate caliente artesano con churros.<br>
                • <strong>20:20 h - 21:40 h</strong>: 🌙 <strong>Cena Familiar & Chimenea en la Casona</strong>: Vuelta a la casona rural, encendido de leña y descanso reparador sabiendo que el spa os ha dejado renovados.
              </p>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span style="background:#ECFDF5;color:#065F46;padding:3px 8px;border-radius:6px;font-size:0.75rem;font-weight:700;">⭐ Momento Marco: Dar de comer a los pingüinos y focas a un palmo, subir a la carabela pirata y chapotear en los toboganes de agua caliente del balneario</span>
              </div>
            </div>
          </div>

          <!-- DÍA 4 -->
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#059669;"></div>
            <div class="timeline-content">
              <span class="timeline-day" style="color:#059669;">DÍA 4 · MARTES 8 DE DICIEMBRE · CABÁRCENO SAFARI 1ª HORA & RETORNO DIRECTO A QUER</span>
              <h3 style="margin: 4px 0 10px 0; font-size: 1.15rem; color: #0F172A;">Check-out Casona, Cabárceno Safari en Volvo XC60 (Apertura 09:30 h), Teleférico + Rapaces, Almuerzo Cántabro & Vuelta Directa por A-67 con Luz de Tarde</h3>
              <p style="font-size: 0.9rem; color: #475569; line-height: 1.5; margin-bottom: 12px;">
                • <strong>08:30 h - 09:15 h</strong>: ☕ <strong>Desayuno de Despedida y Check-out Cómodo</strong>: Carga final del equipaje en el maletero del Volvo XC60 y salida hacia Cabárceno (25 min por autovía A-8).<br>
                • <strong>09:45 h - 12:15 h</strong>: 🦁 <strong>Jornada Safari en Cabárceno a Primera Hora en Volvo XC60</strong>:<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• <strong>Apertura de Taquillas a las 09:30 h</strong>: Llegada a primera hora sin aglomeraciones. Recorrido safari en nuestro propio coche viendo de cerca elefantes africanos, osos pardos, jirafas y rinocerontes en semilibertad.<br>
                • <strong>12:20 h - 13:50 h</strong>: 🚡 <strong>Teleférico Panorámico & Exhibición de Vuelo de Aves Rapaces</strong>:<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• Vuelo en cabinas cerradas sobrevolando a vista de pájaro los valles kársticos de arcilla roja y los recintos de animales salvajes.<br>
                &nbsp;&nbsp;&nbsp;&nbsp;• Exhibición oficial de técnicas de vuelo de aves rapaces en la campa (águilas, halcones y buitres volando a escasos metros) y paseo junto al recinto de leones marinos.<br>
                • <strong>14:05 h - 15:20 h</strong>: 🍲 <strong>Comida / Almuerzo Cántabro de Despedida</strong>: Almuerzo casero tradicional en restaurante familiar junto a Cabárceno para salir con el estómago lleno.<br>
                • <strong>15:30 h - 19:15 h</strong>: 🚗 <strong>Retorno Directo en Volvo XC60 a Quer (Guadalajara)</strong>: Salida directa desde Penagos / Cabárceno hacia la autovía A-67 hacia el sur sin tener que pasar por Santander ni desviarse. Conexión rápida por Reinosa, Aguilar de Campoo, Burgos y A-1 hacia Quer (375 km, 3h 45m). Marco duerme plácidamente la siesta en el coche.<br>
                • <strong>19:15 h - 20:30 h</strong>: 🏠 <strong>Llegada a Casa en Quer con Luz de Tarde & Cena Tranquila</strong>: Llegada antes de anochecer, tiempo de sobra para deshacer maletas, duchar a Marco, cenar tranquilos en casa y descanso total antes de la vuelta al colegio del miércoles.
              </p>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span style="background:#FEF3C7;color:#B45309;padding:3px 8px;border-radius:6px;font-size:0.75rem;font-weight:700;">⭐ Momento Marco: Volar en el teleférico sobre los osos pardos, ver de cerca a los elefantes y llegar a casa a tiempo para cenar tranquilo</span>
              </div>
            </div>
          </div>

        </div>
      </section>

      """

content = content[:tl_idx_start] + new_timeline_html + content[tl_idx_end:]

# 4. Update Dataset OUTLOOK_ACTIVITIES, CONFIG & DEFAULTS
js_marker_start = "// 2. MASTER DATASET DE ACTIVIDADES (CANTABRIA & GRANADA)"
js_marker_end = "// Funciones auxiliares de formateo de tiempo"

js_idx_start = content.find(js_marker_start)
js_idx_end = content.find(js_marker_end, js_idx_start)

if js_idx_start == -1 or js_idx_end == -1:
    print("ERROR: JS markers not found!")
    sys.exit(1)

new_js_dataset = """// 2. MASTER DATASET DE ACTIVIDADES (CANTABRIA & GRANADA)
    const OUTLOOK_ACTIVITIES = {
      // -----------------------------------------------------------------------
      // CANTABRIA (Cabárceno el Último Día + Balneario el Lunes + Retorno 19:15h)
      // -----------------------------------------------------------------------
      // DÍA 1 (SÁBADO 5 DIC)
      ct_salida_quer: {
        id: "ct_salida_quer",
        dest: "cantabria",
        name: "🚗 Salida Cómoda de Quer en Volvo XC60",
        cat: "🚗 Ruta Volvo",
        color: "#0284C7",
        duration: 45,
        travel: 0,
        buffer: 10,
        loc: "Quer (Guadalajara)",
        price: "0 € peajes",
        img: "img_cantabria/casona_saja_cabezon.jpg",
        desc: "Salida a las 07:45 h desde Quer por N-320 y A-1. Marco sale desayunado y viaja descansado."
      },
      ct_secuoyas: {
        id: "ct_secuoyas",
        dest: "cantabria",
        name: "🌲 Bosque de Secuoyas Gigantes de Monte Corona",
        cat: "🌲 Naturaleza",
        color: "#059669",
        duration: 75,
        travel: 225, // 3h 45m viaje directo Quer-Cabezón por A-1 y A-67
        buffer: 10,
        loc: "Cabezón de la Sal",
        price: "100% GRATIS",
        img: "img_cantabria/secuoyas_cantabria.jpg",
        desc: "Pasarelas llanas de madera entre 848 secuoyas gigantes de más de 40 metros de altura 100% accesibles para Marco tras el viaje."
      },
      ct_cocido_montanes: {
        id: "ct_cocido_montanes",
        dest: "cantabria",
        name: "🥘 Comida: Cazuela de Cocido Montañés en Valle del Saja",
        cat: "🍲 Comida / Almuerzo",
        color: "#D97706",
        duration: 90,
        travel: 15,
        buffer: 10,
        loc: "Valle del Saja",
        price: "18 € ad · 8 € ni",
        img: "img_cantabria/cocido_montanes.jpg",
        desc: "Almuerzo tradicional montañés con alubia blanca fina, berza y compango artesano en mesón con chimenea (Casa Cofiño o El Jardín)."
      },
      ct_checkin_casona: {
        id: "ct_checkin_casona",
        dest: "cantabria",
        name: "🏡 Check-in Casona & Siesta de Marco al Fuego",
        cat: "🏡 Relax Familiar",
        color: "#0D9488",
        duration: 90,
        travel: 15,
        buffer: 10,
        loc: "Casona del Saja",
        price: "Incluido",
        img: "img_cantabria/casona_saja_cabezon.jpg",
        desc: "Check-in en la casona montañesa independiente con chimenea, desempaque de maletas y siesta reparadora de Marco."
      },
      ct_cartes: {
        id: "ct_cartes",
        dest: "cantabria",
        name: "🎄 Poblado Navideño de Cartes, Árbol 65m & Papá Noel",
        cat: "🎅 Navidad Mágica",
        color: "#DC2626",
        duration: 150,
        travel: 15,
        buffer: 10,
        loc: "Cartes",
        price: "100% GRATIS",
        img: "img_cantabria/cartes_poblado_navideno.jpg",
        desc: "Pueblo medieval de cuento iluminado al anochecer, soldados cascanueces y entrega de carta en mano a Papá Noel."
      },
      ct_cena_d1: {
        id: "ct_cena_d1",
        dest: "cantabria",
        name: "🌙 Cena Familiar & Chimenea de Leña",
        cat: "🌙 Cena",
        color: "#475569",
        duration: 80,
        travel: 15,
        buffer: 0,
        loc: "Casona del Saja",
        price: "Cocina propia",
        img: "img_cantabria/casona_saja_cabezon.jpg",
        desc: "Cena reconfortante al calor del fuego en la casona rural tras una primera jornada perfecta."
      },

      // DÍA 2 (DOMINGO 6 DIC)
      ct_desayuno_d2: {
        id: "ct_desayuno_d2",
        dest: "cantabria",
        name: "☕ Desayuno Energético de Montaña",
        cat: "☕ Desayuno",
        color: "#D97706",
        duration: 45,
        travel: 0,
        buffer: 10,
        loc: "Casona del Saja",
        price: "Incluido casona",
        img: "img_cantabria/santillana_del_mar.jpg",
        desc: "Sobaos pasiegos artesanos y café caliente para salir temprano hacia el Valle de Liébana."
      },
      ct_fuente_de: {
        id: "ct_fuente_de",
        dest: "cantabria",
        name: "🚠 Teleférico Fuente Dé Picos de Europa (1.823m con Nieve)",
        cat: "🏔️ Alta Montaña",
        color: "#0284C7",
        duration: 165,
        travel: 65, // Ruta por Desfiladero La Hermida a Fuente Dé
        buffer: 10,
        loc: "Fuente Dé (Camaleño)",
        price: "19 € ad · 7 € ni",
        img: "img_cantabria/fuente_de_picos.jpg",
        desc: "Ruta por el Desfiladero de La Hermida, subida vertical salvando 753m y juego seguro en la nieve para Marco."
      },
      ct_cocido_lebaniego: {
        id: "ct_cocido_lebaniego",
        dest: "cantabria",
        name: "🍲 Comida: Gran Cocido Lebaniego en Potes",
        cat: "🍲 Comida / Almuerzo",
        color: "#D97706",
        duration: 120,
        travel: 20,
        buffer: 10,
        loc: "Potes",
        price: "22 € ad · 9 € ni",
        img: "img_cantabria/cocido_montanes.jpg",
        desc: "Gran almuerzo de gala en mesón de Potes: sopa de fideos, garbanzos finos de Liébana, relleno de miga y compango."
      },
      ct_soplao: {
        id: "ct_soplao",
        dest: "cantabria",
        name: "🚂 Cueva de El Soplao en Tren Minero Subterráneo",
        cat: "🚂 Aventura Subterránea",
        color: "#6D28D9",
        duration: 90,
        travel: 40,
        buffer: 10,
        loc: "Rábago / Celis",
        price: "14 € ad · 10.5 € ni",
        img: "img_cantabria/el_soplao_tren.jpg",
        desc: "Viaje en tren minero subterráneo hasta la 'Capilla Sixtina' de las estalagmitas excéntricas del mundo."
      },
      ct_santillana: {
        id: "ct_santillana",
        dest: "cantabria",
        name: "🏘️ Villa Medieval de Santillana del Mar Iluminada",
        cat: "🏰 Villa Medieval",
        color: "#0D9488",
        duration: 85,
        travel: 25,
        buffer: 10,
        loc: "Santillana del Mar",
        price: "100% GRATIS",
        img: "img_cantabria/santillana_del_mar.jpg",
        desc: "Calles empedradas peatonales sin coches, Colegiata románica iluminada y degustación de sobaos calientes."
      },
      ct_cena_d2: {
        id: "ct_cena_d2",
        dest: "cantabria",
        name: "🌙 Cena Cántabra & Tertulia Familiar",
        cat: "🌙 Cena",
        color: "#475569",
        duration: 80,
        travel: 20,
        buffer: 0,
        loc: "Casona del Saja",
        price: "Cocina propia",
        img: "img_cantabria/cocido_montanes.jpg",
        desc: "Cena reconfortante en la casona con quesucos de Liébana y descanso temprano al calor de la leña."
      },

      // DÍA 3 (LUNES 7 DIC)
      ct_desayuno_d3: {
        id: "ct_desayuno_d3",
        dest: "cantabria",
        name: "☕ Desayuno en Casona & Salida a Santander",
        cat: "☕ Desayuno",
        color: "#D97706",
        duration: 45,
        travel: 0,
        buffer: 10,
        loc: "Casona del Saja",
        price: "Incluido casona",
        img: "img_cantabria/santillana_del_mar.jpg",
        desc: "Desayuno en la casona con sobaos pasiegos antes de salir hacia la costa de Santander."
      },
      ct_magdalena: {
        id: "ct_magdalena",
        dest: "cantabria",
        name: "🐬 Península de La Magdalena (Pingüinos, Focas & Carabelas 100% Gratis)",
        cat: "🐬 Fauna Marina",
        color: "#0284C7",
        duration: 165,
        travel: 35, // Trayecto a Santander Magdalena
        buffer: 10,
        loc: "Santander (Magdalena)",
        price: "100% GRATIS",
        img: "img_cantabria/magdalena_pinguinos.jpg",
        desc: "Piscinas naturales en acantilados con pingüinos, focas y leones marinos gratis, más las 3 carabelas piratas de Vital Alsar."
      },
      ct_almuerzo_santander: {
        id: "ct_almuerzo_santander",
        dest: "cantabria",
        name: "🐟 Comida: Rabas del Cantábrico en la Bahía de Santander",
        cat: "🍲 Comida / Almuerzo",
        color: "#D97706",
        duration: 90,
        travel: 10,
        buffer: 10,
        loc: "Santander (Puerto Chico)",
        price: "18 € ad · 8 € ni",
        img: "img_cantabria/cocido_montanes.jpg",
        desc: "Almuerzo marinero de rabas frescas de calamar y pescado del Cantábrico frente a la bahía en Puerto Chico."
      },
      ct_santander_navidad: {
        id: "ct_santander_navidad",
        dest: "cantabria",
        name: "⛸️ Santander Navideño: Noria Gigante Panorámica & Luces",
        cat: "⛸️ Luces Bahía",
        color: "#6D28D9",
        duration: 60,
        travel: 10,
        buffer: 10,
        loc: "Santander Centro",
        price: "5 € noria · Mercadillo gratis",
        img: "img_cantabria/santander_noria_navidad.jpg",
        desc: "Paseo por la Plaza Porticada iluminada con pista de hielo y subida a la Noria Gigante panorámica sobre la bahía."
      },
      ct_solares: {
        id: "ct_solares",
        dest: "cantabria",
        name: "♨️ Castilla Termal Balneario Solares (34°C + Balnea Infantil)",
        cat: "♨️ Termalismo Infantil",
        color: "#7C3AED",
        duration: 150,
        travel: 15, // 15 min de Santander a Solares
        buffer: 10,
        loc: "Solares",
        price: "35 € ad · 15 € ni",
        img: "img_cantabria/balneario_solares_termal.jpg",
        desc: "Aguas termales calientes a 34°C: piscina termal con chorros para adultos y Balnea Infantil con toboganes para Marco."
      },
      ct_lierganes: {
        id: "ct_lierganes",
        dest: "cantabria",
        name: "🏘️ Liérganes Histórico & Chocolate con Churros",
        cat: "🏰 Villa Monumental",
        color: "#2563EB",
        duration: 60,
        travel: 5,
        buffer: 15,
        loc: "Liérganes",
        price: "4 € merienda",
        img: "img_cantabria/posada_lierganes_rural.jpg",
        desc: "Paseo por el Puente Romano de Liérganes, leyenda del Hombre Pez y merienda de chocolate caliente con churros."
      },
      ct_cena_d3: {
        id: "ct_cena_d3",
        dest: "cantabria",
        name: "🌙 Cena Familiar & Chimenea de Leña",
        cat: "🌙 Cena",
        color: "#475569",
        duration: 80,
        travel: 25, // Trayecto a la casona
        buffer: 0,
        loc: "Casona del Saja",
        price: "Cocina propia",
        img: "img_cantabria/casona_saja_cabezon.jpg",
        desc: "Cena reconfortante al calor del fuego tras una tarde de máximo relax en las aguas calientes del balneario."
      },

      // DÍA 4 (MARTES 8 DIC)
      ct_desayuno_d4: {
        id: "ct_desayuno_d4",
        dest: "cantabria",
        name: "☕ Desayuno de Despedida & Check-out Casona",
        cat: "☕ Desayuno",
        color: "#D97706",
        duration: 45,
        travel: 0,
        buffer: 10,
        loc: "Casona del Saja",
        price: "Incluido casona",
        img: "img_cantabria/casona_saja_cabezon.jpg",
        desc: "Desayuno, carga final del equipaje en el maletero del Volvo XC60 y salida hacia Cabárceno por autovía A-8."
      },
      ct_cabarceno_safari: {
        id: "ct_cabarceno_safari",
        dest: "cantabria",
        name: "🦁 Cabárceno Safari en Volvo XC60 (Apertura 09:30 h)",
        cat: "🦁 Safari Volvo",
        color: "#059669",
        duration: 150,
        travel: 25, // 25 min desde la casona a Cabárceno
        buffer: 10,
        loc: "Cabárceno",
        price: "25 € ad · 15 € ni",
        img: "img_cantabria/cabarceno_elefantes.jpg",
        desc: "¡Entrada directa a las 09:30 h! Primeros coches en entrar al recinto con animales activos: osos, elefantes y jirafas."
      },
      ct_teleferico_cabarceno: {
        id: "ct_teleferico_cabarceno",
        dest: "cantabria",
        name: "🚡 Teleférico de Cabárceno & Aves Rapaces",
        cat: "🚡 Vuelo Aéreo",
        color: "#0D9488",
        duration: 90,
        travel: 0,
        buffer: 10,
        loc: "Cabárceno",
        price: "Incluido en entrada",
        img: "img_cantabria/teleferico_cabarceno.jpg",
        desc: "Vuelo en cabina sobrevolando los valles kársticos (desde 11:00 h) y exhibición didáctica de rapaces a las 12:00 h."
      },
      ct_almuerzo_cabarceno: {
        id: "ct_almuerzo_cabarceno",
        dest: "cantabria",
        name: "🍲 Comida: Almuerzo Cántabro de Despedida",
        cat: "🍲 Comida / Almuerzo",
        color: "#D97706",
        duration: 75,
        travel: 10,
        buffer: 10,
        loc: "Penagos / Cabárceno",
        price: "16 € ad · 8 € ni",
        img: "img_cantabria/cocido_montanes.jpg",
        desc: "Almuerzo tradicional en restaurante familiar junto al parque antes de iniciar el viaje de regreso."
      },
      ct_retorno_quer: {
        id: "ct_retorno_quer",
        dest: "cantabria",
        name: "🚗 Retorno en Volvo XC60 a Quer con Luz de Tarde",
        cat: "🌙 Retorno & Cena",
        color: "#475569",
        duration: 75,
        travel: 225, // 3h 45m viaje directo por A-67 hacia el sur
        buffer: 0,
        loc: "Quer (Guadalajara)",
        price: "En casa",
        img: "img_cantabria/casona_saja_cabezon.jpg",
        desc: "Salida a las 15:30 h por la A-67 hacia el sur sin entrar en Santander. Llegada a Quer a las 19:15 h para cenar tranquilos."
      },

      // -----------------------------------------------------------------------
      // GRANADA (Actividades + Pausas de Desayuno, Almuerzo y Cena)
      // -----------------------------------------------------------------------
      // DÍA 1
      gr_desayuno_d1: {
        id: "gr_desayuno_d1",
        dest: "granada",
        name: "☕ Desayuno & Salida a Granada en Volvo XC60",
        cat: "☕ Desayuno",
        color: "#D97706",
        duration: 45,
        travel: 0,
        buffer: 10,
        loc: "Alcalá de Henares",
        price: "En casa / Ruta",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Desayuno en familia, carga del Volvo XC60 y salida por autovía A-4 hacia Despeñaperros y Granada."
      },
      gr_tapeo_bibrambla: {
        id: "gr_tapeo_bibrambla",
        dest: "granada",
        name: "🍲 Comida: Tapeo Tradicional en Plaza Bib-Rambla",
        cat: "🍲 Comida / Almuerzo",
        color: "#D97706",
        duration: 90,
        travel: 255, // 4h 15m viaje desde Alcalá
        buffer: 10,
        loc: "Plaza Bib-Rambla",
        price: "15 € ad · 8 € ni",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Almuerzo de bienvenida a base de tapas auténticas granadinas (tapa gratis con cada consumición)."
      },
      gr_tiovivo_navidad: {
        id: "gr_tiovivo_navidad",
        dest: "granada",
        name: "🎠 Tiovivo Clásico & Encendido Navideño",
        cat: "🎅 Navidad Mágica",
        color: "#DC2626",
        duration: 60,
        travel: 15,
        buffer: 10,
        loc: "Plaza del Carmen",
        price: "3.5 € tiovivo",
        img: "img_granada/navidad_bibrambla_luces.jpg",
        desc: "Paseo por el árbol de luces gigantes y carrusel veneciano clásico de dos pisos para Marco."
      },
      gr_poblado_salon: {
        id: "gr_poblado_salon",
        dest: "granada",
        name: "⛸️ Poblado Navideño Paseo del Salón & Hielo",
        cat: "🎅 Navidad Mágica",
        color: "#D97706",
        duration: 120,
        travel: 15,
        buffer: 10,
        loc: "Paseo del Salón",
        price: "Pista 6 €",
        img: "img_granada/navidad_bibrambla_luces.jpg",
        desc: "Pista de hielo infantil, tirolina navideña, tobogán de trineos y castañeros tradicionales junto al río Genil."
      },
      gr_cena_d1: {
        id: "gr_cena_d1",
        dest: "granada",
        name: "🌙 Cena Ligera en el Apartamento / Carmen",
        cat: "🌙 Cena",
        color: "#475569",
        duration: 75,
        travel: 20,
        buffer: 0,
        loc: "Albaicín / Centro",
        price: "Cocina propia",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Cena tranquila en el alojamiento y descanso reparador para empezar el domingo con fuerza."
      },

      // DÍA 2
      gr_desayuno_d2: {
        id: "gr_desayuno_d2",
        dest: "granada",
        name: "☕ Desayuno Andaluz: Pan con Tomate & Aceite",
        cat: "☕ Desayuno",
        color: "#D97706",
        duration: 45,
        travel: 0,
        buffer: 10,
        loc: "Alojamiento / Cafetería",
        price: "Incluido / 3.5 €",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Tostadas de pan con aceite de oliva virgen extra y tomate rallado con zumo de naranja natural."
      },
      gr_alhambra: {
        id: "gr_alhambra",
        dest: "granada",
        name: "👑 La Alhambra & Palacios Nazaríes",
        cat: "🏛️ Monumento UNESCO",
        color: "#D97706",
        duration: 180,
        travel: 25,
        buffer: 10,
        loc: "La Alhambra",
        price: "19.09 € ad · 0 € ni",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Patio de los Leones, fuentes de agua que fascinan a Marco y jardines del Generalife sin escaleras empinadas."
      },
      gr_almuerzo_alhambra: {
        id: "gr_almuerzo_alhambra",
        dest: "granada",
        name: "🍲 Comida: Almuerzo Granadino Tradicional",
        cat: "🍲 Comida / Almuerzo",
        color: "#D97706",
        duration: 90,
        travel: 15,
        buffer: 10,
        loc: "Cuesta de Gomérez",
        price: "16 € ad · 8 € ni",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Almuerzo reconfortante de habas con jamón, plato alpujarreño o fritura andaluza en mesón tradicional."
      },
      gr_carmen_martires: {
        id: "gr_carmen_martires",
        dest: "granada",
        name: "🌳 Carmen de los Mártires & Jardines",
        cat: "🌲 Jardín Romántico",
        color: "#059669",
        duration: 60,
        travel: 15,
        buffer: 10,
        loc: "Colina de la Alhambra",
        price: "100% GRATIS",
        img: "img_granada/carmen_martires_jardines.jpg",
        desc: "Paseo llano entre pavos reales sueltos, estanque con patos y lago con torreón de cuento."
      },
      gr_albaicin_nicolas: {
        id: "gr_albaicin_nicolas",
        dest: "granada",
        name: "🌇 Mirador de San Nicolás al Atardecer",
        cat: "📸 Mirador Alhambra",
        color: "#2563EB",
        duration: 90,
        travel: 20,
        buffer: 10,
        loc: "Albaicín Alto",
        price: "100% GRATIS",
        img: "img_granada/mirador_san_nicolas.jpg",
        desc: "La puesta de sol más famosa del mundo con música flamenca en vivo y la Alhambra tiñéndose de rojo."
      },
      gr_cena_d2: {
        id: "gr_cena_d2",
        dest: "granada",
        name: "🌙 Cena de Tapeo en Plaza Nueva & Elvira",
        cat: "🌙 Cena",
        color: "#475569",
        duration: 75,
        travel: 15,
        buffer: 0,
        loc: "Plaza Nueva",
        price: "12 € ad · 6 € ni",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Tapeo tradicional en terrazas y mesones del bajo Albaicín antes de descansar."
      },

      // DÍA 3
      gr_desayuno_d3: {
        id: "gr_desayuno_d3",
        dest: "granada",
        name: "☕ Desayuno de Sierra con Vistas",
        cat: "☕ Desayuno",
        color: "#D97706",
        duration: 45,
        travel: 0,
        buffer: 10,
        loc: "Alojamiento",
        price: "Incluido",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Desayuno caliente para afrontar la jornada alpina en Sierra Nevada."
      },
      gr_sierra_nevada: {
        id: "gr_sierra_nevada",
        dest: "granada",
        name: "❄️ Trineos y Mirlo Blanco en Pradollano",
        cat: "❄️ Nieve Infantil",
        color: "#0284C7",
        duration: 150,
        travel: 50, // Subida a Pradollano A-395
        buffer: 10,
        loc: "Pradollano (2.100m)",
        price: "14 € parque infantil",
        img: "img_granada/sierra_nevada_mirlo_blanco.jpg",
        desc: "Parque de atracciones en la nieve: roscos hinchables, trineos con carril seguro y bici-esquís para Marco."
      },
      gr_telecabina: {
        id: "gr_telecabina",
        dest: "granada",
        name: "🚡 Subida en Telecabina Borreguiles (2.700m)",
        cat: "🚡 Alta Montaña",
        color: "#7C3AED",
        duration: 60,
        travel: 10,
        buffer: 10,
        loc: "Borreguiles",
        price: "19.5 € ad · 0 € ni",
        img: "img_granada/sierra_nevada_mirlo_blanco.jpg",
        desc: "Vistas panorámicas espectaculares del Veleta y el mar Mediterráneo en días claros."
      },
      gr_almuerzo_sierra: {
        id: "gr_almuerzo_sierra",
        dest: "granada",
        name: "🍲 Comida: Almuerzo Alpino en Pradollano",
        cat: "🍲 Comida / Almuerzo",
        color: "#D97706",
        duration: 90,
        travel: 15,
        buffer: 10,
        loc: "Pradollano",
        price: "18 € ad · 9 € ni",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Plato caliente de cuchara, migas alpujarreñas y carnes a la brasa en restaurante de montaña."
      },
      gr_teterias: {
        id: "gr_teterias",
        dest: "granada",
        name: "🫖 Tetería en Calle Calderería & Zoco",
        cat: "☕ Tradición Moruna",
        color: "#0D9488",
        duration: 75,
        travel: 45, // Bajada a Granada
        buffer: 10,
        loc: "Calle Calderería Nueva",
        price: "4.5 € té y dulce",
        img: "img_granada/teterias_caldereria.jpg",
        desc: "Té verde pakistaní con hierbabuena fresca, pastas árabes de pistacho y ambiente de las mil y una noches."
      },
      gr_cena_d3: {
        id: "gr_cena_d3",
        dest: "granada",
        name: "🌙 Cena Reconfortante en Granada",
        cat: "🌙 Cena",
        color: "#475569",
        duration: 75,
        travel: 15,
        buffer: 0,
        loc: "Granada Centro",
        price: "14 € ad · 7 € ni",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Cena en mesón andaluz y descanso relajado tras la jornada en la nieve."
      },

      // DÍA 4
      gr_desayuno_d4: {
        id: "gr_desayuno_d4",
        dest: "granada",
        name: "☕ Desayuno de Despedida & Check-out",
        cat: "☕ Desayuno",
        color: "#D97706",
        duration: 45,
        travel: 0,
        buffer: 10,
        loc: "Alojamiento",
        price: "Incluido",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Carga de equipaje en el Volvo XC60 y salida hacia el Parque de las Ciencias."
      },
      gr_ciencias_biodomo: {
        id: "gr_ciencias_biodomo",
        dest: "granada",
        name: "🔬 Parque de las Ciencias & Biodomo Tropical",
        cat: "🌿 Ciencia & Selva",
        color: "#059669",
        duration: 180,
        travel: 20,
        buffer: 10,
        loc: "Avenida de la Ciencia",
        price: "11 € ad · 9 € ni",
        img: "img_granada/parque_ciencias_biodomo.jpg",
        desc: "Inmersión en selva tropical real con tucanes, lémures a centímetros, tiburones y planetario interactivo."
      },
      gr_almuerzo_ciencias: {
        id: "gr_almuerzo_ciencias",
        dest: "granada",
        name: "🍲 Comida: Almuerzo en el Parque de las Ciencias",
        cat: "🍲 Comida / Almuerzo",
        color: "#D97706",
        duration: 75,
        travel: 10,
        buffer: 10,
        loc: "Restaurante del Parque",
        price: "14 € ad · 8 € ni",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Menú cómodo y completo en las instalaciones para no perder tiempo en desplazamientos."
      },
      gr_cahorros: {
        id: "gr_cahorros",
        dest: "granada",
        name: "🌉 Puentes Colgantes de Los Cahorros",
        cat: "🌲 Aventura Naturaleza",
        color: "#0284C7",
        duration: 105,
        travel: 25,
        buffer: 10,
        loc: "Monachil",
        price: "100% GRATIS",
        img: "img_granada/cahorros_monachil.jpg",
        desc: "Sendero llano junto al río pasando por el puente colgante de 63m entre paredes de piedra caliza."
      },
      gr_flamenco_sacromonte: {
        id: "gr_flamenco_sacromonte",
        dest: "granada",
        name: "💃 Cuevas de Sacromonte & Despedida",
        cat: "🎭 Folclore & Tradición",
        color: "#D97706",
        duration: 60,
        travel: 25,
        buffer: 15,
        loc: "Sacromonte",
        price: "100% GRATIS",
        img: "img_granada/sacromonte_cuevas.jpg",
        desc: "Paseo por las cuevas encaladas con chumberas antes de iniciar el viaje de vuelta."
      },
      gr_cena_retorno: {
        id: "gr_cena_retorno",
        dest: "granada",
        name: "🌙 Cena de Llegada a Casa en Alcalá",
        cat: "🌙 Cena",
        color: "#475569",
        duration: 60,
        travel: 255, // Retorno a Madrid
        buffer: 0,
        loc: "Alcalá de Henares",
        price: "En casa",
        img: "img_granada/alhambra_generalife.jpg",
        desc: "Llegada al hogar tras 4h 15m de viaje cómodo en el Volvo XC60. Marco duerme en ruta."
      }
    };

    // Configuración de Días por Destino (Horas de inicio y Resúmenes oficiales)
    const OUTLOOK_DAYS_CONFIG = {
      cantabria: {
        1: { name: "Día 1 · Sábado 5 Dic", dateStr: "2026-12-05", startMins: 7 * 60 + 45, summary: "Salida Quer 07:45h, Secuoyas 40m, Cocido Montañés, Casona y Cartes Navideño" },
        2: { name: "Día 2 · Domingo 6 Dic", dateStr: "2026-12-06", startMins: 8 * 60 + 0, summary: "Teleférico Fuente Dé (1.823m con Nieve), Cocido Lebaniego en Potes, El Soplao y Santillana" },
        3: { name: "Día 3 · Lunes 7 Dic", dateStr: "2026-12-07", startMins: 8 * 60 + 30, summary: "Santander Magdalena (Pingüinos & Carabelas gratis), Rabas, Balneario Solares 34°C y Liérganes" },
        4: { name: "Día 4 · Martes 8 Dic", dateStr: "2026-12-08", startMins: 8 * 60 + 30, summary: "Check-out, Cabárceno Safari 1ª hora (09:30h), Teleférico y Retorno por A-67 a Quer (19:15h)" }
      },
      granada: {
        1: { name: "Día 1 · Sábado 5 Dic", dateStr: "2026-12-05", startMins: 8 * 60 + 0, summary: "Salida Alcalá, Tapeo Bib-Rambla, Tiovivo y Encendido Navideño" },
        2: { name: "Día 2 · Domingo 6 Dic", dateStr: "2026-12-06", startMins: 8 * 60 + 30, summary: "Alhambra Nazarí, Almuerzo, Carmen Mártires y San Nicolás al Atardecer" },
        3: { name: "Día 3 · Lunes 7 Dic", dateStr: "2026-12-07", startMins: 8 * 60 + 30, summary: "Sierra Nevada Trineos Mirlo Blanco, Telecabina, Almuerzo y Teterías" },
        4: { name: "Día 4 · Martes 8 Dic", dateStr: "2026-12-08", startMins: 8 * 60 + 30, summary: "Parque Ciencias Biodomo, Almuerzo, Cahorros, Sacromonte y Retorno" }
      }
    };

    // Estado por defecto de actividades por día (Secuencia 100% Lógica con Desayunos, Comidas y Cenas)
    const OUTLOOK_DEFAULTS = {
      cantabria: {
        1: ['ct_salida_quer', 'ct_secuoyas', 'ct_cocido_montanes', 'ct_checkin_casona', 'ct_cartes', 'ct_cena_d1'],
        2: ['ct_desayuno_d2', 'ct_fuente_de', 'ct_cocido_lebaniego', 'ct_soplao', 'ct_santillana', 'ct_cena_d2'],
        3: ['ct_desayuno_d3', 'ct_magdalena', 'ct_almuerzo_santander', 'ct_santander_navidad', 'ct_solares', 'ct_lierganes', 'ct_cena_d3'],
        4: ['ct_desayuno_d4', 'ct_cabarceno_safari', 'ct_teleferico_cabarceno', 'ct_almuerzo_cabarceno', 'ct_retorno_quer']
      },
      granada: {
        1: ['gr_desayuno_d1', 'gr_tapeo_bibrambla', 'gr_tiovivo_navidad', 'gr_poblado_salon', 'gr_cena_d1'],
        2: ['gr_desayuno_d2', 'gr_alhambra', 'gr_almuerzo_alhambra', 'gr_carmen_martires', 'gr_albaicin_nicolas', 'gr_cena_d2'],
        3: ['gr_desayuno_d3', 'gr_sierra_nevada', 'gr_telecabina', 'gr_almuerzo_sierra', 'gr_teterias', 'gr_cena_d3'],
        4: ['gr_desayuno_d4', 'gr_ciencias_biodomo', 'gr_almuerzo_ciencias', 'gr_cahorros', 'gr_flamenco_sacromonte', 'gr_cena_retorno']
      }
    };

    window.outlookState = {
      cantabria: null,
      granada: null
    };

    // Versión del planificador para invalidar estados obsoletos
    const OUTLOOK_PLANNER_VERSION = "2026-11-01_v4_cabarceno_dia4_retorno_quer";

    function loadOutlookState(dest) {
      try {
        const savedVer = localStorage.getItem(`portal_viajes_planner_ver_${dest}`);
        if (savedVer === OUTLOOK_PLANNER_VERSION) {
          const saved = localStorage.getItem(`portal_viajes_planner_${dest}`);
          if (saved) {
            const parsed = JSON.parse(saved);
            if (parsed && parsed[1] && parsed[2] && parsed[3] && parsed[4]) {
              return parsed;
            }
          }
        }
      } catch (e) {
        console.warn("Could not load planner state for", dest, e);
      }
      try {
        localStorage.setItem(`portal_viajes_planner_ver_${dest}`, OUTLOOK_PLANNER_VERSION);
        localStorage.setItem(`portal_viajes_planner_${dest}`, JSON.stringify(OUTLOOK_DEFAULTS[dest]));
      } catch(e){}
      return JSON.parse(JSON.stringify(OUTLOOK_DEFAULTS[dest]));
    }

    """

content = content[:js_idx_start] + new_js_dataset + content[js_idx_end:]

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html with Cabárceno on Day 4 and Balneario on Day 3!")
