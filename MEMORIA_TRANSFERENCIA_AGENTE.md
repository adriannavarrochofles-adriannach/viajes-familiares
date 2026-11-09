# 🧠 MEMORIA MAESTRA DE TRANSFERENCIA OPERATIVA ENTRE AGENTES E IA
**Documento de Relevo Técnico, Contexto Integral, Estado del Sistema y Registro de Pendientes**
*Fecha de generación:* 9 de Noviembre de 2026 · 14:30 h  
*Destinatario:* Cualquier Agente de IA (Claude / Codex / Antigravity / ChatGPT / Subagentes) que tome el relevo de la sesión.

---

## 📌 1. PERFIL MAESTRO DEL USUARIO Y LA FAMILIA
* **Usuario Principal:** Adrián Navarro Chofles (`anavarro@autoelia.com`).
* **Núcleo Familiar / Grupo de Viaje Habitual:**
  - **4 Adultos + 1 Niño de 4 años (Marco):** Adrián, su pareja, otra pareja familiar (2 matrimonios/parejas) y el niño Marco (4 años).
  - En ocasiones, Adrián pide la cotización/configuración desdoblada tanto para **3 personas (2 adultos + Marco)** como para **5 personas (el grupo completo de 4 adultos + Marco)**.
* **Vehículo de Carretera:** Volvo XC60 familiar (usado para salidas terrestres y traslados al parking de larga estancia de Madrid-Barajas T1/T4).
* **Punto de Partida / Residencia:** Alcalá de Henares (Madrid) y Quer (Guadalajara).
* **Filosofía de Viaje:**
  - **"Bueno, Bonito y Barato" (BBB):** Sin trampas para turistas, máxima autenticidad, calidad y optimización del dinero.
  - **Gastronomía 100% Autóctona:** En España: sidrerías tradicionales, cocido montañés, tapeo leonés con tapa gratis, arroces marineros. En Italia: trattorias familiares en barrios no masificados (Cannaregio en Venecia, San Lorenzo y Oltrarno en Florencia), focaccias artesanas, heladerías de prestigio local (*Suso*, *Perché No!*), y el *Mercato Centrale*.
  - **Ritmo Adaptado a Niño de 4 Años (Marco):** Máximo 3 a 4,5 km diarios a pie, cero agobios, alicientes infantiles en cada parada (carruseles/tiovivos de época, trenes, parques, animales, barcos/vaporettos, fuentes de deseos), horarios de siesta protegidos y carritos/maletas en terrenos llanos sin escaleras innecesarias.
  - **Planes B Obligatorios:** Toda actividad exterior debe tener contingencia cubierta por si llueve o hay mal tiempo.

---

## 🏗️ 2. ARQUITECTURA TÉCNICA DEL PROYECTO
El proyecto principal gestionado en este entorno es el **Portal Web de Viajes Familiares**:

* **Directorio Raíz Local:**  
  `C:\Users\ANAVARRO\OneDrive - AUTO ELIA, S.A\PERSONALES\03_Viajes_y_Ocio\PORTAL_VIAJES_FAMILIARES`
* **Repositorio Remoto Git:**  
  `https://github.com/adriannavarrochofles-adriannach/viajes-familiares.git` (Rama activa: `main`).
* **Ficheros Nucleares del Sistema:**
  1. `index.html`: Aplicación web interactiva SPA (Single Page Application) multi-pestaña con selector de destinos (Cantabria, Asturias, Bilbao, Italia, Alsacia, Rumanía, etc.), calculadoras interactivas de presupuesto por persona/pareja, galerías fotográficas en lightbox y cronogramas hora a hora.
  2. `PORTAL_VIAJES_FAMILIARES_WHATSAPP.html`: Versión monolítica offline y portátil (~110 MB) que compila todas las 190 imágenes locales en base64 `data:image/...` para poder abrir el portal completo en móviles o sin conexión a internet.
  3. `BITACORA_VIAJES.md`: Diario de a bordo operativo histórico con más de 2.200 líneas donde se registran rigurosamente todos los cambios de rutas, precios, reservas y decisiones logísticas.
  4. `PENDIENTES.md`: Archivo obligatorio de control de tareas activas según la directiva del usuario (debe registrarse al iniciar y limpiarse al terminar).
  5. `scratch/run_compile_whatsapp_full.py`: Script en Python encargado de procesar `index.html`, codificar todas las imágenes relativas a Base64 e inyectarlas en el HTML offline.

---

## 🗺️ 3. DESTINOS TRABAJADOS Y ESTADO DE CADA VIAJE

