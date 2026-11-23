# 📝 BOT FACTORY AI — Bitácora acumulada

Registro cronológico de decisiones, avances, cambios y pendientes del proyecto.

## 📝 2026-11-22 — Inicio de documentación y continuidad

### 🎯 Objetivo confirmado
Crear una empresa/plataforma de desarrollo de bots y automatizaciones para Telegram, correo electrónico y WhatsApp.

### 📌 Repositorio
- URL: https://github.com/hernandezjxs-alt/BOT-FACTORY-IA
- Propietario: hernandezjxs-alt
- Rama: main
- Visibilidad: pública.
- Se requiere mantener documentación de continuidad versionada en GitHub.

### 📌 Decisiones técnicas
- Python como lenguaje principal.
- Streamlit para la interfaz y panel de control; no FastAPI.
- Supabase para datos y autenticación.
- Redis y workers independientes para tareas asíncronas, según necesidad.
- Arquitectura modular y conectores separados por canal.
- Arquitectura multimodelo mediante adaptadores, considerando Claude y otros proveedores.

### 📌 Avance 1 — Fundaciones
- [x] Se creó memoria.md.
- [x] Se creó bitacora_acumulada.md.
- [x] Se agregó .gitignore.
- [x] Se agregó .env.example sin secretos.
- [x] Se agregó requirements.txt.
- [x] Se creó app.py con interfaz Streamlit inicial.
- [x] Se creó el paquete bot_factory.

### ✈️ Avance 2 — Telegram Bot Factory MVP 0.1
- [x] Se creó bot_factory/connectors/telegram/.
- [x] Se implementaron handlers para /start, /help y /status.
- [x] Se creó el constructor de la aplicación Telegram.
- [x] Se creó run_telegram_bot.py como worker independiente.
- [x] Se documentó cómo crear el bot con @BotFather.
- [x] Se agregó python-telegram-bot a requirements.txt.
- [x] Se agregó LOG_LEVEL y TELEGRAM_BOT_TOKEN a .env.example.
- [x] El token se lee desde variable de entorno; no se incluye ningún token real en Git.

### 🔐 Seguridad
El repositorio es público. No publicar tokens, contraseñas, API keys, credenciales, datos personales ni archivos .env. Si un token se expone, revocarlo y generar uno nuevo desde el proveedor.

### 📊 Estado real
El código del MVP fue escrito en GitHub. Aún no se ha ejecutado en un equipo local ni se ha probado con un token real de Telegram; por tanto, no declarar el bot operativo en producción.

### 🗺️ Pendientes inmediatos
1. Instalar dependencias localmente con pip install -r requirements.txt.
2. Crear el bot con @BotFather y guardar el token en .env local.
3. Ejecutar python run_telegram_bot.py.
4. Probar /start, /help y /status desde Telegram.
5. Incorporar pruebas automatizadas.
6. Construir la interfaz Streamlit para administrar y monitorear bots.
7. Diseñar persistencia multiempresa y almacenamiento seguro de credenciales en Supabase.

### 📌 Regla permanente
Actualizar memoria.md cuando cambien decisiones o requisitos. Agregar entradas fechadas a bitacora_acumulada.md sin borrar entradas anteriores.


## ☁️ 2026-11-22 — Decisión de administración automática y panel Streamlit

### 📌 Decisión confirmada por el usuario
Se elige la modalidad de creación automatizada/guiada de bots y administración centralizada desde Streamlit. El objetivo es que BOT FACTORY AI sea la plataforma operativa de una empresa que implemente y mantenga bots para múltiples clientes.

### 📌 Avance 3 — Panel de gestión MVP
- [x] Se amplió app.py con dashboard y métricas iniciales.
- [x] Se agregó formulario para registrar fichas de bots con nombre, canal, cliente y descripción.
- [x] Se agregó catálogo inicial de plantillas para Telegram, correo y WhatsApp.
- [x] Se agregó guía de onboarding para Telegram y roadmap de implementación.
- [x] Los registros se mantienen solo en la sesión Streamlit; todavía no hay persistencia permanente.
- [x] El panel no solicita ni almacena tokens ni secretos.

### 📌 Aclaración técnica importante
Telegram requiere que el bot sea creado inicialmente mediante @BotFather; la API de Telegram no permite que una aplicación de terceros cree bots directamente. La automatización de BOT FACTORY AI cubrirá el flujo guiado, registro, configuración posterior, despliegue y administración, sin intentar eludir esa limitación.

