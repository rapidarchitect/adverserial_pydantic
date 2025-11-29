"""End-to-end tests for the adversarial tournament.

These tests require a valid OPENAI_API_KEY environment variable.
Run with: uv run pytest tests/test_e2e.py -v -m slow
"""

import os
import pytest

from adversarial_tournament import AdversarialTournament, TournamentResult


# Skip all tests in this module if no API key is available
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set",
)


@pytest.mark.slow
class TestEndToEnd:
    """End-to-end tournament tests."""

    @pytest.mark.asyncio
    async def test_full_tournament_async(self):
        """Test running a complete tournament asynchronously."""
        tournament = AdversarialTournament(model="openai:gpt-4o-mini")

        result = await tournament.run(
            "Write an apology email from a SaaS company after a 4-hour outage"
        )

        # Verify result structure
        assert isinstance(result, TournamentResult)
        assert result.task is not None
        assert result.personas is not None
        assert result.round_one is not None
        assert result.round_two is not None
        assert result.round_three is not None

        # Verify personas were generated
        assert result.personas.contestant_1.name
        assert result.personas.contestant_2.name
        assert result.personas.judge.name

        # Verify drafts were created
        assert len(result.round_one.contestant_1_draft) > 100
        assert len(result.round_one.contestant_2_draft) > 100

        # Verify critique was generated
        assert len(result.round_two.critique_of_contestant_1) > 50
        assert len(result.round_two.key_issues) > 0

        # Verify final output
        assert len(result.round_three.final_output) > 100

    def test_full_tournament_sync(self):
        """Test running a complete tournament synchronously."""
        tournament = AdversarialTournament(model="openai:gpt-4o-mini")

        result = tournament.run_sync(
            "Write a brief press release announcing a new product feature"
        )

        assert isinstance(result, TournamentResult)
        assert result.round_three.final_output

    def test_tournament_produces_valid_markdown(self):
        """Test that tournament output produces valid markdown."""
        tournament = AdversarialTournament(model="openai:gpt-4o-mini")

        result = tournament.run_sync("Write a customer notification about scheduled maintenance")

        markdown = result.to_markdown()

        # Check markdown structure
        assert "# Adversarial Tournament Results" in markdown
        assert "## Task" in markdown
        assert "## Personas Generated" in markdown
        assert "## Round 1: Initial Drafts" in markdown
        assert "## Round 2: The Roast" in markdown
        assert "## Round 3: The Synthesis" in markdown
        assert "## Final Output" in markdown

    def test_tournament_produces_valid_json(self):
        """Test that tournament output produces valid JSON."""
        import ujson

        tournament = AdversarialTournament(model="openai:gpt-4o-mini")

        result = tournament.run_sync("Write an internal announcement about office policy changes")

        json_output = result.to_json()

        # Verify it's valid JSON
        parsed = ujson.loads(json_output)

        assert parsed["task"]
        assert parsed["personas"]
        assert parsed["round_one"]
        assert parsed["round_two"]
        assert parsed["round_three"]


@pytest.mark.slow
class TestCloudflareApology:
    """Specific test case: Cloudflare-style apology email."""

    def test_cloudflare_apology(self):
        """Test the Cloudflare apology scenario."""
        tournament = AdversarialTournament()

        result = tournament.run_sync(
            "Generate a public apology email from Cloudflare after a major outage "
            "that affected millions of websites for 2 hours"
        )

        final_output = result.round_three.final_output.lower()

        # The apology should contain key elements
        assert any(word in final_output for word in ["apolog", "sorry", "regret"])
        assert any(word in final_output for word in ["outage", "incident", "disruption"])
