# 📌 Agent Factory Engine — MVP fundacional

Este paquete define agentes IA independientes de los canales de mensajería.

## 📌 Qué incluye
- Modelo declarativo `AgentSpec` con nombre, rol, instrucciones, proveedor, modelo, canal, herramientas y tenant.
- Validación centralizada para evitar definiciones incompletas.
- Contrato `ModelProvider` para conectar Claude/Anthropic, OpenAI, Google u otros proveedores.
- Adaptador placeholder que falla de forma explícita mientras no exista integración real.

## 📌 Qué todavía no hace
- No ejecuta inferencia ni llama a modelos.
- No almacena agentes permanentemente.
- No ejecuta herramientas ni acciones externas.
- No gestiona credenciales ni conversaciones.

## 🔐 Seguridad y siguiente paso
Nunca añadir API keys a `AgentSpec`, al panel, ni al repositorio. Los proveedores reales deberán resolver credenciales desde variables de entorno/secret manager y aplicar límites, auditoría y aislamiento por tenant. Claude Pro no implica acceso a la API de Anthropic; el uso de API requiere credenciales y facturación/API habilitada por separado.

## 📌 Ejemplo

```python
from bot_factory.agents import create_agent_spec

agent = create_agent_spec(
    name="Asistente comercial",
    role="Asesor de ventas",
    instructions="Responde con claridad y deriva casos complejos a una persona.",
    provider="anthropic",
    model="",
    channel="telegram",
    tools=(),
)
print(agent.to_dict())
```

## 🧠 Proveedor Gemini inicial

- Adaptador: `GeminiProvider` en `providers/gemini.py`.
- SDK oficial: `google-genai`.
- Configuración: `GEMINI_API_KEY` y `GEMINI_MODEL` mediante variables de entorno o secretos del despliegue.
- Modelo predeterminado: `gemini-2.5-flash-lite`, sujeto a disponibilidad y cuotas de Google.
- El panel incluye una prueba de conversación para agentes configurados con proveedor `google`.
- La API key no se almacena en el registro del agente, Streamlit ni GitHub.
- El nivel gratuito tiene límites y condiciones de privacidad diferentes al nivel de pago. No enviar datos confidenciales de clientes al nivel gratuito.
- Integración pendiente de validación real con una clave configurada en un entorno local o despliegue.