### 📊 Estado y límites de validación
- El cambio de app.py fue publicado en GitHub.
- No se ha ejecutado el panel localmente ni se ha validado en un despliegue.
- El registro actual es temporal y no soporta todavía multiusuario o multiempresa.
- El worker Telegram previo tampoco ha sido probado con credenciales reales.

### 🗺️ Próximos pasos
1. Validar localmente Streamlit y el worker Telegram.
2. Implementar esquema Supabase, autenticación y RLS multiempresa.
3. Diseñar almacenamiento seguro de secretos antes de incorporar tokens de clientes.
4. Implementar supervisor de workers y monitoreo real.
5. Continuar con correo y WhatsApp mediante integraciones oficiales.

### 📚 Continuidad
Se actualizó memoria.md para reflejar la decisión del usuario, el alcance real del panel y las limitaciones actuales. Se conserva íntegro el historial previo de esta bitácora.


## 📊 2026-11-22 — Agent Factory Engine: primera implementación

### 🎯 Objetivo
Incorporar agentes IA como componentes propios de BOT FACTORY AI, separados de los bots/canales de mensajería.

### 📌 Avances publicados
- [x] Se creó bot_factory/agents/models.py con AgentSpec y validaciones.
- [x] Se creó bot_factory/agents/registry.py para construir definiciones validadas.
- [x] Se creó la interfaz ModelProvider para desacoplar los proveedores de IA.
- [x] Se agregó PlaceholderProvider que informa explícitamente cuando un proveedor aún no está conectado.
- [x] Se documentó el paquete en bot_factory/agents/README.md.
- [x] Se amplió app.py con la pestaña Agent Factory.
- [x] El panel permite definir nombre, rol, instrucciones, proveedor previsto, modelo, canal, tenant y herramientas previstas.
- [x] El dashboard muestra el número y listado de agentes definidos.

### 📌 Alcance y límites actuales
- Los agentes son definiciones de configuración, no agentes autónomos en ejecución.
- Los registros se conservan únicamente en session_state de Streamlit y se pierden al finalizar la sesión.
- No hay llamadas reales a Claude, OpenAI o Gemini.
- Las herramientas seleccionables son etiquetas descriptivas; todavía no ejecutan acciones.
- No hay memoria conversacional persistente, autenticación, aislamiento RLS ni gestor de secretos.
- No introducir API keys ni tokens en formularios, código o GitHub.
- Claude Pro no concede por sí solo acceso a la API de Anthropic; la API requiere habilitación y credenciales independientes.

### 🗺️ Próxima etapa técnica
1. Añadir pruebas unitarias al modelo AgentSpec y su validación.
2. Crear adaptador real del primer proveedor elegido, leyendo credenciales solo desde entorno seguro.
3. Persistir agentes y organizaciones en Supabase con RLS.
4. Implementar memoria conversacional por agente y tenant.
5. Diseñar herramientas con lista permitida, confirmación humana para acciones sensibles, límites y auditoría.
6. Vincular agentes a bots/canales una vez exista persistencia y configuración segura.

### 📚 Continuidad
Se actualizó memoria.md con el estado real del motor de agentes y se conserva todo el historial anterior.


## 🧠 2026-11-22 — Gemini configurable como proveedor inicial sin presupuesto

### 📌 Decisión del usuario
- Se utilizará Google Gemini como primera opción de IA debido a que actualmente no hay presupuesto para APIs de pago.
- El proveedor y modelo deben ser configurables para poder cambiar en el futuro a GPT, DeepSeek, GLM, Claude u Ollama sin reconstruir bots ni canales.

### 📝 Cambios preparados/publicados
- [x] Adaptador inicial Gemini con SDK oficial google-genai.
- [x] Lectura de GEMINI_API_KEY y GEMINI_MODEL desde entorno/secretos; no se exponen en formularios.
- [x] Modelo predeterminado gemini-2.5-flash-lite, configurable mediante variable de entorno.
- [x] Dependencia google-genai agregada a requirements.txt.
- [x] Variables Gemini agregadas a .env.example sin credenciales.
- [x] Panel Streamlit informa si detecta la clave y ofrece una prueba de conversación para agentes configurados con proveedor google.
- [x] Documentación del adaptador y límites del nivel gratuito.

