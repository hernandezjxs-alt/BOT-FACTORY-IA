"""Modelos de configuración de agentes, sin dependencias de proveedores."""
from dataclasses import asdict, dataclass, field
from typing import Any


SUPPORTED_PROVIDERS = ("anthropic", "openai", "google", "manual")
SUPPORTED_CHANNELS = ("none", "telegram", "email", "whatsapp")


@dataclass(frozen=True)
class AgentSpec:
    """Definición declarativa de un agente IA.

    No contiene API keys ni tokens. Las credenciales se resolverán en runtime
    desde un gestor de secretos asociado al tenant.
    """
    name: str
    role: str
    instructions: str
    provider: str = "manual"
    model: str = ""
    channel: str = "none"
    tools: tuple[str, ...] = field(default_factory=tuple)
    tenant_id: str = "local-demo"

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("El agente necesita un nombre.")
        if not self.role.strip():
            raise ValueError("El agente necesita una especialidad o rol.")
        if not self.instructions.strip():
            raise ValueError("El agente necesita instrucciones.")
        if self.provider not in SUPPORTED_PROVIDERS:
            raise ValueError("Proveedor no soportado.")
        if self.channel not in SUPPORTED_CHANNELS:
            raise ValueError("Canal no soportado.")
        if len(self.instructions) > 12000:
            raise ValueError("Las instrucciones superan el máximo de 12.000 caracteres.")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tools"] = list(self.tools)
        return data
