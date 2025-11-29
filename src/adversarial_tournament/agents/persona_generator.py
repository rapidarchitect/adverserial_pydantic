"""Persona Generator Agent - Analyzes tasks and creates appropriate personas."""

from pydantic_ai import Agent

from adversarial_tournament.models.persona import PersonaSet
from adversarial_tournament.prompts.templates import build_persona_generator_prompt


def create_persona_generator(model: str = "openai:gpt-4o-mini") -> Agent[None, PersonaSet]:
    """Create the persona generator agent.

    This agent analyzes the input task and generates three personas:
    - Two contestant personas with complementary expertise
    - One adversarial judge persona representing affected stakeholders

    Args:
        model: The model identifier (e.g., 'openai:gpt-4o-mini').

    Returns:
        A configured Pydantic AI Agent for persona generation.
    """
    return Agent(
        model,
        output_type=PersonaSet,
        instructions=build_persona_generator_prompt(),
    )