### 🔐 Costos, privacidad y límites
- Google ofrece nivel gratuito con límites de uso para modelos elegibles. Las cuotas pueden variar y no equivalen a servicio ilimitado ni garantizado para producción.
- Google indica que el contenido del nivel gratuito puede utilizarse para mejorar sus productos; no usarlo para información sensible o confidencial de clientes.
- No se configuró facturación ni se añadió ninguna API key real.

### 📊 Estado de validación
- Código publicado, pendiente de instalar dependencias y probar con una API key real en entorno privado.
- No afirmar que Gemini está operativo hasta completar esa prueba.

### 🗺️ Próximos pasos
1. Configurar una clave gratuita desde Google AI Studio en el .env local.
2. Instalar requirements.txt y ejecutar Streamlit.
3. Crear un agente con proveedor google y ejecutar la prueba de conversación.
4. Añadir límites de uso, registro de consumo y persistencia multiempresa antes de ofrecerlo a clientes.

## ☁️ 2026-11-22 — Preparación del despliegue móvil en Streamlit Community Cloud

### 📌 Contexto
El usuario confirmó que dispone de acceso a GitHub desde Android y desea administrar BOT FACTORY AI desde el teléfono, sin configurar un computador local.

### 📝 Revisión del repositorio
- [x] Confirmado repositorio hernandezjxs-alt/BOT-FACTORY-IA, rama main y permisos de administración.
- [x] Confirmado app.py en raíz y requirements.txt con Streamlit y google-genai.
- [x] Confirmado .gitignore excluye .env y .streamlit/secrets.toml.
- [x] Detectado que el panel consultaba únicamente os.getenv para la API key, lo que no es suficiente para leer secretos de Streamlit Cloud.

### 📝 Cambios de preparación
- [x] app.py actualizado para leer GEMINI_API_KEY y GEMINI_MODEL desde st.secrets, con fallback a variables de entorno para ejecución local.
- [x] Prueba Gemini usa la clave inyectada desde el gestor de secretos y no muestra su valor.
- [x] memoria.md corregido para eliminar secuencias de salto de línea malformadas y registrar el despliegue cloud.
- [x] Se agregó guía de despliegue móvil (DEPLOYMENT_STREAMLIT.md).

### 🗺️ Pasos pendientes del usuario
1. Revocar la API key de Gemini que compartió anteriormente y generar una nueva.
2. Abrir Streamlit Community Cloud e iniciar sesión con GitHub.
3. Autorizar acceso al repositorio público BOT-FACTORY-IA.
4. Crear la app usando rama main y archivo app.py.
5. En Advanced settings / Secrets, configurar la nueva clave (nunca compartirla en el chat).
6. Esperar el despliegue, abrir la URL generada y probar un agente Gemini.

### 📊 Estado y límites
- Código y guía preparados en GitHub; no se ha creado todavía una app en Streamlit Cloud ni se ha validado el runtime.
- Streamlit Community Cloud ofrece hosting gratuito según sus condiciones vigentes, pero no equivale a un SLA de producción.
- El registro de bots/agentes sigue siendo temporal en session_state. Antes de atender clientes reales se requiere Supabase Auth/RLS, persistencia, aislamiento multiempresa y políticas de privacidad.

## 📝 2026-11-22 — Rediseño visual moderno de BOT FACTORY AI

### 📌 Requisito del usuario
La aplicación debe tener una apariencia moderna y profesional, con tarjetas, botón/área de administración, vistas de administrador y usuario, modo claro y oscuro, iconos modernos y colores actuales; debe funcionar desde el teléfono.

### 📝 Cambios publicados
- [x] Rediseño de app.py con estilo visual SaaS y paleta tecnológica.
- [x] Navegación lateral por Inicio, Bots, Agentes IA, Canales, Plantillas, Administración y Configuración.
- [x] Tarjetas de métricas y paneles de actividad/conectores.
- [x] Selector de tema claro/oscuro.
- [x] Selector de perfil Administrador/Usuario para previsualizar las vistas.
- [x] Se conservaron los formularios de bots y agentes y el laboratorio Gemini.
- [x] Se documentó que el selector de rol es demostrativo y no ofrece seguridad real.

