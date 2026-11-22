# BOT FACTORY AI — Memoria del proyecto

## Propósito
Construir una plataforma/fábrica de bots y agentes de automatización para crear, configurar, operar y administrar soluciones conectadas a Telegram, correo electrónico y WhatsApp.

## Objetivo de negocio
Desarrollar una empresa de creación e implementación de bots para clientes, con una plataforma reutilizable que permita ofrecer automatizaciones, asistentes, integraciones, implementación y mantenimiento.

## Decisión de producto confirmada
- Modalidad elegida: **crear bots mediante un flujo automatizado/guiado y administrarlos desde un panel central Streamlit**.
- El panel debe permitir registrar bots, asociarlos a clientes, seleccionar canal, describir su objetivo, aplicar plantillas y monitorear su estado.
- Aclaración Telegram: la creación inicial del bot y la emisión del token deben realizarse mediante @BotFather. La API oficial de Telegram no permite crear bots directamente desde nuestra aplicación. BOT FACTORY AI automatizará el onboarding posterior, configuración, despliegue y administración dentro de los límites oficiales.
- No presentar como automatizadas capacidades que todavía no estén implementadas.

## Canales objetivo
- Telegram: bots, comandos, notificaciones y conversaciones.
- Correo electrónico: recepción, clasificación, respuestas y notificaciones; integrar proveedores mediante APIs y SMTP seguro cuando corresponda.
- WhatsApp: integración mediante proveedores y APIs oficiales, respetando las políticas, plantillas y permisos de cada plataforma.

## Decisiones técnicas vigentes
- Lenguaje principal: Python.
- Interfaz y panel de control: Streamlit.
- No utilizar FastAPI como base del proyecto.
- Arquitectura modular, con conectores independientes por canal.
- Supabase como plataforma de datos, autenticación y persistencia.
- Redis para colas, caché o coordinación cuando sea necesario.
- Workers independientes para ejecutar tareas en segundo plano.
- Arquitectura multimodelo mediante adaptadores; considerar Claude, OpenAI, Gemini y otros proveedores.
- GitHub es el repositorio oficial y control de versiones.

## Arquitectura
1. Aplicación Streamlit: panel administrativo, registro, configuración y monitoreo.
2. Núcleo BOT FACTORY: clientes, proyectos, bots, flujos, permisos y configuraciones.
3. Capa de conectores: Telegram, correo y WhatsApp, desacoplados.
4. Capa de IA: selección de proveedor/modelo, prompts, herramientas y políticas.
5. Persistencia: Supabase (PostgreSQL, Auth, Storage y RLS).
6. Procesamiento asíncrono: Redis + workers.
7. Observabilidad: logs, estados de ejecución, errores y auditoría.

## Principios
- Multiempresa/multicliente: separar datos, credenciales, configuraciones y permisos por cliente.
- Seguridad por diseño: mínimo privilegio, validación de entradas y auditoría.
- No almacenar secretos en el código ni en el repositorio.
- Usar variables de entorno y un archivo .env local excluido de Git.
- Incluir .env.example únicamente con nombres de variables y valores ficticios.
- Respetar términos, consentimiento, privacidad y límites de las APIs de cada canal.
- Mantener documentación actualizada y cambios versionados.

## Seguridad crítica
El repositorio es público. Nunca subir tokens de Telegram, credenciales SMTP, claves de WhatsApp, claves de Supabase, API keys de modelos, contraseñas ni datos reales de clientes. Si alguna credencial se expone, revocarla y generar otra.
La versión actual del panel no solicita ni persiste tokens. Los registros del panel son temporales en la sesión Streamlit; no constituyen todavía una base de datos ni un sistema multiusuario.

