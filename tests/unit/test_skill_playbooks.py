"""Guardrail tests for code-health playbooks, SKILL.md links, and README boundaries."""

from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "code-health"
REFS_DIR = SKILL_DIR / "references"

EXPECTED_PLAYBOOKS: tuple[str, ...] = (
    "python",
    "java",
    "java-spring",
    "javascript",
    "typescript",
    "react",
    "nextjs",
    "angular",
)

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PENALTY_RE = re.compile(r"-\d+(?:\.\d+)?\s*pts", re.IGNORECASE)


def _find_broken_links(md_path: Path) -> list[str]:
    """Return unresolvable relative Markdown link targets inside ``md_path``."""
    broken: list[str] = []
    text = md_path.read_text(encoding="utf-8")
    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://")):
            continue
        resolved = (md_path.parent / target).resolve()
        if not resolved.exists():
            broken.append(f"{md_path.name} -> {raw_target}")
    return broken


def test_all_supported_profiles_have_playbooks() -> None:
    """Every supported language and framework profile has a playbook linked in SKILL.md."""
    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    missing_files: list[str] = []
    missing_links: list[str] = []

    for profile in EXPECTED_PLAYBOOKS:
        filename = f"{profile}-playbook.md"
        playbook_path = REFS_DIR / filename
        if not playbook_path.is_file() or not playbook_path.read_text(encoding="utf-8").strip():
            missing_files.append(filename)
        if f"references/{filename}" not in skill_text:
            missing_links.append(filename)

    assert not missing_files, f"Missing or empty playbooks: {missing_files}"
    assert not missing_links, f"Playbooks not linked in SKILL.md: {missing_links}"


def test_readme_contains_no_scoring_rules() -> None:
    """Root README delegates scoring rules to the rubric and playbooks."""
    readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "Code Health Rules" not in readme_text
    assert not PENALTY_RE.search(readme_text), "README.md must not list penalty points"
    assert "scoring-rubric.md" in readme_text


def test_skill_and_playbook_links_resolve() -> None:
    """All relative Markdown links inside SKILL.md and references/*.md exist on disk."""
    markdown_files = [SKILL_DIR / "SKILL.md", *sorted(REFS_DIR.glob("*.md"))]
    broken_links: list[str] = []
    for md_file in markdown_files:
        broken_links.extend(_find_broken_links(md_file))

    assert markdown_files, "Expected Markdown documentation files under skills/code-health"
    assert not broken_links, f"Broken relative links found: {broken_links}"