### 🗺️ Límites y pendientes
- Los datos siguen en session_state; no hay persistencia Supabase.
- No existe todavía login ni autorización real por rol. No usar el selector visual como mecanismo de seguridad.
- La vista debe probarse en el despliegue Streamlit para validar el aspecto real en Android.
- Próximo paso: desplegar la versión actualizada, configurar GEMINI_API_KEY en Secrets de Streamlit (sin compartirla) y comprobar la aplicación. Luego implementar Supabase Auth/RLS y persistencia multiempresa.

### 📌 Commit
- app.py rediseñado: 229fe0c213df7729808c5827bbcd529841ec4e43.


## 📝 2026-11-22 — Tarjetas con colores resaltados y efectos dinámicos
- [x] Se asignaron gradientes distintos a las métricas: violeta para bots, celeste para agentes IA, verde para Telegram y naranja para canales.
- [x] Se agregaron sombras, formas decorativas, alto contraste y transición hover con elevación.
- [x] Se añadieron efectos sutiles de interacción a los contenedores con borde.
- [x] Cambio publicado en app.py, commit 1dde3bb8f4e16e45e7267e7a26badbfe1cb2fee3.
- [ ] Validar visualización final desde Streamlit Cloud y ajustar según pantalla Android.


## 🏢 2026-11-22 — Decisión de modelo de negocio híbrido y diseño del producto

### 📌 Decisión confirmada
El usuario eligió **Ambos**: plataforma SaaS de autoservicio + servicios profesionales personalizados BOT FACTORY Studio.

### 📊 Diseño funcional y comercial
- [x] Se definieron dos líneas de negocio que comparten la misma plataforma.
- [x] Se definieron segmentos: profesionales, microempresas, pymes, empresas y futura oferta para agencias.
- [x] Se definió catálogo inicial: atención, ventas, correo inteligente, notificaciones, operaciones y asistentes internos.
- [x] Se diseñó el recorrido del cliente desde demo/registro hasta conexión, pruebas, publicación y soporte.
- [x] Se definieron roles objetivo de plataforma y organización.
- [x] Se definieron entidades principales para el futuro esquema multiempresa.
- [x] Se documentaron principios de seguridad, métricas y criterios para considerar un canal listo para producción.
- [x] Se documentaron planes piloto Starter, Pro, Business y Enterprise.

### 📌 Precios y cautelas
Los precios en CLP del documento son hipótesis para validar con pilotos, no tarifas definitivas ni referencias de mercado. Antes de cobrar se deben calcular costos variables de IA, WhatsApp, correo, infraestructura, soporte e impuestos, y establecer cuotas y excedentes. No ofrecer uso ilimitado.

### 📚 Documento creado
- business_model.md: propuesta de valor, líneas comerciales, segmentos, catálogo, planes de prueba, servicios Studio, roles, arquitectura, seguridad, métricas y roadmap.

### 📊 Pendientes de implementación
1. Diseñar y crear el esquema Supabase multiempresa con RLS.
2. Implementar autenticación, organizaciones y membresías.
3. Persistir bots y agentes; eliminar dependencia exclusiva de session_state.
4. Crear onboarding de cliente y flujo de solicitud de cotización Studio.
5. Medir consumo y costos antes de habilitar suscripciones/pagos.
6. Completar conectores oficiales de correo y WhatsApp.
7. Validar despliegue Streamlit y pruebas privadas de Telegram/Gemini.

El diseño comercial está documentado; las funciones anteriores siguen pendientes y no se consideran implementadas.


## ☁️ 2026-11-22 — Primera pantalla comercial en Streamlit

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


## 📝 2026-11-22 — Identidad de marca y página de acceso de usuario
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

## 📝 2026-11-22 — Rediseño dinámico de la pantalla inicial
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


## 📝 2026-11-22 — Ajustes globales de diseño responsive
- [x] Se estableció como requisito transversal la compatibilidad visual y funcional con móvil, tablet y escritorio.
- [x] La barra lateral ahora usa estado automático para facilitar la navegación en pantallas pequeñas.
- [x] Se agregaron reglas globales para márgenes, marca, tipografía, tarjetas, formularios, botones y contenedores de datos.
- [x] En pantallas de 760 px o menos, las columnas se apilan al 100% para evitar contenido comprimido; en escritorio se mantiene el diseño por columnas.
- [x] Se reforzó el escalado del hero y la esfera IA en teléfonos estrechos.
- [x] Se añadió soporte para prefers-reduced-motion y desactivación de animaciones decorativas cuando el sistema lo solicita.
- [ ] Probar en Streamlit Community Cloud desde un Android real y en navegador de escritorio.
- [ ] Ajustar cualquier desbordamiento o diferencia visual detectada mediante capturas.
- Nota: los cambios de CSS no sustituyen las pruebas reales de navegador ni garantizan por sí solos el comportamiento de cada widget Streamlit.


