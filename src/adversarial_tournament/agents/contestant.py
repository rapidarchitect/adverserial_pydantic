"""Contestant Agent Factory - Creates dynamic contestant agents from personas."""

from pydantic_ai import Agent

from adversarial_tournament.models.persona import Persona
from adversarial_tournament.prompts.templates import build_contestant_prompt


def create_contestant_agent(
    persona: Persona,
    model: str = "openai:gpt-4o-mini",
) -> Agent[None, str]:
    """Create a contestant agent from a persona definition.

    Contestants generate content in Round 1 and collaborate in Round 3.

    Args:
        persona: The persona definition for this contestant.
        model: The model identifier (e.g., 'openai:gpt-4o-mini').

    Returns:
        A configured Pydantic AI Agent for content generation.
    """
    return Agent(
        model,
        output_type=str,
        instructions=build_contestant_prompt(persona),
    )
