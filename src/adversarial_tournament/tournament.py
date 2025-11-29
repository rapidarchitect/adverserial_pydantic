"""Main tournament orchestrator using Pydantic AI."""

import asyncio
from dataclasses import dataclass, field

from pydantic_ai import Agent

from adversarial_tournament.config import DEFAULT_MODEL
from adversarial_tournament.models.persona import PersonaSet
from adversarial_tournament.models.tournament import (
    TournamentResult,
    RoundOneOutput,
    RoundTwoCritique,
    RoundThreeOutput,
)
from adversarial_tournament.agents.persona_generator import create_persona_generator
from adversarial_tournament.agents.contestant import create_contestant_agent
from adversarial_tournament.agents.judge import create_judge_agent
from adversarial_tournament.prompts.templates import (
    build_round_one_prompt,
    build_round_two_prompt,
    build_round_three_prompt,
)


@dataclass
class AdversarialTournament:
    """Orchestrates the adversarial tournament process.

    The tournament follows this flow:
    1. Phase 0: Generate personas based on the task
    2. Round 1: Both contestants create drafts (parallel execution)
    3. Round 2: Judge critiques both drafts
    4. Round 3: Contestants synthesize feedback into final output
    """

    model: str = field(default=DEFAULT_MODEL)

    async def run(self, task: str) -> TournamentResult:
        """Run the full tournament asynchronously.

        Args:
            task: The task description for the tournament.

        Returns:
            TournamentResult containing all rounds and the final output.
        """
        # Phase 0: Generate personas
        personas = await self._generate_personas(task)

        # Round 1: Parallel drafts
        round_one = await self._run_round_one(task, personas)

        # Round 2: Judge critique
        round_two = await self._run_round_two(task, personas, round_one)

        # Round 3: Synthesis
        round_three = await self._run_round_three(
            task, personas, round_one, round_two
        )

        return TournamentResult(
            task=task,
            personas=personas,
            round_one=round_one,
            round_two=round_two,
            round_three=round_three,
        )

    def run_sync(self, task: str) -> TournamentResult:
        """Run the tournament synchronously.

        Args:
            task: The task description for the tournament.

        Returns:
            TournamentResult containing all rounds and the final output.
        """
        return asyncio.run(self.run(task))

    async def _generate_personas(self, task: str) -> PersonaSet:
        """Phase 0: Generate personas based on the task."""
        agent = create_persona_generator(self.model)
        result = await agent.run(f"Create personas for this task: {task}")
        return result.output

    async def _run_round_one(
        self, task: str, personas: PersonaSet
    ) -> RoundOneOutput:
        """Round 1: Run both contestants in parallel with asyncio.gather()."""
        agent_1 = create_contestant_agent(personas.contestant_1, self.model)
        agent_2 = create_contestant_agent(personas.contestant_2, self.model)

        prompt_1 = build_round_one_prompt(personas.contestant_1, task)
        prompt_2 = build_round_one_prompt(personas.contestant_2, task)

        # Parallel execution using asyncio.gather()
        result_1, result_2 = await asyncio.gather(
            agent_1.run(prompt_1),
            agent_2.run(prompt_2),
        )

        return RoundOneOutput(
            contestant_1_draft=result_1.output,
            contestant_2_draft=result_2.output,
        )

    async def _run_round_two(
        self, task: str, personas: PersonaSet, round_one: RoundOneOutput
    ) -> RoundTwoCritique:
        """Round 2: Judge critiques both drafts."""
        agent = create_judge_agent(personas.judge, self.model)

        prompt = build_round_two_prompt(
            judge_persona=personas.judge,
            contestant_1_persona=personas.contestant_1,
            contestant_2_persona=personas.contestant_2,
            task=task,
            draft_1=round_one.contestant_1_draft,
            draft_2=round_one.contestant_2_draft,
        )

        result = await agent.run(prompt)
        return result.output

    async def _run_round_three(
        self,
        task: str,
        personas: PersonaSet,
        round_one: RoundOneOutput,
        round_two: RoundTwoCritique,
    ) -> RoundThreeOutput:
        """Round 3: Synthesis - contestant 1 leads collaboration."""
        # Create synthesis agent with contestant 1's persona but synthesis instructions
        agent: Agent[None, RoundThreeOutput] = Agent(
            self.model,
            output_type=RoundThreeOutput,
            instructions=f"""You are {personas.contestant_1.name}, {personas.contestant_1.role}.

You are now collaborating with {personas.contestant_2.name} to synthesize the best
final output incorporating all feedback from the judge.

Your goal is to create a unified output that addresses every criticism and combines
the best elements of both drafts.""",
        )

        prompt = build_round_three_prompt(
            contestant_1_persona=personas.contestant_1,
            contestant_2_persona=personas.contestant_2,
            judge_persona=personas.judge,
            task=task,
            draft_1=round_one.contestant_1_draft,
            draft_2=round_one.contestant_2_draft,
            critique_1=round_two.critique_of_contestant_1,
            critique_2=round_two.critique_of_contestant_2,
            key_issues=round_two.key_issues,
        )

        result = await agent.run(prompt)
        return result.output
