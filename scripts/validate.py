#!/usr/bin/env python3
"""Validate every skill in ./skills against the Agent Skills conventions and this repo's rules.

Checks per skill:
  - SKILL.md exists with YAML frontmatter containing `name` and `description`
  - `name` matches the folder name and is kebab-case
  - description is non-empty and under 1024 characters
  - SKILL.md body is under 500 lines (progressive disclosure: put detail in references/)
  - every relative Markdown link or backticked path in SKILL.md, references/ and templates/ resolves to a file
  - every http(s) link to the API book anchors an id that exists (only if --book <API.en.html> is given)
  - rule IDs cited in SKILL.md, checklist and templates are defined in references/rules/*.md (api-design specific)

Usage: scripts/validate.py [--book path/to/API.en.html]
Exit code 1 on any error.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def check_links(skill_dir):
    md_files = list(skill_dir.rglob("*.md"))
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        # markdown links [x](path) that are relative
        for target in re.findall(r"\]\((?!https?://|#)([^)]+)\)", text):
            p = (f.parent / target.split("#")[0]).resolve()
            if not p.exists():
                err(f"{f.relative_to(ROOT)}: broken link -> {target}")
        # backticked relative paths ending in .md or / that look like repo paths
        for target in re.findall(r"`((?:\.\./|references/|templates/|rules/|scripts/)[^`\s]*)`", text):
            if any(ch in target for ch in "*<>N"):
                continue  # glob-like placeholders such as rules/0N-*.md
            p = (f.parent / target).resolve()
            if not p.exists():
                err(f"{f.relative_to(ROOT)}: path in backticks does not exist -> {target}")


def check_book_anchors(skill_dir, book_html):
    ids = set(re.findall(r'id="([a-z0-9-]+)"', book_html))
    for f in skill_dir.rglob("*.md"):
        for a in re.findall(r"API\.en\.html#([a-z0-9-]+)", f.read_text(encoding="utf-8")):
            if a not in ids:
                err(f"{f.relative_to(ROOT)}: book anchor not found -> #{a}")


def check_rule_ids(skill_dir):
    rules_dir = skill_dir / "references" / "rules"
    if not rules_dir.exists():
        return
    defined = set()
    for f in rules_dir.glob("*.md"):
        defined |= set(re.findall(r"^- ([IDPBHSQ]\d{1,2}-\d{1,2}):", f.read_text(encoding="utf-8"), re.M))
    additions = skill_dir / "references" / "additions.md"
    if additions.exists():
        defined |= set(re.findall(r"^- (X\d{1,3}):", additions.read_text(encoding="utf-8"), re.M))
    cited = {}
    for f in [skill_dir / "SKILL.md", *(skill_dir / "references").glob("*.md"), *(skill_dir / "templates").glob("*.md")]:
        if not f.exists():
            continue
        for rid in re.findall(r"\b([IDPBHSQ]\d{1,2}-\d{1,2}|X\d{1,3})\b", f.read_text(encoding="utf-8")):
            cited.setdefault(rid, f)
    for rid, f in sorted(cited.items()):
        if rid not in defined:
            err(f"{f.relative_to(ROOT)}: rule id cited but not defined -> {rid}")
    print(f"    rule ids: {len(defined)} defined, {len(cited)} cited")


def main():
    book_html = None
    if "--book" in sys.argv:
        book_html = pathlib.Path(sys.argv[sys.argv.index("--book") + 1]).read_text(encoding="utf-8", errors="ignore")

    if not SKILLS.exists():
        err("skills/ directory missing")
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        name = skill_dir.name
        print(f"== {name}")
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            err(f"{name}: SKILL.md missing")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm is None:
            err(f"{name}: SKILL.md has no YAML frontmatter")
        else:
            if fm.get("name") != name:
                err(f"{name}: frontmatter name '{fm.get('name')}' != folder name")
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
                err(f"{name}: folder name is not kebab-case")
            desc = fm.get("description", "")
            if not desc:
                err(f"{name}: description missing")
            elif len(desc) > 1024:
                err(f"{name}: description is {len(desc)} chars (>1024)")
            extra = set(fm) - {"name", "description", "license", "metadata", "compatibility", "allowed-tools"}
            if extra:
                warn(f"{name}: frontmatter has non-portable keys {sorted(extra)} (other agents may ignore them)")
        lines = text.count("\n") + 1
        print(f"    SKILL.md: {lines} lines")
        if lines > 500:
            err(f"{name}: SKILL.md is {lines} lines (>500); move detail into references/")
        check_links(skill_dir)
        if book_html:
            check_book_anchors(skill_dir, book_html)
        check_rule_ids(skill_dir)

    for w in warnings:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