## ☁️ 2026-11-22 — Reparación del error de inicio en Streamlit
- [x] Se recibió el error: SyntaxError en app.py, línea 94, f-string expecting a valid expression after '{'.
- [x] Se revisó el archivo real en la rama main y se identificó que los bloques CSS responsive globales usaban llaves simples dentro de st.markdown(f"""...""").
- [x] Se escaparon las llaves de los bloques CSS responsive para que Python las trate como texto literal.
- [x] Se publicó la corrección en GitHub.
- Commit app.py: 3b3011fa046f6388f145536f382a0f8e08545013.
- [x] Se actualizó memoria.md con el diagnóstico y la solución.
- [ ] Esperar/revisar el reinicio de Streamlit Cloud y confirmar que la aplicación abra.
- [ ] Si aparece otro error, revisar el nuevo traceback completo y corregirlo.


## 📝 2026-11-22 — Refinamiento visual de tarjetas y núcleo IA
- [x] Se cambiaron las tarjetas de métricas de degradados multicolores a fondos sólidos, conservando la paleta individual violeta, cian, verde y naranja.
- [x] Se sustituyó el asterisco del centro de la esfera IA por un icono de globo 🌐.
- [x] Se actualizó memoria.md.
- Commit app.py: 9b736ad9479bbdc30b2ff24a4c8596b97f71158a.
- [ ] Revisar el resultado en Streamlit Cloud desde móvil y escritorio.


## 📝 2026-11-22 — Identidad visual hexagonal aprobada e integrada

### 📌 Decisión del usuario
- El usuario aprobó la propuesta visual con hexágono tecnológico, núcleo holográfico animado y marca BOT FACTORY AI.

### 📝 Cambios publicados
- [x] Se reemplazó el símbolo genérico del encabezado por un logotipo hexagonal vectorial SVG con núcleo y nodos conectados.
- [x] Se sustituyó la esfera circular de la portada por un núcleo hexagonal holográfico construido con SVG y CSS.
- [x] Se agregaron dos anillos orbitales animados y un pulso luminoso cian/violeta.
- [x] Se actualizó el icono de pestaña del navegador y el título de marca de la barra lateral.
- [x] Se conservó el diseño responsive y la preferencia de movimiento reducido.
- [x] No se incorporaron recursos premium ni dependencias de pago; la identidad visual se dibuja en el propio código.
- [x] Se actualizaron memoria.md y esta bitácora acumulativa.

### 📌 Commit
- app.py: 61ccc9df922f54868050a406751100c60940c926.
- memoria.md: 9fdc8f2d9b63a3f9629458bfe1c25c64707775b2.

### 🗺️ Pendiente de validación
- [ ] Recargar Streamlit Community Cloud y comprobar que el despliegue complete el reinicio.
- [ ] Revisar la marca y el núcleo holográfico desde Android y escritorio.
- [ ] Revisar modo claro y oscuro, y ajustar tamaños si la captura real lo requiere.
- Nota: el cambio está publicado en GitHub, pero todavía no se ha confirmado visualmente en el despliegue.


## 📝 2026-11-22 — Corrección visual de los iconos de canales
- El usuario reportó que la portada publicada no se parecía al prototipo aprobado y que no se veían correctamente los iconos de Telegram y WhatsApp.
- Se reemplazaron los emojis por SVG inline reconocibles: avión de Telegram, símbolo verde de WhatsApp y sobre de correo.
- Se reforzaron las tarjetas flotantes (fondo, borde, tamaño y distribución) alrededor del núcleo hexagonal holográfico.
- Commit app.py: 77c825ee27a788bd45f03a1dd9bc6cc0887899eb.
- memoria.md actualizado en commit a4a2a22b3e2292f3171e88013d9926b379e5d96c.
- Pendiente: recargar Streamlit Cloud y revisar captura en móvil; no se ha confirmado todavía el resultado visual del despliegue.


