# 🔌 Conectores

Cada canal debe implementarse como un módulo independiente.

Estructura prevista:
- `telegram/`: bots, comandos, mensajes y webhooks.
- `email/`: recepción, envío y clasificación de correo.
- `whatsapp/`: integración mediante API/proveedor oficial.

No guardar tokens ni credenciales en estos módulos. Leer secretos desde variables de entorno o un gestor seguro.
