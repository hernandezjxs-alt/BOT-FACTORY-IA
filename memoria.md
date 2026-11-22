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
- Diseñar una arquitectura multimodelo que permita integrar modelos de IA, considerando Claude (el usuario dispone de Claude Pro) y otros proveedores mediante adaptadores.
- GitHub es el repositorio oficial y control de versiones.

## Arquitectura inicial propuesta
1. Aplicación Streamlit: panel administrativo y experiencia de configuración.
2. Núcleo BOT FACTORY: registro de clientes, proyectos, bots, flujos, permisos y configuraciones.
3. Capa de conectores: Telegram, correo y WhatsApp, desacoplados entre sí.
4. Capa de IA: selección de proveedor/modelo, prompts, herramientas y políticas.
5. Persistencia: Supabase.
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
Este repositorio es público. Nunca subir tokens de Telegram, credenciales SMTP, claves de WhatsApp, claves de Supabase, API keys de modelos, contraseñas ni datos reales de clientes. Si alguna credencial se expone, revocarla y generar otra.

## Alcance de construcción por etapas
### Etapa 1 — Fundaciones
- Estructura Python modular.
- Documentación y configuración segura.
- Aplicación Streamlit inicial.
- Modelo de datos y configuración base.

### Etapa 2 — Primer canal funcional
- Integración inicial con Telegram.
- Registro de eventos, manejo de errores y pruebas.

### Etapa 3 — Correo
- Conector de correo entrante/saliente.
- Plantillas, clasificación y automatizaciones.

### Etapa 4 — WhatsApp
- Integración mediante API/proveedor oficial.
- Gestión de consentimiento, plantillas y estados.

### Etapa 5 — IA y automatizaciones
- Enrutamiento multimodelo.
- Flujos reutilizables, herramientas y workers.
- Métricas, límites por cliente y panel de administración.

### Etapa 6 — Oferta comercial
- Paquetes de implementación y mantenimiento.
- Onboarding de clientes, soporte, documentación y precios.
- Pilotos controlados antes de producción.

## Archivos de continuidad obligatorios
- memoria.md: decisiones, arquitectura, requisitos y contexto vigente.
- bitacora_acumulada.md: registro cronológico de avances, cambios y pendientes.

Ambos archivos deben actualizarse en cada sesión de trabajo y mantenerse en la raíz del repositorio.

## Estado inicial
- Repositorio: https://github.com/hernandezjxs-alt/BOT-FACTORY-IA
- Rama principal: main
- Visibilidad: pública
- Contenido inicial conocido: README.md
- Próximo objetivo: crear la estructura inicial del proyecto y validar que la integración GitHub tenga permisos de escritura.