## 📝 2026-11-22 — Revisión de la identidad visual: azul eléctrico y tarjetas uniformes
- El usuario rechazó la apariencia actual por no coincidir con la presentación conceptual y pidió explícitamente conservar el azul eléctrico, usar iconos reales/reconocibles y eliminar las tarjetas multicolores.
- Se revisó app.py y se encontró que el color de acento seguía siendo violeta y que las cuatro tarjetas de métricas tenían fondos distintos (violeta, cian, verde y naranja).
- Se modificó la paleta para dar protagonismo al azul eléctrico y cian, reducir el violeta a un acento secundario y unificar todas las tarjetas en azul sólido.
- Se reforzó el fondo azul profundo de la portada y el núcleo hexagonal con iluminación cian/azul.
- Los iconos de Telegram, WhatsApp y correo están implementados como SVG inline reconocibles; se requiere validación visual en Streamlit Cloud y captura Android para ajustar escala/visibilidad.
- No afirmar que la interfaz ya coincide con la presentación hasta revisar el despliegue real.


## 📝 2026-11-22 — Rediseño integral conforme a la presentación enviada
- El usuario compartió la lámina visual que considera la propuesta oficial de BOT FACTORY AI y pidió que toda la aplicación, incluidas sus secciones, se parezca a ella.
- Se identificaron los elementos a reproducir: logo hexagonal, mascota robot, cerebro IA, holograma hexagonal sobre plataforma orbital, frase “Crea. Conecta. Automatiza.”, botones de Telegram/WhatsApp/Email y franja de iconos de aplicación.
- Se reemplazó la portada genérica por una composición de marca con SVG propios y efectos CSS de iluminación, órbitas y flotación.
- Se amplió el sistema visual a todas las secciones internas con fondos azul noche, bordes eléctricos, paneles sólidos azul profundo, botones azules y tipografía clara. Se evita usar tarjetas multicolores genéricas; los tres botones de canal conservan sus colores identificativos.
- Se mantiene responsive para móvil y escritorio. La apariencia final debe validarse en el despliegue real después del redeploy de Streamlit Cloud.
- Los cambios visuales no modifican el estado de integración funcional: Supabase Auth/RLS, persistencia, correo y WhatsApp siguen pendientes.

- Refinamiento adicional aplicado a la navegación lateral y encabezados de todas las secciones: se eliminan emojis genéricos de la navegación y se utiliza el lenguaje visual hexagonal/azul eléctrico de la marca.


## 📝 2026-11-22 — Segunda revisión visual completa tras feedback del usuario
- El usuario volvió a señalar diferencias con la lámina: logotipo principal, bloque derecho, robot y tarjetas.
- Se inspeccionó app.py y se detectó que la mascota era una figura SVG simplificada y que la franja de iconos inferior no tenía tarjetas visuales independientes.
- Se redibujó la mascota SVG con casco metálico, visor, ojos cian, torso, brazos y emblema hexagonal.
- Se ampliaron y equilibraron las tres ilustraciones de la cabecera; se mejoró el tamaño y la jerarquía del logo de la zona derecha, la composición del holograma y los botones de Telegram/WhatsApp/Email.
- Se añadieron tarjetas oscuras individuales a la franja inferior de iconos, con borde azul eléctrico y resplandor cian.
- Se reforzaron las tarjetas métricas del centro de operaciones y los contenedores de todas las secciones con fondos azules uniformes, bordes luminosos y sombras internas.
- Ajustes responsive incluidos para móvil.
- Pendiente: usuario debe compartir captura del nuevo despliegue para validar escalas y recortes. Para alcanzar el aspecto 3D de la lámina se requerirán ilustraciones de alta calidad, ya que los SVG/CSS actuales son aproximaciones vectoriales.


