import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

INDEX_PATH = r"C:\Users\ANAVARRO\OneDrive - AUTO ELIA, S.A\PERSONALES\03_Viajes_y_Ocio\PORTAL_VIAJES_FAMILIARES\index.html"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# -----------------------------------------------------------------------------
# 1. ADD SMART BOOKING TIP BOX IN TAB-CANTABRIA (BEFORE hotel-carousel-nav-bar)
# -----------------------------------------------------------------------------
tip_box_html = """
        <!-- BANNER CONSEJO DE RESERVA INTELIGENTE: MARCO COLECHO -->
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(16, 185, 129, 0.12)); border: 1.5px solid rgba(245, 158, 11, 0.4); border-radius: 12px; padding: 14px 18px; margin-bottom: 18px; display: flex; align-items: flex-start; gap: 14px; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">
          <div style="font-size: 1.8rem; line-height: 1;">💡</div>
          <div style="font-size: 0.88rem; color: #1E293B; line-height: 1.5;">
            <strong style="color: #B45309; font-size: 0.96rem; display: block; margin-bottom: 4px;">CONSEJO DE RESERVA INTELIGENTE: Marco duerme con nosotros (Colecho)</strong>
            <span>Al dormir Marco (4 años) con vosotros en la cama de matrimonio, <strong>no tenéis que pagar por camas supletorias ni reservar chalets sobredimensionados</strong>:</span>
            <ul style="margin: 6px 0 6px 18px; padding: 0;">
              <li><strong>Si viajáis 5 (4 adultos + Marco)</strong>: Buscad casas o apartamentos para <strong>4 adultos (2 dormitorios dobles)</strong>. El algoritmo de Booking os mostrará el doble de opciones y ahorraréis entre <strong>80 € y 150 €</strong> respecto a casas de 3-4 habitaciones.</li>
              <li><strong>Si viajáis 3 (2 adultos + Marco)</strong>: Buscad directamente para <strong>2 adultos (1 habitación doble / apartamento 1 hab)</strong>. Ahorro directo de más de <strong>120 €</strong>.</li>
            </ul>
            <span style="font-size: 0.82rem; color: #475569;"><em>Nota legal y de registro:</em> El 95% de casas rurales en Cantabria alojan gratis a niños de 4 años en cama existente. Al reservar en Booking, indicad en comentarios: <code>"Viajamos con niño de 4 años que duerme en nuestra cama de matrimonio compartida"</code> para su registro oficial (DNI/Libro de Familia) a 0 € de suplemento.</span>
          </div>
        </div>
"""

nav_bar_target = '<div class="hotel-carousel-nav-bar">'
# Ensure we only insert once in Cantabria
ct_idx = content.find('id="tab-cantabria"')
nav_bar_idx = content.find(nav_bar_target, ct_idx)

if nav_bar_idx != -1 and "CONSEJO DE RESERVA INTELIGENTE: Marco duerme con nosotros" not in content:
    content = content[:nav_bar_idx] + tip_box_html + content[nav_bar_idx:]
    print("Added Smart Booking Tip Box in Cantabria tab!")
else:
    print("Tip box already exists or target not found.")

# -----------------------------------------------------------------------------
# 2. ADD ALTERNATIVES TO FUENTE DÉ IN TIMELINE (DAY 2 CANTABRIA)
# -----------------------------------------------------------------------------
fuente_de_target = '<span style="background:#DCFCE7;color:#166534;padding:3px 8px;border-radius:6px;font-size:0.75rem;font-weight:700;">⭐ Momento Marco: Subir en el teleférico sobre las nubes'

