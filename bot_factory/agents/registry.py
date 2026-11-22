"""Casos de uso del Agent Factory Engine."""
from .models import AgentSpec


def create_agent_spec(*, name: str, role: str, instructions: str,
                      provider: str = "manual", model: str = "",
                      channel: str = "none", tools: tuple[str, ...] = (),
                      tenant_id: str = "local-demo") -> AgentSpec:
    """Valida y construye una definición de agente; no inicia llamadas IA."""
    spec = AgentSpec(
        name=name.strip(), role=role.strip(), instructions=instructions.strip(),
        provider=provider, model=model.strip(), channel=channel,
        tools=tuple(tools), tenant_id=tenant_id,
    )
    spec.validate()
    return spec
