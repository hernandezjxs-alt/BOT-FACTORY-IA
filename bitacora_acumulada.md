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
- Se requiere mantener documentación de continuidad versionada en GitHub.

### Decisiones técnicas
- Python como lenguaje principal.
- Streamlit para la interfaz y panel de control; no FastAPI.
- Supabase para datos y autenticación.
- Redis y workers independientes para tareas asíncronas, según necesidad.
- Arquitectura modular y conectores separados por canal.
- Arquitectura multimodelo mediante adaptadores, considerando Claude y otros proveedores.

### Avance 1 — Fundaciones
- [x] Se creó memoria.md.
- [x] Se creó bitacora_acumulada.md.
- [x] Se agregó .gitignore.
- [x] Se agregó .env.example sin secretos.
- [x] Se agregó requirements.txt.
- [x] Se creó app.py con interfaz Streamlit inicial.
- [x] Se creó el paquete bot_factory.

### Avance 2 — Telegram Bot Factory MVP 0.1
- [x] Se creó bot_factory/connectors/telegram/.
- [x] Se implementaron handlers para /start, /help y /status.
- [x] Se creó el constructor de la aplicación Telegram.
- [x] Se creó run_telegram_bot.py como worker independiente.
- [x] Se documentó cómo crear el bot con @BotFather.
- [x] Se agregó python-telegram-bot a requirements.txt.
- [x] Se agregó LOG_LEVEL y TELEGRAM_BOT_TOKEN a .env.example.
- [x] El token se lee desde variable de entorno; no se incluye ningún token real en Git.

### Seguridad
El repositorio es público. No publicar tokens, contraseñas, API keys, credenciales, datos personales ni archivos .env. Si un token se expone, revocarlo y generar uno nuevo desde el proveedor.

### Estado real
El código del MVP fue escrito en GitHub. Aún no se ha ejecutado en un equipo local ni se ha probado con un token real de Telegram; por tanto, no declarar el bot operativo en producción.

### Pendientes inmediatos
1. Instalar dependencias localmente con pip install -r requirements.txt.
2. Crear el bot con @BotFather y guardar el token en .env local.
3. Ejecutar python run_telegram_bot.py.
4. Probar /start, /help y /status desde Telegram.
5. Incorporar pruebas automatizadas.
6. Construir la interfaz Streamlit para administrar y monitorear bots.
7. Diseñar persistencia multiempresa y almacenamiento seguro de credenciales en Supabase.

### Regla permanente
Actualizar memoria.md cuando cambien decisiones o requisitos. Agregar entradas fechadas a bitacora_acumulada.md sin borrar entradas anteriores.


## 2026-11-22 — Decisión de administración automática y panel Streamlit

### Decisión confirmada por el usuario
Se elige la modalidad de creación automatizada/guiada de bots y administración centralizada desde Streamlit. El objetivo es que BOT FACTORY AI sea la plataforma operativa de una empresa que implemente y mantenga bots para múltiples clientes.

### Avance 3 — Panel de gestión MVP
- [x] Se amplió app.py con dashboard y métricas iniciales.
- [x] Se agregó formulario para registrar fichas de bots con nombre, canal, cliente y descripción.
- [x] Se agregó catálogo inicial de plantillas para Telegram, correo y WhatsApp.
- [x] Se agregó guía de onboarding para Telegram y roadmap de implementación.
- [x] Los registros se mantienen solo en la sesión Streamlit; todavía no hay persistencia permanente.
- [x] El panel no solicita ni almacena tokens ni secretos.

### Aclaración técnica importante
Telegram requiere que el bot sea creado inicialmente mediante @BotFather; la API de Telegram no permite que una aplicación de terceros cree bots directamente. La automatización de BOT FACTORY AI cubrirá el flujo guiado, registro, configuración posterior, despliegue y administración, sin intentar eludir esa limitación.

### Estado y límites de validación
- El cambio de app.py fue publicado en GitHub.
- No se ha ejecutado el panel localmente ni se ha validado en un despliegue.
- El registro actual es temporal y no soporta todavía multiusuario o multiempresa.
- El worker Telegram previo tampoco ha sido probado con credenciales reales.

### Próximos pasos
1. Validar localmente Streamlit y el worker Telegram.
2. Implementar esquema Supabase, autenticación y RLS multiempresa.
3. Diseñar almacenamiento seguro de secretos antes de incorporar tokens de clientes.
4. Implementar supervisor de workers y monitoreo real.
5. Continuar con correo y WhatsApp mediante integraciones oficiales.

### Continuidad
Se actualizó memoria.md para reflejar la decisión del usuario, el alcance real del panel y las limitaciones actuales. Se conserva íntegro el historial previo de esta bitácora.