## 📝 2026-11-22 — Ajuste de fidelidad y dinamismo tras nueva referencia
- El usuario volvió a compartir la lámina de identidad y pidió aplicar CSS y todos los ajustes necesarios para que la aplicación se vea igual y dinámica.
- Se comparó la estructura real de app.py con la lámina. Se detectó barra de marca redundante sobre el hero, escala insuficiente en los tres elementos de la cabecera, panel holográfico bajo de altura, tarjetas inferiores poco definidas y exceso de estilos anteriores superpuestos.
- Se ocultó la barra genérica únicamente en Inicio para que la composición comience directamente con logo principal, mascota y cerebro IA.
- Se reforzaron proporciones y tamaños de cabecera, panel central 50/50, bloque de marca derecho, logotipo, slogan y botones de canales.
- Se reconstruyó la franja inferior en siete tarjetas: Icono App, Icono Circular, Icono Simple, Telegram, WhatsApp, Email y Favicon.
- Se agregaron efectos de partículas, rotación continua de órbitas, pulso de plataforma holográfica, hover en canales/tarjetas y brillos cian/azul eléctrico.
- Se normalizaron métricas y paneles internos al azul profundo de la identidad, sin multicolor arbitrario.
- Se incorporaron ajustes responsive y respeto a preferencias de movimiento reducido.
- Commit app.py: c79100b7d4659fa4e1d9224c7b342924c1a0c926.
- Pendiente: verificar visualmente el despliegue en Streamlit Cloud y realizar ajustes finales con captura de Android. No declarar igualdad exacta hasta validar.


## 📝 2026-11-22 — Modernización integral de navegación y sistema visual

### 📌 Diagnóstico
- Se revisó la versión vigente de app.py y se confirmó que la barra lateral seguía usando una navegación Streamlit estándar con radio sin tratamiento de marca.
- El CSS acumulaba varias redefiniciones de los mismos selectores, lo que hacía que los estilos fueran difíciles de mantener y provocaba inconsistencias visuales.
- La portada ya tenía composición holográfica y tarjetas inferiores, pero los elementos internos necesitaban una jerarquía más consistente.

### 📝 Cambios publicados
- Se rediseñó la cabecera de la barra lateral con símbolo hexagonal SVG, nombre de marca y descriptor.
- Se mejoró la navegación con etiquetas visuales por sección, estado activo azul eléctrico, hover, espaciado y agrupación.
- Se organizaron preferencias, selector de vista demostrativa y estado de conectores en paneles compactos.
- Se incorporó un pie de barra lateral de marca.
- Se añadió una capa final de CSS unificado para normalizar paneles, métricas, encabezados, botones y estados.
- Se mantuvo el azul eléctrico/cian como paleta principal y el fondo azul noche; las tarjetas métricas se mantienen uniformes.
- Se conservaron Streamlit/Python y las funciones actuales; no se migró a React ni se cambió la arquitectura.

### 📊 Estado y límites
- Commit app.py: 585ddd42d3a0537512f36da62189a11cb955f445.
- Publicado en la rama main.
- El CSS de Streamlit depende de selectores del DOM de Streamlit; el aspecto final debe validarse en el despliegue real.
- No se ha confirmado visualmente el render en Streamlit Cloud. No afirmar que la interfaz coincide exactamente con la lámina hasta recibir captura de la aplicación.
- El rediseño es visual: no convierte login/registro, roles ni conectores pendientes en funciones productivas.


## 📝 2026-11-23 — Renovación visual de la documentación del repositorio

### 🎯 Objetivo
- El usuario solicitó completar el README principal y aplicar un estilo visual inspirado en el repositorio privado CxP_VENEZUELA_JH_no_usar.
- Se tomó como referencia su cabecera con insignias superiores, botones grandes de navegación, resumen ejecutivo, tablas, diagramas y árbol del repositorio.

### ✅ Cambios documentales
- Se amplió README.md desde un encabezado mínimo a una presentación completa del proyecto BOT FACTORY AI.
- Se añadieron badges superiores para tecnologías, canales y estado real del MVP, más botones de navegación a la documentación.
- Se incorporaron resumen del proyecto, matriz de funcionalidades, arquitectura Mermaid, canales, instalación, seguridad, despliegue, estructura, roadmap y contribución.
- Se añadieron iconos temáticos a encabezados de los Markdown técnicos y comerciales.
- Se conservan las decisiones y el historial acumulado de memoria.md y bitacora_acumulada.md.

### ⚠️ Criterios de precisión
- Telegram se describe como MVP de código pendiente de validación real.
- Correo, WhatsApp, Supabase Auth/RLS, persistencia, multiempresa y pagos se identifican como planificados o pendientes.
- No se inventa una URL pública de Streamlit ni se declara licencia de distribución.
- El repositorio de referencia es privado; su README fue accesible mediante la conexión GitHub autorizada para esta revisión.

### 📌 Pendiente
- Revisar visualmente el README en GitHub y ajustar detalles si el render final lo requiere.
- Mantener esta convención visual en los Markdown que se creen en adelante.
