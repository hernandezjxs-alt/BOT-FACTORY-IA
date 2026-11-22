# BOT FACTORY AI — Bitácora acumulada

Registro cronológico de decisiones, avances, cambios y pendientes del proyecto.

## 2026-11-22 — Inicio de documentación y continuidad

### Objetivo confirmado
Crear una empresa/plataforma de desarrollo de bots y automatizaciones para Telegram, correo electrónico y WhatsApp.

### Repositorio
- URL: https://github.com/hernandezjxs-alt/BOT-FACTORY-IA
- Propietario: hernandezjxs-alt
- Rama: main
- Visibilidad: pública.
- Se requiere mantener toda la documentación de continuidad versionada en GitHub.

### Decisiones técnicas registradas
- Python como lenguaje principal.
- Streamlit para la interfaz y panel de control; no FastAPI.
- Supabase para datos y autenticación.
- Redis y workers independientes para tareas asíncronas, según necesidad.
- Arquitectura modular y conectores separados para Telegram, correo y WhatsApp.
- Arquitectura multimodelo; considerar Claude Pro y otros proveedores mediante adaptadores.

### Avance de esta sesión
- Se creó `memoria.md` en la raíz del repositorio.
- Se creó este archivo `bitacora_acumulada.md` en la raíz del repositorio.
- Ambos archivos quedan establecidos como respaldos obligatorios y acumulativos.

### Seguridad
El repositorio es público. No publicar tokens, contraseñas, API keys, credenciales, datos personales ni archivos .env. Usar variables de entorno y mantener un .env.example con valores ficticios.

### Pendientes inmediatos
1. Crear la estructura inicial de carpetas y módulos Python.
2. Incorporar README con descripción, instalación y configuración segura.
3. Añadir .gitignore y .env.example sin secretos.
4. Crear una primera aplicación Streamlit ejecutable.
5. Definir el esquema inicial de Supabase y la estrategia de autenticación.
6. Implementar y probar primero el conector de Telegram.
7. Diseñar después los conectores de correo y WhatsApp con APIs/proveedores autorizados.
8. Definir pruebas, logs, manejo de errores y separación de clientes.

### Regla para próximas sesiones
Actualizar memoria.md cuando cambien decisiones o requisitos. Agregar una nueva entrada fechada a bitacora_acumulada.md en cada sesión, sin borrar entradas anteriores.
