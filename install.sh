#!/usr/bin/env bash
# Install every skill in ./skills into the skill directories of the coding agents on this machine.
#
# Usage:
#   ./install.sh                 # symlink skills into all known targets that exist (or are created)
#   ./install.sh --copy          # copy instead of symlink (for tools that do not follow symlinks)
#   ./install.sh --targets ~/.codex/skills,~/.claude/skills
#   ./install.sh --only api-design
#   ./install.sh --uninstall
#
# Default targets:
#   ~/.claude/skills            Claude Code (work profile)
#   ~/.claude-personal/skills   Claude Code (personal profile, via CLAUDE_CONFIG_DIR)
#   ~/.codex/skills             OpenAI Codex CLI
#   ~/.config/opencode/skills   OpenCode (it also reads ~/.claude/skills)
#
# Re-running is safe: existing links are replaced, copies are refreshed, foreign directories are left alone.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
MODE="link"
ONLY=""
UNINSTALL=0
TARGETS=(
  "$HOME/.claude/skills"
  "$HOME/.claude-personal/skills"
  "$HOME/.codex/skills"
  "$HOME/.config/opencode/skills"
)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy) MODE="copy"; shift ;;
    --link) MODE="link"; shift ;;
    --targets) IFS=',' read -r -a TARGETS <<< "${2/#\~/$HOME}"; shift 2 ;;
    --only) ONLY="$2"; shift 2 ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
done

# Expand ~ in targets given via --targets
for i in "${!TARGETS[@]}"; do TARGETS[$i]="${TARGETS[$i]/#\~/$HOME}"; done

skills=()
for d in "$SKILLS_DIR"/*/; do
  name="$(basename "$d")"
  [[ -f "$d/SKILL.md" ]] || { echo "skip $name: no SKILL.md" >&2; continue; }
  [[ -n "$ONLY" && "$name" != "$ONLY" ]] && continue
  skills+=("$name")
done
[[ ${#skills[@]} -gt 0 ]] || { echo "no skills found in $SKILLS_DIR" >&2; exit 1; }

owned_by_repo() {
  # true if path is a symlink into this repo, or a copy carrying our marker
  local p="$1"
  if [[ -L "$p" ]]; then
    [[ "$(readlink "$p")" == "$SKILLS_DIR"/* ]]
  elif [[ -d "$p" ]]; then
    [[ -f "$p/.installed-from" && "$(cat "$p/.installed-from")" == "$REPO_DIR" ]]
  else
    return 1
  fi
}

for target in "${TARGETS[@]}"; do
  # Only create the tool's directory if its parent config dir exists (i.e. the tool is present),
  # except for the two Claude profiles which we always support.
  parent="$(dirname "$target")"
  if [[ ! -d "$parent" ]]; then
    echo "-- $target: parent $parent not found, skipping (tool not installed?)"
    continue
  fi
  mkdir -p "$target"
  echo "-- $target"
  for name in "${skills[@]}"; do
    src="$SKILLS_DIR/$name"
    dst="$target/$name"
    if [[ $UNINSTALL -eq 1 ]]; then
      if owned_by_repo "$dst"; then rm -rf "$dst"; echo "   removed $name"; else echo "   left $name (not installed from this repo)"; fi
      continue
    fi
    if [[ -e "$dst" || -L "$dst" ]] && ! owned_by_repo "$dst"; then
      echo "   ! $name exists and was not installed from this repo; leaving it. Remove it manually to replace."
      continue
    fi
    rm -rf "$dst"
    if [[ "$MODE" == "link" ]]; then
      ln -s "$src" "$dst"; echo "   linked $name"
    else
      cp -R "$src" "$dst"; echo "$REPO_DIR" > "$dst/.installed-from"; echo "   copied $name"
    fi
  done
done

echo
echo "Done. Verify inside each tool (e.g. type /api-design in Claude Code, or ask it to review an API)."
echo "If a tool does not pick up symlinked skills, re-run with --copy."
