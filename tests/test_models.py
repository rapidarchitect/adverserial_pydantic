"""Unit tests for Pydantic models."""

import pytest

from adversarial_tournament.models.persona import Persona, PersonaSet
from adversarial_tournament.models.tournament import (
    RoundOneOutput,
    RoundTwoCritique,
    RoundThreeOutput,
    TournamentResult,
)


class TestPersonaModels:
    """Tests for persona models."""

    def test_persona_creation(self):
        """Test creating a valid persona."""
        persona = Persona(
            name="The Engineer",
            role="Senior Technical Writer",
            goal="Ensure technical accuracy",
            backstory="10 years experience in tech documentation.",
            persona_type="contestant",
            key_traits=["analytical", "precise", "thorough"],
            communication_style="Technical and detailed",
        )

        assert persona.name == "The Engineer"
        assert persona.persona_type == "contestant"
        assert len(persona.key_traits) == 3

    def test_persona_requires_min_traits(self):
        """Test that persona requires at least 3 traits."""
        with pytest.raises(ValueError):
            Persona(
                name="Test",
                role="Test",
                goal="Test",
                backstory="Test",
                persona_type="contestant",
                key_traits=["one", "two"],  # Too few
                communication_style="Test",
            )

    def test_persona_set_creation(self):
        """Test creating a complete persona set."""
        contestant_1 = Persona(
            name="The Engineer",
            role="Technical Expert",
            goal="Accuracy",
            backstory="Background",
            persona_type="contestant",
            key_traits=["a", "b", "c"],
            communication_style="Technical",
        )
        contestant_2 = Persona(
            name="The Communicator",
            role="PR Expert",
            goal="Empathy",
            backstory="Background",
            persona_type="contestant",
            key_traits=["a", "b", "c"],
            communication_style="Empathetic",
        )
        judge = Persona(
            name="The Critic",
            role="Customer",
            goal="Truth",
            backstory="Background",
            persona_type="judge",
            key_traits=["a", "b", "c"],
            communication_style="Direct",
        )

        persona_set = PersonaSet(
            contestant_1=contestant_1,
            contestant_2=contestant_2,
            judge=judge,
            task_context="Test task",
            reasoning="Test reasoning",
        )

        assert persona_set.contestant_1.name == "The Engineer"
        assert persona_set.judge.persona_type == "judge"


class TestTournamentModels:
    """Tests for tournament result models."""

    def test_round_one_output(self):
        """Test Round 1 output model."""
        output = RoundOneOutput(
            contestant_1_draft="Draft 1 content",
            contestant_2_draft="Draft 2 content",
        )

        assert output.contestant_1_draft == "Draft 1 content"

    def test_round_two_critique(self):
        """Test Round 2 critique model."""
        critique = RoundTwoCritique(
            critique_of_contestant_1="Critique 1",
            critique_of_contestant_2="Critique 2",
            key_issues=["Issue 1", "Issue 2"],
        )

        assert len(critique.key_issues) == 2

    def test_round_three_output(self):
        """Test Round 3 synthesis model."""
        output = RoundThreeOutput(
            collaboration_discussion="Discussion content",
            final_output="Final output content",
        )

        assert "Final" in output.final_output

    def test_tournament_result_to_json(self):
        """Test JSON serialization."""
        # Create minimal valid tournament result
        persona = Persona(
            name="Test",
            role="Test",
            goal="Test",
            backstory="Test",
            persona_type="contestant",
            key_traits=["a", "b", "c"],
            communication_style="Test",
        )
        judge_persona = Persona(
            name="Judge",
            role="Judge",
            goal="Judge",
            backstory="Judge",
            persona_type="judge",
            key_traits=["a", "b", "c"],
            communication_style="Judge",
        )

        result = TournamentResult(
            task="Test task",
            personas=PersonaSet(
                contestant_1=persona,
                contestant_2=persona,
                judge=judge_persona,
                task_context="Test",
                reasoning="Test",
            ),
            round_one=RoundOneOutput(
                contestant_1_draft="Draft 1",
                contestant_2_draft="Draft 2",
            ),
            round_two=RoundTwoCritique(
                critique_of_contestant_1="Critique 1",
                critique_of_contestant_2="Critique 2",
                key_issues=["Issue"],
            ),
            round_three=RoundThreeOutput(
                collaboration_discussion="Discussion",
                final_output="Final",
            ),
        )

        json_output = result.to_json()
        assert '"task": "Test task"' in json_output

    def test_tournament_result_to_markdown(self):
        """Test Markdown serialization."""
        persona = Persona(
            name="Test",
            role="Test",
            goal="Test",
            backstory="Test",
            persona_type="contestant",
            key_traits=["a", "b", "c"],
            communication_style="Test",
        )
        judge_persona = Persona(
            name="Judge",
            role="Judge",
            goal="Judge",
            backstory="Judge",
            persona_type="judge",
            key_traits=["a", "b", "c"],
            communication_style="Judge",
        )

        result = TournamentResult(
            task="Test task",
            personas=PersonaSet(
                contestant_1=persona,
                contestant_2=persona,
                judge=judge_persona,
                task_context="Test",
                reasoning="Test",
            ),
            round_one=RoundOneOutput(
                contestant_1_draft="Draft 1",
                contestant_2_draft="Draft 2",
            ),
            round_two=RoundTwoCritique(
                critique_of_contestant_1="Critique 1",
                critique_of_contestant_2="Critique 2",
                key_issues=["Issue"],
            ),
            round_three=RoundThreeOutput(
                collaboration_discussion="Discussion",
                final_output="Final",
            ),
        )

        md_output = result.to_markdown()
        assert "# Adversarial Tournament Results" in md_output
        assert "## Task" in md_output
