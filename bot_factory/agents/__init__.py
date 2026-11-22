"""Motor inicial de definición y administración de agentes IA."""
from .models import AgentSpec
from .registry import create_agent_spec

__all__ = ["AgentSpec", "create_agent_spec"]