## Motor de agentes IA — Agent Factory Engine
- Se incorporó el paquete bot_factory/agents con modelo AgentSpec, validación y constructor de definiciones.
- Se incorporó contrato ModelProvider y PlaceholderProvider para separar la lógica del agente de cada proveedor.
- El panel Streamlit permite definir agentes con nombre, rol, instrucciones, proveedor previsto, modelo, canal, tenant y herramientas previstas.
- Proveedores contemplados: Anthropic/Claude, OpenAI y Google/Gemini.
- Estado actual: se crean definiciones locales en la sesión Streamlit; no se ejecutan inferencias ni herramientas todavía.
- Las herramientas seleccionables son metadatos declarativos, no permisos efectivos ni acciones ejecutables.
- Las credenciales de proveedores no forman parte de AgentSpec y deberán resolverse desde variables de entorno o secret manager.
- Claude Pro no equivale a acceso API de Anthropic; la integración API requiere habilitación y credenciales/API billing independientes.

## Decisión de costos y proveedor inicial (2026-11-22)
- El usuario indica que actualmente no hay presupuesto para APIs de pago.
- Google Gemini será el proveedor inicial recomendado, usando el nivel gratuito de Gemini API mientras las cuotas y condiciones lo permitan.
- La selección de proveedor/modelo debe permanecer configurable por agente; no acoplar bots ni canales a un único proveedor.
- Variables: GEMINI_API_KEY y GEMINI_MODEL. La clave solo se configura en .env local/secretos del despliegue, nunca en formularios ni GitHub.
- Modelo predeterminado propuesto: gemini-2.5-flash-lite; se puede cambiar mediante GEMINI_MODEL si Google mantiene disponibilidad.
- El nivel gratuito tiene límites y Google indica que el contenido puede usarse para mejorar sus productos. No utilizarlo con información confidencial de clientes; revisar condiciones antes de uso comercial.
- Se incorpora adaptador Gemini inicial y prueba manual desde Streamlit; todavía no se ha validado con API key real.
- Proveedores futuros: OpenAI, Anthropic, DeepSeek, GLM y Ollama, manteniendo el contrato común ModelProvider.

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
- [ ] Configurar token real solo en entorno privado.
- [ ] Probar conversación real con el bot.

### Panel de administración — MVP inicial
- [x] Dashboard Streamlit con métricas básicas.
- [x] Formulario para registrar fichas de bots.
- [x] Asociación inicial de cliente, canal y descripción.
- [x] Catálogo inicial de plantillas propuestas.
- [x] Guía de onboarding para Telegram.
- [x] Roadmap visible desde el panel.
- [ ] Persistencia permanente con Supabase.
- [ ] Autenticación de usuarios y roles.
- [ ] Aislamiento multiempresa con políticas RLS.
- [ ] Almacenamiento seguro de credenciales/secretos.
- [ ] Control real de inicio, parada y estado de workers.
- [ ] Registro de auditoría y pruebas automatizadas.\n- [x] Paquete fundacional Agent Factory Engine (modelos, validación y contrato de proveedor).\n- [x] Interfaz Streamlit para definir y listar agentes IA.\n- [ ] Adaptadores reales Anthropic, OpenAI y Google.\n- [ ] Memoria conversacional persistente y ejecución segura de herramientas.

## Etapas siguientes
1. Ejecutar y validar localmente el panel Streamlit y el worker Telegram.
2. Diseñar esquema Supabase multiempresa: organizaciones, usuarios, bots, canales, credenciales referenciadas y eventos.
3. Implementar Supabase Auth, PostgreSQL y RLS.
4. Integrar un gestor de secretos seguro; nunca guardar tokens en texto plano ni en GitHub.
5. Construir un supervisor de workers para iniciar, detener y monitorear instancias por bot.
6. Desarrollar conectores de correo y WhatsApp mediante APIs/proveedores oficiales.
7. Conectar adaptadores reales de IA, memoria conversacional y herramientas con permisos explícitos.
8. Definir paquetes comerciales, onboarding, soporte y mantenimiento.

## Archivos de continuidad obligatorios
- memoria.md: decisiones, arquitectura, requisitos y contexto vigente.
- bitacora_acumulada.md: registro cronológico de avances, cambios y pendientes.
Actualizar ambos en cada sesión y conservar el historial de la bitácora.