## 2026-11-22 — Agent Factory Engine: primera implementación

### Objetivo
Incorporar agentes IA como componentes propios de BOT FACTORY AI, separados de los bots/canales de mensajería.

### Avances publicados
- [x] Se creó bot_factory/agents/models.py con AgentSpec y validaciones.
- [x] Se creó bot_factory/agents/registry.py para construir definiciones validadas.
- [x] Se creó la interfaz ModelProvider para desacoplar los proveedores de IA.
- [x] Se agregó PlaceholderProvider que informa explícitamente cuando un proveedor aún no está conectado.
- [x] Se documentó el paquete en bot_factory/agents/README.md.
- [x] Se amplió app.py con la pestaña Agent Factory.
- [x] El panel permite definir nombre, rol, instrucciones, proveedor previsto, modelo, canal, tenant y herramientas previstas.
- [x] El dashboard muestra el número y listado de agentes definidos.

### Alcance y límites actuales
- Los agentes son definiciones de configuración, no agentes autónomos en ejecución.
- Los registros se conservan únicamente en session_state de Streamlit y se pierden al finalizar la sesión.
- No hay llamadas reales a Claude, OpenAI o Gemini.
- Las herramientas seleccionables son etiquetas descriptivas; todavía no ejecutan acciones.
- No hay memoria conversacional persistente, autenticación, aislamiento RLS ni gestor de secretos.
- No introducir API keys ni tokens en formularios, código o GitHub.
- Claude Pro no concede por sí solo acceso a la API de Anthropic; la API requiere habilitación y credenciales independientes.

### Próxima etapa técnica
1. Añadir pruebas unitarias al modelo AgentSpec y su validación.
2. Crear adaptador real del primer proveedor elegido, leyendo credenciales solo desde entorno seguro.
3. Persistir agentes y organizaciones en Supabase con RLS.
4. Implementar memoria conversacional por agente y tenant.
5. Diseñar herramientas con lista permitida, confirmación humana para acciones sensibles, límites y auditoría.
6. Vincular agentes a bots/canales una vez exista persistencia y configuración segura.

### Continuidad
Se actualizó memoria.md con el estado real del motor de agentes y se conserva todo el historial anterior.


## 2026-11-22 — Gemini configurable como proveedor inicial sin presupuesto

### Decisión del usuario
- Se utilizará Google Gemini como primera opción de IA debido a que actualmente no hay presupuesto para APIs de pago.
- El proveedor y modelo deben ser configurables para poder cambiar en el futuro a GPT, DeepSeek, GLM, Claude u Ollama sin reconstruir bots ni canales.

### Cambios preparados/publicados
- [x] Adaptador inicial Gemini con SDK oficial google-genai.
- [x] Lectura de GEMINI_API_KEY y GEMINI_MODEL desde entorno/secretos; no se exponen en formularios.
- [x] Modelo predeterminado gemini-2.5-flash-lite, configurable mediante variable de entorno.
- [x] Dependencia google-genai agregada a requirements.txt.
- [x] Variables Gemini agregadas a .env.example sin credenciales.
- [x] Panel Streamlit informa si detecta la clave y ofrece una prueba de conversación para agentes configurados con proveedor google.
- [x] Documentación del adaptador y límites del nivel gratuito.

### Costos, privacidad y límites
- Google ofrece nivel gratuito con límites de uso para modelos elegibles. Las cuotas pueden variar y no equivalen a servicio ilimitado ni garantizado para producción.
- Google indica que el contenido del nivel gratuito puede utilizarse para mejorar sus productos; no usarlo para información sensible o confidencial de clientes.
- No se configuró facturación ni se añadió ninguna API key real.

### Estado de validación
- Código publicado, pendiente de instalar dependencias y probar con una API key real en entorno privado.
- No afirmar que Gemini está operativo hasta completar esa prueba.

### Próximos pasos
1. Configurar una clave gratuita desde Google AI Studio en el .env local.
2. Instalar requirements.txt y ejecutar Streamlit.
3. Crear un agente con proveedor google y ejecutar la prueba de conversación.
4. Añadir límites de uso, registro de consumo y persistencia multiempresa antes de ofrecerlo a clientes.

## 2026-11-22 — Preparación del despliegue móvil en Streamlit Community Cloud

### Contexto
El usuario confirmó que dispone de acceso a GitHub desde Android y desea administrar BOT FACTORY AI desde el teléfono, sin configurar un computador local.

