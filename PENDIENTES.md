# PENDIENTES - PORTAL DE VIAJES FAMILIARES

*(No hay tareas pendientes en este momento. Todas las tareas previas han sido completadas, verificadas con pruebas automatizadas y desplegadas en producción).*

---
### Historial Reciente de Tareas Completadas:
- [x] **[2026-10-20] Sistema de acceso, contraseña, registro abierto y privacidad estricta de fotos por usuario**:
  - Hashing de contraseñas y tokens HMAC-SHA256 en FastAPI (`app.py`).
  - Cuentas de familia precargadas (`adrian`, `maripaz`, `marco`) con acceso en 1 clic + registro abierto de nuevos usuarios.
  - Endpoints de fotos privadas y almacenamiento aislado (`user_uploads/{user_id}/`).
  - Pestaña "📸 Mis Fotos" y navegación táctil en App Móvil (`index.html`).
  - Galería responsive, subida con cámara móvil, visor Lightbox y compartir en WhatsApp.
  - Verificación 100% PASS en Playwright (login, subida, aislamiento estricto de fotos entre usuarios).
  - Standalone WhatsApp compilado y desplegado en GitHub / Render.