## Repositorio
- URL: https://github.com/hernandezjxs-alt/BOT-FACTORY-IA
- Propietario: hernandezjxs-alt
- Rama principal: main
- Visibilidad: pública

## Despliegue en la nube (2026-11-22)
- Plataforma seleccionada para el primer panel web: Streamlit Community Cloud, con despliegue desde el repositorio GitHub.
- Archivo de entrada: app.py en la raíz; dependencias: requirements.txt.
- Las credenciales en Streamlit Cloud se guardan en App settings / Secrets como TOML: GEMINI_API_KEY = "..." y GEMINI_MODEL = "gemini-2.5-flash-lite".
- app.py lee la clave desde st.secrets con fallback a variable de entorno para ejecución local.
- El repositorio es público; no almacenar secretos en GitHub, issues, commits ni archivos versionados.
- Estado: preparación del código/documentación completada; el usuario debe iniciar sesión en Streamlit Community Cloud, autorizar GitHub y crear el despliegue desde el móvil. El despliegue y la prueba real de Gemini aún no están confirmados.
- Limitación: el MVP conserva bots/agentes en st.session_state; los registros no son persistentes y el panel no es todavía un servicio multiusuario listo para clientes.

## Diseño visual de plataforma SaaS (2026-11-22)
- Requisito confirmado: interfaz moderna, adaptable a móvil, con tarjetas, iconografía actual, botones claros y paleta tecnológica.
- Se rediseñó app.py como dashboard SaaS con navegación lateral: Inicio, Bots, Agentes IA, Canales, Plantillas, Administración y Configuración.
- Se añadió selector de tema claro/oscuro y selector de perfil de vista Administrador/Usuario para demostración.
- El panel muestra tarjetas de métricas, secciones de actividad, estado de canales, formularios con jerarquía visual y una vista administrativa.
- Importante: el selector de rol es solo demostrativo. No constituye autenticación ni autorización; no se deben considerar protegidas las vistas hasta implementar Supabase Auth, roles y RLS.
- Los datos siguen almacenándose en st.session_state y pueden perderse al terminar la sesión. No presentar el MVP como multiusuario/productivo.
- Commit del rediseño visual de app.py: 229fe0c213df7729808c5827bbcd529841ec4e43.
- Pendiente: ejecutar y revisar el render en Streamlit Community Cloud, ajustar detalles visuales según pantalla real, y posteriormente implementar persistencia y seguridad.


## Tarjetas visuales dinámicas y resaltadas (2026-11-22)
- Solicitud adicional: las tarjetas deben tener colores resaltados y efectos dinámicos.
- Se actualizaron las cuatro tarjetas principales del dashboard con gradientes diferenciados (violeta, celeste, verde y naranja), tipografía de alto contraste, sombras, elementos decorativos y animación hover de elevación/saturación.
- Se añadieron transiciones sutiles a contenedores con borde para reforzar la interacción visual.
- Commit app.py: 1dde3bb8f4e16e45e7267e7a26badbfe1cb2fee3.