### Revisión del repositorio
- [x] Confirmado repositorio hernandezjxs-alt/BOT-FACTORY-IA, rama main y permisos de administración.
- [x] Confirmado app.py en raíz y requirements.txt con Streamlit y google-genai.
- [x] Confirmado .gitignore excluye .env y .streamlit/secrets.toml.
- [x] Detectado que el panel consultaba únicamente os.getenv para la API key, lo que no es suficiente para leer secretos de Streamlit Cloud.

### Cambios de preparación
- [x] app.py actualizado para leer GEMINI_API_KEY y GEMINI_MODEL desde st.secrets, con fallback a variables de entorno para ejecución local.
- [x] Prueba Gemini usa la clave inyectada desde el gestor de secretos y no muestra su valor.
- [x] memoria.md corregido para eliminar secuencias de salto de línea malformadas y registrar el despliegue cloud.
- [x] Se agregó guía de despliegue móvil (DEPLOYMENT_STREAMLIT.md).

### Pasos pendientes del usuario
1. Revocar la API key de Gemini que compartió anteriormente y generar una nueva.
2. Abrir Streamlit Community Cloud e iniciar sesión con GitHub.
3. Autorizar acceso al repositorio público BOT-FACTORY-IA.
4. Crear la app usando rama main y archivo app.py.
5. En Advanced settings / Secrets, configurar la nueva clave (nunca compartirla en el chat).
6. Esperar el despliegue, abrir la URL generada y probar un agente Gemini.

### Estado y límites
- Código y guía preparados en GitHub; no se ha creado todavía una app en Streamlit Cloud ni se ha validado el runtime.
- Streamlit Community Cloud ofrece hosting gratuito según sus condiciones vigentes, pero no equivale a un SLA de producción.
- El registro de bots/agentes sigue siendo temporal en session_state. Antes de atender clientes reales se requiere Supabase Auth/RLS, persistencia, aislamiento multiempresa y políticas de privacidad.

## 2026-11-22 — Rediseño visual moderno de BOT FACTORY AI

### Requisito del usuario
La aplicación debe tener una apariencia moderna y profesional, con tarjetas, botón/área de administración, vistas de administrador y usuario, modo claro y oscuro, iconos modernos y colores actuales; debe funcionar desde el teléfono.

### Cambios publicados
- [x] Rediseño de app.py con estilo visual SaaS y paleta tecnológica.
- [x] Navegación lateral por Inicio, Bots, Agentes IA, Canales, Plantillas, Administración y Configuración.
- [x] Tarjetas de métricas y paneles de actividad/conectores.
- [x] Selector de tema claro/oscuro.
- [x] Selector de perfil Administrador/Usuario para previsualizar las vistas.
- [x] Se conservaron los formularios de bots y agentes y el laboratorio Gemini.
- [x] Se documentó que el selector de rol es demostrativo y no ofrece seguridad real.

### Límites y pendientes
- Los datos siguen en session_state; no hay persistencia Supabase.
- No existe todavía login ni autorización real por rol. No usar el selector visual como mecanismo de seguridad.
- La vista debe probarse en el despliegue Streamlit para validar el aspecto real en Android.
- Próximo paso: desplegar la versión actualizada, configurar GEMINI_API_KEY en Secrets de Streamlit (sin compartirla) y comprobar la aplicación. Luego implementar Supabase Auth/RLS y persistencia multiempresa.

### Commit
- app.py rediseñado: 229fe0c213df7729808c5827bbcd529841ec4e43.


## 2026-11-22 — Tarjetas con colores resaltados y efectos dinámicos
- [x] Se asignaron gradientes distintos a las métricas: violeta para bots, celeste para agentes IA, verde para Telegram y naranja para canales.
- [x] Se agregaron sombras, formas decorativas, alto contraste y transición hover con elevación.
- [x] Se añadieron efectos sutiles de interacción a los contenedores con borde.
- [x] Cambio publicado en app.py, commit 1dde3bb8f4e16e45e7267e7a26badbfe1cb2fee3.
- [ ] Validar visualización final desde Streamlit Cloud y ajustar según pantalla Android.


## 2026-11-22 — Decisión de modelo de negocio híbrido y diseño del producto

### Decisión confirmada
El usuario eligió **Ambos**: plataforma SaaS de autoservicio + servicios profesionales personalizados BOT FACTORY Studio.

### Diseño funcional y comercial
- [x] Se definieron dos líneas de negocio que comparten la misma plataforma.
- [x] Se definieron segmentos: profesionales, microempresas, pymes, empresas y futura oferta para agencias.
- [x] Se definió catálogo inicial: atención, ventas, correo inteligente, notificaciones, operaciones y asistentes internos.
- [x] Se diseñó el recorrido del cliente desde demo/registro hasta conexión, pruebas, publicación y soporte.
- [x] Se definieron roles objetivo de plataforma y organización.
- [x] Se definieron entidades principales para el futuro esquema multiempresa.
- [x] Se documentaron principios de seguridad, métricas y criterios para considerar un canal listo para producción.
- [x] Se documentaron planes piloto Starter, Pro, Business y Enterprise.

