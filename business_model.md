# BOT FACTORY AI — Producto y modelo comercial

**Versión:** 1.0 · **Fecha:** 2026-11-22  
**Modelo:** híbrido SaaS + servicios profesionales.

## 1. Propuesta de valor
BOT FACTORY AI permite a empresas crear, conectar y administrar asistentes y automatizaciones con IA en Telegram, WhatsApp y correo electrónico. El producto combina autoservicio para clientes con implementación especializada para quienes necesitan soluciones a medida.

## 2. Dos líneas de negocio

### A. BOT FACTORY SaaS
El cliente crea una cuenta, registra su empresa, elige un plan, configura agentes y conecta canales desde un panel web. Puede administrar conversaciones, consumo, integraciones, usuarios y facturación según su plan.

### B. BOT FACTORY Studio
Servicio profesional para empresas que requieren diagnóstico, diseño de procesos, desarrollo de bots personalizados, integración con CRM/ERP, migración, capacitación, soporte y mantenimiento. Se cotiza según alcance y complejidad.

Ambas líneas utilizan el mismo núcleo técnico, conectores, motor de agentes y sistema de permisos. Un proyecto Studio puede convertirse en un espacio administrado dentro de SaaS, sin duplicar la plataforma.

## 3. Segmentos de clientes
- Emprendedores y profesionales: respuestas frecuentes, reservas, captación de prospectos y notificaciones.
- Pymes: atención multicanal, ventas, seguimiento y automatización administrativa.
- Empresas: flujos con aprobaciones, integración con sistemas internos, trazabilidad, roles y soporte especializado.
- Agencias/consultores: espacios separados para administrar bots de sus propios clientes (fase posterior).

## 4. Catálogo de soluciones
1. Atención al cliente: preguntas frecuentes, clasificación y derivación humana.
2. Ventas: captura y calificación de prospectos, cotizaciones y seguimiento.
3. Correo inteligente: clasificación, extracción de datos, borradores y respuestas sujetas a aprobación.
4. Notificaciones: alertas, recordatorios y avisos transaccionales.
5. Operaciones: recepción de solicitudes, creación de tickets y consulta de conocimiento.
6. Asistentes internos: búsqueda en documentos y ayuda a equipos.

## 5. Planes SaaS propuestos
Los siguientes valores son **hipótesis comerciales iniciales en CLP**, no precios de mercado verificados ni tarifas publicadas. Se validarán con clientes piloto, costos reales de infraestructura, consumo de IA y proveedores de mensajería.

| Plan | Precio mensual de prueba | Cliente objetivo | Alcance conceptual |
|---|---:|---|---|
| Starter | $14.990 | Profesional / microempresa | 1 espacio, 1 bot, 1 canal, límites de uso bajos |
| Pro | $39.990 | Pyme | Hasta 3 bots, 2 canales, métricas y plantillas |
| Business | $99.990 | Pyme en crecimiento | Hasta 10 bots, varios usuarios, roles básicos e historial ampliado |
| Enterprise | A cotizar | Empresa | Volumen, integraciones, controles y soporte acordados |

Condiciones comerciales por definir antes de cobrar:
- Cuotas de mensajes, ejecuciones y tokens por plan.
- Costos externos de WhatsApp, correo, modelos de IA y proveedores se transparentan y pueden cobrarse aparte.
- No ofrecer uso ilimitado.
- Definir política de excedentes, suspensión, cancelación, retención y exportación de datos.
- Los precios no incluyen desarrollos personalizados ni impuestos salvo que se indique expresamente.

## 6. Servicios BOT FACTORY Studio
- Diagnóstico y levantamiento de procesos.
- Diseño funcional y prototipo.
- Implementación de bots y agentes personalizados.
- Integración con CRM, ERP, bases de datos y APIs.
- Configuración de canales oficiales.
- Capacitación, documentación y acompañamiento.
- Soporte y mantenimiento mensual.

Cada propuesta debe incluir alcance, entregables, exclusiones, cronograma, criterios de aceptación, responsabilidades del cliente, costos de terceros y plan de soporte. No fijar tarifas hasta estimar horas, riesgos y costos externos.

