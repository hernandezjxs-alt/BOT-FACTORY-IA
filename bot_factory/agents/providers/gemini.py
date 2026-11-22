"""Adaptador Google Gemini usando el SDK oficial google-genai."""
import os
from .base import ProviderNotConfigured
from ..models import AgentSpec

class GeminiProvider:
    """Proveedor Gemini. Lee la API key solo desde secretos o entorno."""
    name = "google"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    def generate(self, agent: AgentSpec, user_message: str) -> str:
        if not self.api_key:
            raise ProviderNotConfigured("Falta GEMINI_API_KEY. Configura una clave desde Google AI Studio en el entorno privado; no la pegues en el panel ni en GitHub.")
        if not user_message or not user_message.strip():
            raise ValueError("El mensaje del usuario no puede estar vacío.")
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise ProviderNotConfigured("Falta el SDK google-genai. Instala dependencias con pip install -r requirements.txt.") from exc
        client = genai.Client(api_key=self.api_key)
        system_instruction = (
            f"Tu nombre es {agent.name}. Tu rol es: {agent.role}.\n"
            f"Instrucciones del agente:\n{agent.instructions}\n"
            "Responde de forma clara, útil y segura. No afirmes haber ejecutado acciones externas si no tienes una herramienta habilitada."
        )
        response = client.models.generate_content(
            model=agent.model or self.model,
            contents=user_message.strip(),
            config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.3),
        )
        answer = getattr(response, "text", None)
        if not answer:
            raise RuntimeError("Gemini no devolvió texto. Revisa filtros, cuotas y disponibilidad del modelo.")
        return answer.strip()