### A. ITALIA: VENECIA, FLORENCIA Y PISA (DESTINO PRINCIPAL EN CURSO)
* **Evolución Histórica de las Fechas:**
  1. *Versión 1.0:* 1 al 4 de Enero de 2027.
  2. *Versión 2.0:* El usuario solicitó cambiar a **2 al 5 de Enero de 2027** para no viajar el 1 de enero tras la fiesta de Nochevieja.
  3. *Versión 3.0 ("Operación Cabalgata de Reyes"):* El usuario pidió adelantar el vuelo de vuelta del día 5 a mediodía (11:30 h – 12:30 h ➔ 14:00 h – 14:45 h en Barajas) para llegar a casa a las 15:30 h, comer tranquilos y asistir a la **Cabalgata de Reyes Magos de Alcalá de Henares (18:30 h con Marco)**. La excursión a la Torre Inclinada de Pisa se movió a la tarde del Lunes 4 en tren regional (50 min).
  4. *Versión 4.0 (Consulta Reciente):* El usuario ha solicitado estudiar mover todo el viaje del **26 al 30 de Diciembre de 2026** (5 días / 4 noches). Se demostró que es 100% viable, con ventajas enormes (pasan Nochebuena/Navidad en casa, Nochevieja/Año Nuevo en casa y Cabalgata en Alcalá, ganando 1 día y 1 noche extra en Italia).
* **Alojamientos Oficiales Fijados por Adrián en Booking:**
  - **Venecia Mestre:** *Dream Palace* (Via Sernaglia 29, a 400 m en llano de la estación Venezia Mestre). Apartamento de 2 dormitorios independientes + cocina. Cero puentes cargando maletas. Lanzadera a Venecia en 9 min (1,45 €).
  - **Florencia:** *San Lorenzo Wooden Loft* (Via San Zanobi 53, barrio San Lorenzo). Loft toscano rústico de 60 m² (1ª planta), 2 dormitorios + sofá cama y cocina. A 9 min a pie de la estación SMN y a 3 min del Mercato Centrale. 0 € en taxis.
* **Normativa y Desglose de Gastos Reales en Italia (¡Crítico!):**
  - **Tassa di Soggiorno Oficial:** En Venecia Mestre es 2,80 € / adulto / noche. En Florencia es 5,50 € / adulto / noche. **Marco (4 años) está 100% EXENTO por ley** (<10 años en Venecia, <12 años en Florencia).
  - **El "Coperto" en Trattorias:** Suplemento obligatorio italiano por pan y servicio de mesa (~2,50 € por adulto en comidas con mantel).
  - **Trenes:** El tren bala Frecciarossa aplica la tarifa familiar *Bimbi Gratis* (Marco viaja 100% gratis con plaza propia). En los trenes regionales toscanos a Pisa (9,80 € adulto), los menores de 4 años viajan gratis.
  - **Parking AENA Barajas:** Reserva de larga estancia para el Volvo XC60 (~32 € para 4 días / ~40 € para 5 días).

### B. CANTABRIA: PUENTE DE DICIEMBRE (5 AL 8 DICIEMBRE 2026)
* **Base Oficial:** *El Molino de Mateo* (Solares). Casa independiente de 94 m², 3 dormitorios, jardín vallado y barbacoa, a 4 min del Balneario de Solares y 10 min de Cabárceno.
* **Hitos del Itinerario Aprobado:**
  - Cueva El Soplao con tren minero subterráneo.
  - Museo y Neocueva de Altamira (¡gratis los sábados por la tarde!).
  - Bosque de Secuoyas de Cabezón de la Sal.
  - Tarde completa en las piscinas termales del **Balneario de Solares** (piscina a 34°C + zona infantil Balnea).
  - Safari de día completo en el **Parque de la Naturaleza de Cabárceno** con el Volvo XC60 + teleférico panorámico.
  - Costa Oriental (Santoña, Túnel de La Atalaya en Laredo, Castillo de Castro-Urdiales).
  - Pueblos navideños nocturnos: Poblado Navideño de Cartes (árbol de 65m y casa de Papá Noel), Santander iluminado (pista de hielo, tobogán de trineos).
  - Todas las cenas relajadas en casa con barbacoa en El Molino de Mateo.

### C. ASTURIAS & LEÓN: PUENTE DEL PILAR (9 AL 12 OCTUBRE 2026)
* **Base Oficial:** Casa Rural La Espriella (Avín, Concejo de Onís). Chalet en planta baja con 3 dormitorios y 900 m² de jardín.
* **Itinerario:** Lagos de Covadonga (bus regulado), Ruta del Cares desde Caín de Valdeón, Funicular subterráneo de Bulnes, Cuevona de Cueves transitada en coche, Llanes y costa oriental, Fiordos de Riaño y tapeo tradicional en el Barrio Húmedo de León.

---

## 📊 4. TABLA COMPARATIVA DE PRESUPUESTOS (ITALIA)

| Configuración | Fechas | Duración | 3 Pax (2 Ad + Niño 4a) | 5 Pax (4 Ad + Niño 4a) | Estado |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Operación Cabalgata** *(Fijada en index.html)* | **2 al 5 Ene 2027** | 4 días / 3 noches | **~1.119 € total**<br>(~559 € / adulto) | **~1.741 € total**<br>(~348 € / cabeza · ~696 € / pareja) | **Publicada en Git y WhatsApps listos** |
| **Navidad / Fin de Año** *(Consultada hoy)* | **26 al 30 Dic 2026** | 5 días / 4 noches | **~1.360 € – 1.480 €**<br>(~680 € / adulto) | **~2.070 € – 2.260 €**<br>(~415 € / cabeza · ~830 € / pareja) | **Analizada y presentada al usuario** |

