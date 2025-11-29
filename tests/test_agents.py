"""Unit tests for agent factories."""

import pytest

from adversarial_tournament.agents import (
    create_persona_generator,
    create_contestant_agent,
    create_judge_agent,
)
from adversarial_tournament.models.persona import Persona, PersonaSet
from adversarial_tournament.models.tournament import RoundTwoCritique


class TestAgentFactories:
    """Tests for agent factory functions."""

    @pytest.fixture
    def sample_contestant_persona(self) -> Persona:
        """Create a sample contestant persona for testing."""
        return Persona(
            name="The Engineer",
            role="Senior Technical Writer",
            goal="Ensure technical accuracy and completeness",
            backstory="10 years of experience in technical documentation.",
            persona_type="contestant",
            key_traits=["analytical", "precise", "thorough"],
            communication_style="Technical and detailed",
        )

    @pytest.fixture
    def sample_judge_persona(self) -> Persona:
        """Create a sample judge persona for testing."""
        return Persona(
            name="The Angry Customer",
            role="Affected User",
            goal="Get a genuine apology and commitment to improvement",
            backstory="Lost critical data during the outage.",
            persona_type="judge",
            key_traits=["skeptical", "demanding", "direct"],
            communication_style="Blunt and unforgiving",
        )

    def test_create_persona_generator(self):
        """Test persona generator agent creation."""
        agent = create_persona_generator()

        # Check the agent is configured correctly
        assert agent is not None
        # The output type should be PersonaSet
        # Note: Pydantic AI stores this internally

    def test_create_persona_generator_custom_model(self):
        """Test persona generator with custom model."""
        agent = create_persona_generator(model="openai:gpt-4o")
        assert agent is not None

    def test_create_contestant_agent(self, sample_contestant_persona):
        """Test contestant agent creation from persona."""
        agent = create_contestant_agent(sample_contestant_persona)
        assert agent is not None

    def test_create_contestant_agent_custom_model(self, sample_contestant_persona):
        """Test contestant agent with custom model."""
        agent = create_contestant_agent(
            sample_contestant_persona,
            model="openai:gpt-4o",
        )
        assert agent is not None

    def test_create_judge_agent(self, sample_judge_persona):
        """Test judge agent creation from persona."""
        agent = create_judge_agent(sample_judge_persona)
        assert agent is not None

    def test_create_judge_agent_custom_model(self, sample_judge_persona):
        """Test judge agent with custom model."""
        agent = create_judge_agent(
            sample_judge_persona,
            model="openai:gpt-4o",
        )
        assert agent is not None