alternatives_box_html = """
              <!-- ALTERNATIVAS A FUENTE DÉ -->
              <div style="background: rgba(2, 132, 199, 0.08); border-left: 4px solid #0284C7; padding: 12px 14px; border-radius: 8px; margin-top: 14px; font-size: 0.86rem; color: #1E293B;">
                <strong style="color: #0369A1; font-size: 0.92rem; display: flex; align-items: center; gap: 6px;">
                  <span>🔄 ¿Alternativas a Fuente Dé? (Por mal tiempo, viento o si preferís no subir a alta montaña)</span>
                </strong>
                <p style="margin: 4px 0 8px 0; font-size: 0.83rem; color: #475569;">
                  Si el teleférico estuviera cerrado por rachas de viento, hubiera niebla cerrada en la cumbre, o preferís un día costero o techado sin curvas de desfiladero:
                </p>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                  <div style="background: #FFFFFF; padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(2, 132, 199, 0.2);">
                    <strong style="color: #0F172A;">🏰 Alternativa 1 (Costa y Fantasía de Gaudí · A 12 min sin curvas):</strong>
                    <span><strong>Comillas & El Capricho de Gaudí</strong>: Casa-castillo de cuento con girasoles de cerámica verde y amarilla, torre musical y cuevas en el jardín ideales para Marco. Enlaza con paseo señorial por el Palacio de Sobrellano y comida marinera en <strong>San Vicente de la Barquera</strong> (arroz caldoso de bogavante o marisco frente a las marismas de Oyambre).</span>
                  </div>
                  <div style="background: #FFFFFF; padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(2, 132, 199, 0.2);">
                    <strong style="color: #0F172A;">🦬 Alternativa 2 (Prehistoria 100% Techada y Climatizada · A 14 min):</strong>
                    <span><strong>Museo y Neocueva de Altamira (Santillana del Mar)</strong>: Réplica exacta a escala 1:1 de la cueva de los bisontes policromados, con talleres infantiles de fuego y pintura, museografía interactiva y cine 3D. 100% a cubierto y a 18°C constantes (perfecto si llueve o hace frío intenso).</span>
                  </div>
                  <div style="background: #FFFFFF; padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(2, 132, 199, 0.2);">
                    <strong style="color: #0F172A;">🌲 Alternativa 3 (Pueblo Rústico de Cuento & Bosque · A 25 min):</strong>
                    <span><strong>Bárcena Mayor & Parque Natural Saja-Besaya</strong>: El pueblo más antiguo y mejor conservado de Cantabria, 100% peatonal con calles empedradas, puentes sobre el río Argoza, vacas tudancas pastando libres y las mejores cazuelas de cocido montañés de caserío sin curvas pronunciadas.</span>
                  </div>
                </div>
              </div>
"""

tl_ct_idx = content.find('id="timeline-cantabria"')
fd_idx = content.find(fuente_de_target, tl_ct_idx)

if fd_idx != -1 and "¿Alternativas a Fuente Dé?" not in content:
    # insert before the Momento Marco span
    content = content[:fd_idx] + alternatives_box_html + "\n              " + content[fd_idx:]
    print("Added Alternatives to Fuente Dé in Cantabria Timeline!")
else:
    print("Alternatives already exist or target not found.")

# -----------------------------------------------------------------------------
# 3. ADD ALTERNATIVE ACTIVITIES IN OUTLOOK_ACTIVITIES['cantabria']
# -----------------------------------------------------------------------------
act_target = 'ct_fuente_de: {'
act_idx = content.find(act_target)

extra_acts = """      ct_gaudi_comillas: {
        id: "ct_gaudi_comillas",
        dest: "cantabria",
        name: "🏰 Alt: El Capricho de Gaudí & Comillas Señorial",
        cat: "🏰 Cultura / Costa",
        color: "#0D9488",
        duration: 120,
        travel: 15,
        buffer: 10,
        loc: "Comillas",
        price: "7 € ad · Gratis ni",
        img: "img_cantabria/santillana_medieval.jpg",
        desc: "Alternativa a Fuente Dé: Castillo modernista de Gaudí con girasoles de cerámica, cueva y torre musical, perfecto para Marco a solo 12 min."
      },
      ct_altamira: {
        id: "ct_altamira",
        dest: "cantabria",
        name: "🦬 Alt: Neocueva y Museo de Altamira (Techado)",
        cat: "🦬 Prehistoria",
        color: "#B45309",
        duration: 105,
        travel: 15,
        buffer: 10,
        loc: "Santillana del Mar",
        price: "3 € ad · Gratis ni",
        img: "img_cantabria/cueva_soplao.jpg",
        desc: "Alternativa techada a 18°C: Réplica 1:1 de la cueva de los bisontes con talleres infantiles y museografía interactiva."
      },
      """

if act_idx != -1 and "ct_gaudi_comillas:" not in content:
    content = content[:act_idx] + extra_acts + content[act_idx:]
    print("Added ct_gaudi_comillas and ct_altamira to OUTLOOK_ACTIVITIES!")
else:
    print("Extra activities already exist or target not found.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("index.html updated successfully!")
