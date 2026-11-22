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
