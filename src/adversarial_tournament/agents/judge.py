"""Judge Agent Factory - Creates dynamic adversarial judge agents from personas."""

from pydantic_ai import Agent

from adversarial_tournament.models.persona import Persona
from adversarial_tournament.models.tournament import RoundTwoCritique
from adversarial_tournament.prompts.templates import build_judge_prompt


def create_judge_agent(
    persona: Persona,
    model: str = "openai:gpt-4o-mini",
) -> Agent[None, RoundTwoCritique]:
    """Create a judge agent from a persona definition.

    Judges provide brutal, constructive critique in Round 2.

    Args:
        persona: The persona definition for this judge.
        model: The model identifier (e.g., 'openai:gpt-4o-mini').

    Returns:
        A configured Pydantic AI Agent for adversarial critique.
    """
    return Agent(
        model,
        output_type=RoundTwoCritique,
        instructions=build_judge_prompt(persona),
    )
