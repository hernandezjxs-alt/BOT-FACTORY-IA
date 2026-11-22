"""Contrato común para proveedores de modelos IA."""
from typing import Protocol
from ..models import AgentSpec


class ModelProvider(Protocol):
    name: str

    def generate(self, agent: AgentSpec, user_message: str) -> str:
        """Genera una respuesta usando credenciales obtenidas de forma segura."""
        ...


class ProviderNotConfigured(RuntimeError):
    """El proveedor no está configurado o su adaptador no está habilitado."""


class PlaceholderProvider:
    """Adaptador deliberadamente no operativo para el MVP sin credenciales."""
    def __init__(self, name: str):
        self.name = name

    def generate(self, agent: AgentSpec, user_message: str) -> str:
        raise ProviderNotConfigured(
            f"El proveedor {self.name} aún no está conectado. Configura su API oficial "
            "y un gestor seguro de secretos antes de habilitar conversaciones."
        )
