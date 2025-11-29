"""Agent factories for tournament participants."""

from adversarial_tournament.agents.persona_generator import create_persona_generator
from adversarial_tournament.agents.contestant import create_contestant_agent
from adversarial_tournament.agents.judge import create_judge_agent

__all__ = [
    "create_persona_generator",
    "create_contestant_agent",
    "create_judge_agent",
]
