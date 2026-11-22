# BOT FACTORY AI — Memoria del proyecto

## Propósito
Construir una plataforma/fábrica de bots y agentes de automatización para crear, configurar, operar y administrar soluciones conectadas a Telegram, correo electrónico y WhatsApp.

## Objetivo de negocio
Desarrollar una empresa de creación e implementación de bots para clientes, con una plataforma reutilizable que permita ofrecer automatizaciones, asistentes y flujos personalizados.

## Canales objetivo
- Telegram: bots, comandos, notificaciones y conversaciones.
- Correo electrónico: recepción, clasificación, respuestas y notificaciones; integrar proveedores mediante APIs y SMTP seguro cuando corresponda.
- WhatsApp: integración mediante proveedores y APIs oficiales, respetando las políticas y permisos de cada plataforma.

## Decisiones técnicas vigentes
- Lenguaje principal: Python.
- Interfaz y panel de control: Streamlit.
- No utilizar FastAPI como base del proyecto.
- Arquitectura modular, con conectores independientes por canal.
- Supabase como plataforma de datos, autenticación y persistencia cuando corresponda.
- Redis para colas, caché o coordinación cuando sea necesario.
- Workers independientes para ejecutar tareas en segundo plano.
- Arquitectura multimodelo mediante adaptadores; considerar Claude y otros proveedores.
- GitHub es el repositorio oficial y control de versiones.

## Arquitectura
1. Aplicación Streamlit: panel administrativo y experiencia de configuración.
2. Núcleo BOT FACTORY: clientes, proyectos, bots, flujos, permisos y configuraciones.
3. Capa de conectores: Telegram, correo y WhatsApp, desacoplados.
4. Capa de IA: selección de proveedor/modelo, prompts, herramientas y políticas.
5. Persistencia: Supabase (PostgreSQL, Auth, Storage y RLS).
6. Procesamiento asíncrono: Redis + workers, incorporados según necesidad.
7. Observabilidad: logs, estados de ejecución, errores y auditoría.

## Principios
- Multiempresa/multicliente: separar datos, credenciales y configuraciones por cliente.
- Seguridad por diseño: mínimo privilegio, validación de entradas y auditoría.
- No almacenar secretos en el código ni en el repositorio.
- Usar variables de entorno y un archivo .env local excluido de Git.
- Incluir .env.example únicamente con nombres de variables y valores ficticios.
- Respetar términos, consentimiento, privacidad y límites de las APIs de cada canal.
- Mantener documentación actualizada y cambios versionados.

## Seguridad crítica
El repositorio es público. Nunca subir tokens de Telegram, credenciales SMTP, claves de WhatsApp, claves de Supabase, API keys de modelos, contraseñas ni datos reales de clientes. Si alguna credencial se expone, revocarla y generar otra.

## Estado de implementación
### Fundaciones
- [x] Estructura Python inicial.
- [x] Aplicación Streamlit inicial.
- [x] .gitignore y .env.example sin secretos.
- [x] Archivos de continuidad en la raíz.

### Telegram Bot Factory — MVP 0.1
- [x] Conector Telegram independiente.
- [x] Comandos /start, /help y /status.
- [x] Worker Python independiente del panel Streamlit.
- [x] Token leído desde TELEGRAM_BOT_TOKEN en entorno local.
- [x] Instrucciones de creación con @BotFather.
- [ ] Instalar dependencias y ejecutar pruebas locales.
- [ ] Conectar token real en entorno local (nunca compartirlo).
- [ ] Probar conversación real con el bot.

## Etapas siguientes
1. Validar el MVP Telegram localmente.
2. Integrar registro multiempresa y credenciales cifradas/secret manager.
3. Construir panel Streamlit para alta, configuración y monitoreo de bots.
4. Incorporar Supabase Auth, PostgreSQL y políticas RLS.
5. Agregar pruebas, logs, métricas y despliegue del worker.
6. Desarrollar conectores de correo y WhatsApp mediante APIs/proveedores oficiales.
7. Integrar agentes y proveedores de IA multimodelo.
8. Definir paquetes comerciales, onboarding y mantenimiento.

## Archivos de continuidad obligatorios
- memoria.md: decisiones, arquitectura, requisitos y contexto vigente.
- bitacora_acumulada.md: registro cronológico de avances, cambios y pendientes.
Actualizar ambos en cada sesión y conservar el historial de la bitácora.

## Repositorio
- URL: https://github.com/hernandezjxs-alt/BOT-FACTORY-IA
- Propietario: hernandezjxs-alt
- Rama principal: main
- Visibilidad: pública
