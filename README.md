# lawrence-skills

Personal library of agent skills in the [Agent Skills](https://agentskills.io) format: one folder per skill, each with a `SKILL.md` plus optional `references/`, `templates/` and `scripts/`. The same folders work in Claude Code, OpenAI Codex CLI, OpenCode and other tools that read `SKILL.md`.

## Skills

| Skill | Purpose |
|---|---|
| `api-design` | Design a new API or review an existing one against the rules distilled from *The API* by Sergey Konstantinov. Checklist, decision tables, compatibility policy, 416 referenced rules, design-doc and scorecard templates. |

## Install

```bash
git clone <this repo> ~/lawrence-skills
cd ~/lawrence-skills
./install.sh            # symlinks every skill into each agent's skills directory
```

Targets (created only if the tool's config directory exists):

| Tool | Directory |
|---|---|
| Claude Code, work profile | `~/.claude/skills/` |
| Claude Code, personal profile (`CLAUDE_CONFIG_DIR=~/.claude-personal`) | `~/.claude-personal/skills/` |
| Codex CLI | `~/.codex/skills/` |
| OpenCode | `~/.config/opencode/skills/` (OpenCode also reads `~/.claude/skills/`) |

Options: `--copy` if a tool does not follow symlinks, `--targets a,b` to choose directories, `--only <skill>`, `--uninstall`.

Because the default is symlinks, `git pull` updates every tool at once. With `--copy`, re-run `./install.sh --copy` after pulling.

Project-local use: copy or link a skill folder into `.claude/skills/`, `.codex/skills/` or `.opencode/skills/` inside the project.

## Add a skill

1. Create `skills/<kebab-name>/SKILL.md` with frontmatter `name` (must equal the folder name) and `description` (what it does and when to use it; this is what the agent matches on).
2. Keep `SKILL.md` under 500 lines. Put detail in `references/`, fill-in documents in `templates/`, helpers in `scripts/`, and tell the agent in `SKILL.md` which file to load when.
3. Stick to portable frontmatter (`name`, `description`). Tool-specific keys are ignored elsewhere.
4. Run `scripts/validate.py` and re-run `./install.sh`.

## Validate

```bash
scripts/validate.py                       # structure, frontmatter, links, rule ids
scripts/validate.py --book API.en.html    # also checks every book anchor (download the book HTML first)
```

## Test a skill

Skills are prompts, so test them like prompts: give each tool a realistic task and compare the output against what the skill should produce.

- Trigger test: describe the task without naming the skill (for example "review this OpenAPI file") and confirm the skill was picked up.
- Output test: check that the result uses the skill's procedure, cites rule IDs, and loads only the reference files it needs.
- Regression: keep a few sample inputs and expected findings under `skills/<name>/tests/` and re-run after edits.

Findings from testing go back into `SKILL.md` or the references, then validate, commit, pull everywhere.

## Licence notes

`api-design` is a paraphrased, non-commercial derivative of *The API* (CC BY-NC 4.0). Keep the attribution and links if you share it.
