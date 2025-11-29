"""Tournament state and result models."""

from pydantic import BaseModel, Field
import ujson

from adversarial_tournament.models.persona import PersonaSet


class RoundOneOutput(BaseModel):
    """Output from Round 1: Initial Drafts."""

    contestant_1_draft: str = Field(description="Complete draft from Contestant 1")
    contestant_2_draft: str = Field(description="Complete draft from Contestant 2")


class RoundTwoCritique(BaseModel):
    """Output from Round 2: The Roast."""

    critique_of_contestant_1: str = Field(
        description="Brutal critique of Contestant 1's draft"
    )
    critique_of_contestant_2: str = Field(
        description="Brutal critique of Contestant 2's draft"
    )
    key_issues: list[str] = Field(
        description="List of the most critical issues identified across both drafts"
    )


class RoundThreeOutput(BaseModel):
    """Output from Round 3: The Synthesis."""

    collaboration_discussion: str = Field(
        description="Brief discussion between contestants about addressing feedback"
    )
    final_output: str = Field(
        description="The unified final output addressing all critiques"
    )


class TournamentResult(BaseModel):
    """Complete tournament result with all rounds and metadata."""

    task: str = Field(description="The original task description")
    personas: PersonaSet = Field(description="The personas used in this tournament")
    round_one: RoundOneOutput = Field(description="Round 1 results")
    round_two: RoundTwoCritique = Field(description="Round 2 results")
    round_three: RoundThreeOutput = Field(description="Round 3 results")

    def to_json(self) -> str:
        """Machine-readable JSON output using ujson."""
        return ujson.dumps(self.model_dump(), indent=2)

    def to_markdown(self) -> str:
        """Human-readable markdown transcript."""
        issues_md = "\n".join(f"- {issue}" for issue in self.round_two.key_issues)

        return f"""# Adversarial Tournament Results

## Task
{self.task}

---

## Personas Generated

### Contestant 1: {self.personas.contestant_1.name}
- **Role**: {self.personas.contestant_1.role}
- **Goal**: {self.personas.contestant_1.goal}
- **Communication Style**: {self.personas.contestant_1.communication_style}
- **Key Traits**: {", ".join(self.personas.contestant_1.key_traits)}

**Backstory**: {self.personas.contestant_1.backstory}

### Contestant 2: {self.personas.contestant_2.name}
- **Role**: {self.personas.contestant_2.role}
- **Goal**: {self.personas.contestant_2.goal}
- **Communication Style**: {self.personas.contestant_2.communication_style}
- **Key Traits**: {", ".join(self.personas.contestant_2.key_traits)}

**Backstory**: {self.personas.contestant_2.backstory}

### Judge: {self.personas.judge.name}
- **Role**: {self.personas.judge.role}
- **Goal**: {self.personas.judge.goal}
- **Communication Style**: {self.personas.judge.communication_style}
- **Key Traits**: {", ".join(self.personas.judge.key_traits)}

**Backstory**: {self.personas.judge.backstory}

**Persona Selection Reasoning**: {self.personas.reasoning}

---

## Round 1: Initial Drafts

### {self.personas.contestant_1.name}'s Draft

{self.round_one.contestant_1_draft}

---

### {self.personas.contestant_2.name}'s Draft

{self.round_one.contestant_2_draft}

---

## Round 2: The Roast

### {self.personas.judge.name}'s Critique

**Critique of {self.personas.contestant_1.name}:**

{self.round_two.critique_of_contestant_1}

---

**Critique of {self.personas.contestant_2.name}:**

{self.round_two.critique_of_contestant_2}

---

**Key Issues Identified:**
{issues_md}

---

## Round 3: The Synthesis

### Collaboration Discussion

{self.round_three.collaboration_discussion}

---

## Final Output

{self.round_three.final_output}
"""
