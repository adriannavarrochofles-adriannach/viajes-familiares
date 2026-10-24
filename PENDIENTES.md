# PENDIENTES - PORTAL DE VIAJES FAMILIARES

*(No hay tareas pendientes en este momento. Todas las tareas previas han sido completadas, verificadas con pruebas automatizadas y desplegadas en producción).*

---
### Historial Reciente de Tareas Completadas:
- [x] **[2026-10-24] Despliegue del Master Plan Italia (Venecia, Florencia & Pisa) en Portal Web**:
  - Mapa de ruta visual interactivo de 7 etapas multidestino.
  - Selector interactivo de actividades con cálculo reactivo de costes y ahorro al descartar (Adultos vs Marco).
  - Vuelos de máximo aprovechamiento (08:35 h salida y 18:50 h regreso) con enlaces directos de búsqueda.
  - Hoteles familiares auditados en Booking.com (Mestre y Florencia centro con zona de juegos).
  - Timeline día a día hora por hora con galería fotográfica.
  - Standalone WhatsApp compilado y desplegado en GitHub / Render.
- [x] **[2026-10-20] Sistema de acceso, contraseña, registro abierto y privacidad estricta de fotos por usuario**:
  - Hashing de contraseñas y tokens HMAC-SHA256 en FastAPI (`app.py`).
  - Cuentas de familia precargadas (`adrian`, `maripaz`, `marco`) con acceso en 1 clic + registro abierto de nuevos usuarios.
  - Endpoints de fotos privadas y almacenamiento aislado (`user_uploads/{user_id}/`).
  - Pestaña "📸 Mis Fotos" y navegación táctil en App Móvil (`index.html`).
  - Galería responsive, subida con cámara móvil, visor Lightbox y compartir en WhatsApp.
  - Verificación 100% PASS en Playwright.
