"""CLI entry point for the adversarial tournament."""

import argparse
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from adversarial_tournament.tournament import AdversarialTournament
from adversarial_tournament.config import DEBUG, DEFAULT_MODEL


def main() -> int:
    """Run the adversarial tournament from command line."""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Adversarial Tournament - Multi-agent content refinement using Pydantic AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Write an apology email from Cloudflare after a major outage"
  %(prog)s "Write a press release" --output-json result.json
  %(prog)s "Write an email" --model openai:gpt-4o
  %(prog)s "Write an email" --no-auto-output
        """,
    )

    parser.add_argument(
        "task",
        help="The task/prompt for the tournament",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        metavar="FILE",
        help="Save JSON output to file",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        metavar="FILE",
        help="Save Markdown output to file",
    )
    parser.add_argument(
        "--no-auto-output",
        action="store_true",
        help="Disable auto-generated YYYY-MM-DD-OUTPUT.md file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output (overrides DEBUG setting)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress all output except final result",
    )

    args = parser.parse_args()

    # Determine verbosity
    verbose = DEBUG
    if args.verbose:
        verbose = True
    if args.quiet:
        verbose = False

    if not args.quiet:
        print(f"Starting adversarial tournament...")
        print(f"Task: {args.task}")
        print(f"Model: {args.model}")
        print()

    # Run the tournament
    tournament = AdversarialTournament(model=args.model)

    try:
        result = tournament.run_sync(args.task)
    except Exception as e:
        print(f"Error running tournament: {e}", file=sys.stderr)
        return 1

    # Auto-output (unless disabled)
    if not args.no_auto_output:
        auto_path = Path(f"{date.today()}-OUTPUT.md")
        auto_path.write_text(result.to_markdown())
        if not args.quiet:
            print(f"Saved transcript to: {auto_path}")

    # Additional outputs
    if args.output_json:
        args.output_json.write_text(result.to_json())
        if not args.quiet:
            print(f"Saved JSON to: {args.output_json}")

    if args.output_md:
        args.output_md.write_text(result.to_markdown())
        if not args.quiet:
            print(f"Saved Markdown to: {args.output_md}")

    # Print final output
    if not args.quiet:
        print()
        print("=" * 60)
        print("FINAL OUTPUT")
        print("=" * 60)
        print()

    print(result.round_three.final_output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