### Precios y cautelas
Los precios en CLP del documento son hipótesis para validar con pilotos, no tarifas definitivas ni referencias de mercado. Antes de cobrar se deben calcular costos variables de IA, WhatsApp, correo, infraestructura, soporte e impuestos, y establecer cuotas y excedentes. No ofrecer uso ilimitado.

### Documento creado
- business_model.md: propuesta de valor, líneas comerciales, segmentos, catálogo, planes de prueba, servicios Studio, roles, arquitectura, seguridad, métricas y roadmap.

### Pendientes de implementación
1. Diseñar y crear el esquema Supabase multiempresa con RLS.
2. Implementar autenticación, organizaciones y membresías.
3. Persistir bots y agentes; eliminar dependencia exclusiva de session_state.
4. Crear onboarding de cliente y flujo de solicitud de cotización Studio.
5. Medir consumo y costos antes de habilitar suscripciones/pagos.
6. Completar conectores oficiales de correo y WhatsApp.
7. Validar despliegue Streamlit y pruebas privadas de Telegram/Gemini.

El diseño comercial está documentado; las funciones anteriores siguen pendientes y no se consideran implementadas.


## 2026-11-22 — Primera pantalla comercial en Streamlit

- [x] Se añadió "Planes y servicios" a la navegación.
- [x] Se incorporaron tarjetas de planes Starter, Pro, Business y Enterprise con valores piloto indicativos.
- [x] Se añadió el catálogo BOT FACTORY Studio.
- [x] Se añadió formulario para solicitar evaluación de un proyecto personalizado.
- [x] Las solicitudes quedan en memoria de sesión solo para demostración.
- [ ] Conectar formulario a Supabase y notificación segura.
- [ ] Validar precios con clientes piloto y costos variables.
- [ ] Implementar suscripciones, límites y pagos después de validar el modelo.
- [ ] Probar visualmente la nueva página en Streamlit Community Cloud.
- [ ] Ejecutar pruebas automatizadas y validar dependencias.
- Nota: el formulario no envía correos ni guarda información permanentemente; la página no habilita cobros.


## 2026-11-22 — Identidad de marca y página de acceso de usuario
- [x] Se agregó una cabecera superior con símbolo moderno geométrico y gradiente violeta/cian.
- [x] Se incorporó el nombre BOT FACTORY AI y el descriptor INTELLIGENT AUTOMATION PLATFORM.
- [x] Se añadió "Acceso de usuario" al menú de navegación.
- [x] Se diseñó la pantalla de acceso con pestañas para iniciar sesión y crear cuenta.
- [x] Se añadieron campos de correo y contraseña, confirmación de contraseña y validación básica del formulario de registro.
- [x] Se dejó explícito que el formulario es una interfaz de demostración y no autentica ni crea usuarios todavía.
- [ ] Conectar Supabase Auth para registro, inicio/cierre de sesión, recuperación de contraseña y sesiones seguras.
- [ ] Crear perfiles, organizaciones, membresías y políticas RLS antes de habilitar usuarios reales.
- [ ] Probar el encabezado y la página de acceso en Streamlit Community Cloud desde Android.
- Commit app.py: 4f7b552479f8ed94bf85bc19d169d8e51dfb1a60.

## 2026-11-22 — Rediseño dinámico de la pantalla inicial
- [x] Se eliminó la cabecera hero genérica de la portada.
- [x] Se creó una composición de bienvenida con estética SaaS/AI propia de BOT FACTORY AI.
- [x] Se añadió fondo tecnológico con cuadrícula, gradientes e iluminación ambiental.
- [x] Se diseñó un núcleo IA con anillos orbitales, brillo y movimiento CSS.
- [x] Se agregaron nodos flotantes Telegram, Email y WhatsApp.
- [x] Se incorporó mensaje principal, propuesta de valor y etiquetas de capacidades.
- [x] Se adaptó la composición para móvil mediante media queries.
- [x] Se mantuvo el panel de operaciones y las tarjetas de indicadores debajo de la portada.
- [ ] Verificar el aspecto real en Streamlit Community Cloud desde Android y escritorio.
- [ ] Ajustar contraste/escala en modo claro y revisar comportamiento de animaciones en navegadores móviles.
- Commit app.py: d3310a7c38b1ed8739d92c0743dcdd0f95436b3e.
