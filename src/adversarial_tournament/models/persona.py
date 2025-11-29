"""Persona models for dynamic agent generation."""

from typing import Literal
from pydantic import BaseModel, Field


class Persona(BaseModel):
    """Defines a persona for dynamic agent creation."""

    name: str = Field(description="A descriptive name for the persona (e.g., 'The Engineer')")
    role: str = Field(description="The role title (e.g., 'Technical Expert')")
    goal: str = Field(description="What this persona aims to achieve in the tournament")
    backstory: str = Field(description="Background context that shapes the persona's perspective")
    persona_type: Literal["contestant", "judge"] = Field(
        description="Whether this is a content creator (contestant) or critic (judge)"
    )
    key_traits: list[str] = Field(
        description="3-5 key personality traits that define behavior",
        min_length=3,
        max_length=5,
    )
    communication_style: str = Field(
        description="How this persona communicates (e.g., 'technical and precise', 'empathetic and diplomatic')"
    )


class PersonaSet(BaseModel):
    """A complete set of personas for a tournament."""

    contestant_1: Persona = Field(description="First content creator persona")
    contestant_2: Persona = Field(description="Second content creator persona")
    judge: Persona = Field(description="Adversarial critic persona")
    task_context: str = Field(description="The original task being addressed")
    reasoning: str = Field(
        description="Explanation of why these personas were chosen for this task"
    )
