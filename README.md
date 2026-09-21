# lawrence-skills

Personal library of agent skills in the [Agent Skills](https://agentskills.io) format: one folder per skill, each with a `SKILL.md` plus optional `references/`, `assets/` and `scripts/`. The same folders work in Claude Code, OpenAI Codex CLI, OpenCode and other tools that read `SKILL.md`.

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

### Install into a project with APM

The repo is installable as an [Agent Package Manager](https://microsoft.github.io/apm/) package with no extra manifest. In the consuming project:

```bash
apm install Lagyamfi/lawrence-skills#v0.2.0 --target claude,codex,opencode
```

APM records the dependency in `apm.yml`, pins it in `apm.lock.yaml`, and deploys every skill to `.claude/skills/<name>/` and to the converged `.agents/skills/<name>/` directory that Codex, OpenCode, Cursor, Copilot and Gemini read. Pin a tag or commit (`#v0.2.0`, `#<sha>`) so the project does not drift; `apm update` moves the pin. For a private repo, export `GITHUB_TOKEN` (for example `export GITHUB_TOKEN=$(gh auth token)`) before installing. Commit `apm.yml`, `apm.lock.yaml` and the deployed skill directories; `apm_modules/` is git-ignored automatically.

Choose one mechanism per machine for global use (`install.sh` symlinks or `apm install -g`), not both, or the two will fight over the same directories.

## Add a skill

1. Create `skills/<kebab-name>/SKILL.md` with frontmatter `name` (must equal the folder name) and `description` (what it does and when to use it; this is what the agent matches on).
2. Keep `SKILL.md` under 500 lines. Put detail in `references/`, fill-in templates in `assets/`, helpers in `scripts/`, and tell the agent in `SKILL.md` which file to load when.
3. Stick to portable frontmatter (`name`, `description`). Tool-specific keys are ignored elsewhere.
4. Run `scripts/validate.py` and re-run `./install.sh`.

## Validate

```bash
scripts/validate.py                       # structure, frontmatter, links, rule ids
scripts/validate.py --book API.en.html    # also checks every book anchor (download the book HTML first)
uvx --from 'git+https://github.com/agentskills/agentskills#subdirectory=skills-ref' skills-ref validate skills/api-design
```

The last line is the reference validator from the Agent Skills specification; run it on every skill before tagging a release.

## Release

Tag releases so consumers can pin them: `git tag v0.2.0 && git push --tags`. Bump `metadata.version` in the changed skill's `SKILL.md` in the same commit.

## Test a skill

Skills are prompts, so test them like prompts: give each tool a realistic task and compare the output against what the skill should produce.

- Trigger test: describe the task without naming the skill (for example "review this OpenAPI file") and confirm the skill was picked up.
- Output test: check that the result uses the skill's procedure, cites rule IDs, and loads only the reference files it needs.
- Regression: keep a few sample inputs and expected findings under `skills/<name>/tests/` and re-run after edits.

Findings from testing go back into `SKILL.md` or the references, then validate, commit, pull everywhere.

## Licence notes

`api-design` is a paraphrased, non-commercial derivative of *The API* (CC BY-NC 4.0). Keep the attribution and links if you share it.