## 7. Experiencia del cliente
1. Descubre soluciones y solicita demo o asesoría.
2. Se registra o agenda diagnóstico.
3. Crea una organización/espacio de trabajo.
4. Elige autoservicio SaaS o solicita implementación Studio.
5. Crea un bot desde una plantilla o recibe una solución configurada.
6. Conecta el canal con un onboarding seguro.
7. Prueba en entorno controlado y aprueba publicación.
8. Supervisa uso, resultados, costos y actividad desde el panel.
9. Solicita soporte, amplía el plan o contrata mejoras.

## 8. Roles y permisos
- Platform Owner: propietario global de BOT FACTORY AI.
- Platform Admin: soporte y operación interna con acceso auditado.
- Organization Owner: titular de la cuenta cliente.
- Organization Admin: administra usuarios, bots y configuración de su organización.
- Operator: revisa conversaciones y ejecuta tareas permitidas.
- Viewer: consulta paneles sin modificar recursos.

La selección visual de roles del prototipo actual no es seguridad real. La autorización deberá implementarse en backend con Supabase Auth, membresías y políticas RLS; las operaciones privilegiadas se ejecutarán en servicios confiables.

## 9. Arquitectura de producto
- Frontend/panel: Streamlit para el MVP; evaluar frontend dedicado cuando el producto y la experiencia multiusuario lo requieran.
- Identidad y datos: Supabase Auth + PostgreSQL + Row Level Security.
- Entidades principales: organizations, memberships, subscriptions, plans, bots, agents, channel_connections, conversations, messages, usage_events, deployments, audit_events, support_tickets.
- Secretos: almacenar referencias a secretos en la base; credenciales reales en un gestor de secretos o mecanismo seguro de despliegue, nunca en texto plano ni en repositorio.
- Ejecución: workers Python separados del proceso Streamlit; colas Redis cuando el volumen lo justifique.
- IA: interfaz común de proveedores, cuotas, límites y registro de consumo.
- Canales: conectores desacoplados; WhatsApp por API oficial/proveedor autorizado, correo mediante OAuth/API o SMTP seguro, Telegram mediante Bot API y onboarding con BotFather.

## 10. Principios de seguridad y cumplimiento
- Aislamiento de datos por organización desde el diseño.
- Mínimo privilegio, auditoría y gestión de sesiones.
- Consentimiento y respeto de políticas de cada canal.
- No enviar mensajes masivos no solicitados ni automatizar spam.
- Revisión humana para acciones sensibles, pagos, compromisos contractuales o respuestas de alto impacto.
- Retención limitada, exportación y eliminación de datos según política definida.
- No usar información confidencial de clientes con proveedores/modelos sin revisar términos, controles y acuerdos aplicables.

## 11. Métricas del negocio
- Activación: organizaciones que conectan su primer canal.
- Tiempo hasta primer bot funcional.
- Bots activos por organización.
- Conversaciones y tareas automatizadas.
- Tasa de resolución y derivación humana.
- Consumo y costo variable por organización.
- Ingreso recurrente mensual, cancelaciones y margen bruto.
- Tiempo de implementación y soporte por proyecto Studio.

## 12. Roadmap de producto

### Fase 1 — Fundaciones comerciales y MVP
- Definir catálogo, planes piloto y flujo de solicitud Studio.
- Mantener panel actual como prototipo interno.
- Diseñar esquema multiempresa y modelo de permisos.
- Validar Telegram y Gemini en entorno privado.

### Fase 2 — SaaS seguro
- Supabase Auth, organizaciones, membresías y RLS.
- Persistencia de bots/agentes y conexiones.
- Secretos seguros y auditoría.
- Límites de uso y medición de consumo.

### Fase 3 — Multicanal
- Correo: recepción y clasificación; borradores antes de envío automático.
- WhatsApp: integración oficial, plantillas, consentimiento y ventanas de conversación.
- Supervisor de workers y estados operativos reales.

### Fase 4 — Comercialización
- Portal de planes, onboarding y solicitud de demo.
- Suscripciones y pagos después de validar costos y condiciones.
- Panel de uso, límites, facturación y soporte.
- Casos piloto, documentación y acuerdos de servicio.

### Fase 5 — Escala
- Multi-proveedor IA, base de conocimiento y herramientas con permisos.
- Espacios para agencias/resellers.
- Integraciones CRM/ERP y analítica avanzada.

## 13. Criterios para declarar producción
No comercializar un canal como disponible hasta tener integración real, pruebas de extremo a extremo, gestión de errores, monitoreo, seguridad, documentación y revisión de políticas del proveedor. Los datos ficticios del prototipo nunca deben presentarse como métricas reales.