---

## 📂 5. ARCHIVOS Y ARTEFACTOS CLAVE DISPONIBLES EN DISCO
1. `PORTAL_VIAJES_FAMILIARES/index.html`: Portal principal con toda la lógica de cálculo, cronogramas y pestañas.
2. `PORTAL_VIAJES_FAMILIARES/BITACORA_VIAJES.md`: Historial exhaustivo de decisiones y bitácora maestra.
3. `PORTAL_VIAJES_FAMILIARES/PENDIENTES.md`: Registro de tareas en curso del proyecto.
4. `MENSAJE_WHATSAPP_ITALIA_3PAX_CABALGATA.txt`: Mensaje cerrado listo para copiar/pegar para 2 adultos + Marco (Enero 2027).
5. `MENSAJE_WHATSAPP_ITALIA_5PAX_CABALGATA.txt`: Mensaje cerrado listo para copiar/pegar para 4 adultos + Marco (Enero 2027).
6. `PORTAL_VIAJES_FAMILIARES_WHATSAPP.html`: Versión offline de 110 MB con 190 imágenes incrustadas.
7. `ADMINISTRACION\IA\REGISTRO_AGENTES.md`: Archivo de sincronización con Claude/Codex (área corporativa de Auto Elia: stock de coches, Motorflash, BBVA, etc.).

---

## ⚡ 6. ESTADO ACTUAL EXACTO Y QUÉ QUEDA PENDIENTE (NEXT STEPS)

### Estado Actual:
* La versión de **2 al 5 de Enero de 2027 ("Operación Cabalgata")** está 100% terminada, verificada visualmente con Playwright, compilada en la versión offline, guardada en los archivos de WhatsApp y subida al repositorio remoto (`origin/main`, commit `93fa5e0`).
* En el último turno (9 Noviembre 2026 13:21 h), Adrián preguntó:  
  *«tengo que cambiar del 26 al 30 de diciembre, el viaje a italia, se puede???»*
* Se ha realizado el estudio completo de viabilidad, confirmando que es totalmente viable y tiene la enorme ventaja de ser **5 días / 4 noches** sin colisionar con Nochebuena, Navidad, Nochevieja ni Reyes.
* Se le han facilitado los precios comparativos y los enlaces directos a Google Flights y Booking para 26–30 Dic.

### Tareas Pendientes para el Agente que continúe:
1. **Esperar la Decisión de Adrián:**
   - **Si Adrián confirma el cambio a 26–30 de Diciembre de 2026 (5 días / 4 noches):**
     * Actualizar `index.html` (cambiar fechas de cabecera en el tab de Italia a 26-30 Dic 2026, adaptar el timeline interactivo a los 5 días: 2 noches en Venecia Mestre + 2 noches en Florencia con Pisa el 29 dic).
     * Actualizar los precios base en las funciones JavaScript de cálculo de presupuestos de `index.html`.
     * Regenerar la versión offline monolítica ejecutando `python scratch/run_compile_whatsapp_full.py`.
     * Generar los nuevos ficheros de WhatsApp para 3 y 5 pax adaptados a las fechas navideñas.
     * Actualizar `BITACORA_VIAJES.md`, limpiar `PENDIENTES.md` y hacer `git commit` & `git push`.
   - **Si Adrián prefiere mantener del 2 al 5 de Enero de 2027:**
     * No hay que tocar el código ni la web, ya que la versión de enero con Operación Cabalgata está completamente terminada, probada y lista para su uso.
   - **Si pide una variante intermedia de 4 días en diciembre (ej. 26-29 dic o 27-30 dic):**
     * Adaptar la distribución a 3 noches (1 noche Mestre + 2 noches Florencia).

---

## 🚨 7. DIRECTIVAS Y NORMAS GLOBALES QUE DEBES CUMPLIR (OBLIGATORIO)
1. **Regla de PENDIENTES.md:**
   - Antes de realizar cualquier cambio, lee `PENDIENTES.md`.
   - Registra de inmediato la tarea antes de modificar código.
   - Al terminarla y verificarla con éxito, límpiala dejando el archivo como `*(Sin tareas pendientes activas)*`.
2. **Regla de Coordinación con Claude:**
   - Si tocas scripts que interactúen con bases de datos corporativas o ficheros de administración de Auto Elia, debes coordinarte mediante `ADMINISTRACION\IA\REGISTRO_AGENTES.md`. (Para el portal de viajes familiares personales, el trabajo se realiza en `PORTAL_VIAJES_FAMILIARES` y se registra en `BITACORA_VIAJES.md`).
3. **Estilo de Comunicación:**
   - Siempre respuestas concisas, estructuradas en Markdown de GitHub, con precios claros, desgloses honestos y enlaces clickables en formato `[texto](file:///ruta)` o `[web](https://...)`.