## Modelo de negocio híbrido SaaS + Studio (2026-11-22)
- Decisión confirmada por el usuario: BOT FACTORY AI operará con ambos modelos.
- SaaS: clientes se registran, crean bots/agentes desde plantillas, conectan canales y administran uso desde un panel con planes y límites.
- Studio: servicios profesionales de diagnóstico, diseño, desarrollo personalizado, integraciones, capacitación, soporte y mantenimiento.
- Ambas líneas compartirán núcleo, conectores, motor IA y aislamiento multiempresa; los proyectos Studio podrán administrarse desde espacios de trabajo SaaS.
- Segmentos: profesionales/microempresas, pymes, empresas y, en fase posterior, agencias.
- Se definieron soluciones iniciales: atención, ventas, correo inteligente, notificaciones, operaciones y asistentes internos.
- Se documentaron cuatro planes piloto (Starter, Pro, Business, Enterprise). Precios en CLP incluidos en business_model.md son hipótesis para validar, no tarifas oficiales ni precios de mercado verificados. No cobrar hasta calcular costos de infraestructura, IA, mensajería, soporte e impuestos.
- Se definieron roles objetivo: Platform Owner/Admin, Organization Owner/Admin, Operator y Viewer. El selector actual de rol sigue siendo solo demostrativo; autorización real requiere Supabase Auth + membresías + RLS.
- Se definió flujo del cliente desde demo/registro hasta conexión segura, pruebas, publicación y seguimiento.
- Se definieron entidades objetivo: organizations, memberships, subscriptions, plans, bots, agents, channel_connections, conversations, messages, usage_events, deployments, audit_events y support_tickets.
- Seguridad: aislamiento por organización, mínimo privilegio, secretos fuera del repositorio, consentimiento de canal, auditoría y aprobación humana para acciones sensibles.
- Roadmap: MVP y validación privada; SaaS seguro con Supabase; conectores de correo y WhatsApp; comercialización tras validar costos; escala con integraciones y agencias.
- Documento de producto: business_model.md.
- Estado: diseño comercial y funcional documentado; no implica que cobros, autenticación, WhatsApp, correo, persistencia o planes estén implementados.


## Página comercial del prototipo (2026-11-22)
- Se añadió al menú Streamlit la sección "Planes y servicios".
- Incluye tarjetas Starter, Pro, Business y Enterprise con precios piloto indicativos en CLP y alcance conceptual.
- Incluye catálogo BOT FACTORY Studio y formulario de solicitud de evaluación.
- Las solicitudes se guardan únicamente en st.session_state durante la sesión; no se envían ni persisten. No existe todavía facturación, suscripción ni cobro.
- Los precios se muestran como hipótesis comerciales sujetas a validación, no como tarifas definitivas.
- Commit app.py: adab38b006bd7c5eb32f40ba24cdeefe25a3ba89.


## Identidad de marca y acceso de usuario (2026-11-22)
- Se añadió una cabecera superior de marca BOT FACTORY AI con símbolo geométrico moderno, gradiente violeta/cian y descriptor "INTELLIGENT AUTOMATION PLATFORM".
- Se incorporó la opción "Acceso de usuario" a la navegación.
- La página incluye pestañas de inicio de sesión y creación de cuenta, con campos de correo y contraseña y diseño responsive coherente con la marca.
- El formulario valida campos básicos y coincidencia de contraseñas en el prototipo, pero NO autentica, registra cuentas ni guarda contraseñas.
- La autenticación, recuperación de contraseña, registro seguro, sesiones y roles reales quedan pendientes de Supabase Auth + RLS. La pantalla lo comunica expresamente para no simular seguridad.
- Commit app.py: 4f7b552479f8ed94bf85bc19d169d8e51dfb1a60.

## Rediseño de pantalla inicial con identidad visual dinámica (2026-11-22)
- Se reemplazó el encabezado/hero genérico por una portada de producto con identidad propia.
- La portada usa fondo profundo con gradiente, cuadrícula tecnológica sutil, iluminación radial y composición en dos columnas.
- Se creó un núcleo visual IA tridimensional mediante CSS, anillos orbitales y animación flotante.
- Se añadieron nodos flotantes para Telegram, correo y WhatsApp, con etiquetas de canales.
- Se incorporaron titular comercial, descripción de propuesta de valor, chips de capacidades y secuencia Diseña/Conecta/Automatiza.
- Se incluyeron reglas responsive para reorganizar y escalar la composición en pantallas móviles.
- Se conserva el dashboard de métricas debajo de la nueva portada.
- Commit app.py: d3310a7c38b1ed8739d92c0743dcdd0f95436b3e.
- Pendiente: revisar el render real en Streamlit Cloud, especialmente Android y modo claro; ajustar detalles si el CSS del host limita alguna animación.
