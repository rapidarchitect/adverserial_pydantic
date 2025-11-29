"""Adversarial Tournament - Multi-agent adversarial prompting with Pydantic AI."""

from adversarial_tournament.tournament import AdversarialTournament
from adversarial_tournament.models.tournament import TournamentResult
from adversarial_tournament.models.persona import Persona, PersonaSet

__all__ = [
    "AdversarialTournament",
    "TournamentResult",
    "Persona",
    "PersonaSet",
]
