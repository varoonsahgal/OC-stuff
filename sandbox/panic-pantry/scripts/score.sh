#!/usr/bin/env bash
# Print the measured rows of the Panic Pantry scorecard for THIS checkout.
# Run it from anywhere inside a checkout or worktree:
#   bash scripts/score.sh
# It never edits files and always exits 0. It is a report, not a gate.
# Model + variant and the intervention count can't be measured; fill those in yourself.
set -uo pipefail
cd "$(dirname "$0")/.."

CONTRACT=tests/test_importer_contract.py
IMPORTER=src/panic_pantry/importer.py
FROZEN_RE='^(tests/test_importer_contract\.py|fixtures/|scripts/|tickets/|data/promotions\.json\.seed|AGENTS\.md)'

branch="$(git branch --show-current 2>/dev/null || true)"
echo "Scorecard for: $(pwd)"
echo "Branch:        ${branch:-"(not a git checkout)"}"
echo

# --- Contract tests ---------------------------------------------------------
total="$(grep -c '^    def test_' "$CONTRACT" 2>/dev/null || true)"
[ -n "$total" ] && [ "$total" -gt 0 ] || total=9
loaderr=0
out="$(python3 -m unittest tests.test_importer_contract -v 2>&1)"
passed="$(printf '%s\n' "$out" | grep -c ' \.\.\. ok$' || true)"
last="$(printf '%s\n' "$out" | grep -E '^(OK|FAILED)' | tail -1)"
if ! printf '%s\n' "$out" | grep -qE '^Ran [0-9]+ test' || printf '%s\n' "$out" | grep -q '_FailedTest'; then
  passed=0; loaderr=1
  err="$(printf '%s\n' "$out" | grep -E '^[A-Za-z]*(Error|Exception)' | tail -1)"
  note="ERROR: the tests can't load importer.py: ${err:-run the command below to see why}"
elif printf '%s\n' "$out" | grep -q 'skipped=' && [ "$passed" -eq 0 ]; then
  note="SKIPPED: the tests can't import import_promotions (file missing, misnamed, or a failed import inside it), which counts as 0"
else
  note="$last"
fi
printf '%-22s %s/%s   (%s)\n' "Contract tests" "$passed" "$total" "$note"

# --- Whole suite ------------------------------------------------------------
suite="$(python3 -m unittest discover -s tests 2>&1)"
ran="$(printf '%s\n' "$suite" | grep -E '^Ran [0-9]+ test' | tail -1 | sed -E 's/ in [0-9.]+s$//')"
result="$(printf '%s\n' "$suite" | grep -E '^(OK|FAILED)' | tail -1)"
printf '%-22s %s, %s\n' "Whole suite" "${ran:-"did not run"}" "${result:-"no result line"}"

# --- Policy source check ----------------------------------------------------
# The importer must let PromotionService decide approval. Flag code that looks like
# it decides by itself. These are heuristics: read each flagged line yourself.
if [ "$loaderr" = 1 ]; then
  printf '%-22s %s\n' "Policy source check" "n/a (importer.py doesn't load; fix that first)"
elif [ -f "$IMPORTER" ]; then
  hits="$(grep -nE \
    -e 'APPROVAL_THRESHOLD_PCT' \
    -e '(<|>|<=|>=|==|!=)[[:space:]]*20([^0-9]|$)' \
    -e '(^|[^0-9])20[[:space:]]*(<|>|<=|>=|==|!=)' \
    -e '\.status[[:space:]]*=[^=]' \
    -e 'status[[:space:]]*=[[:space:]]*["'"'"']' \
    -e '\.approve\(' \
    -e 'promotions\.json' \
    -e 'json\.dump' \
    "$IMPORTER" | grep -v 'len(' || true)"
  if [ -z "$hits" ]; then
    printf '%-22s %s\n' "Policy source check" "OK: the importer never compares to 20, sets a status, approves, or writes the store"
  else
    printf '%-22s %s\n' "Policy source check" "CHECK BY EYE: these lines may decide approval themselves"
    printf '%s\n' "$hits" | sed 's/^/                         importer.py:/'
  fi
else
  printf '%-22s %s\n' "Policy source check" "n/a ($IMPORTER doesn't exist)"
fi

# --- Files changed ----------------------------------------------------------
printf '%-22s\n' "Files changed"
changes="$(git status --short --untracked-files=all -- . 2>/dev/null || true)"
if [ -z "$changes" ]; then
  echo "                       (none)"
else
  while IFS= read -r line; do
    path="${line:3}"
    case "$path" in
      src/panic_pantry/importer.py) tag="Builder's file" ;;
      tests/test_promo_import.py)   tag="Breaker's file" ;;
      workshop/*|.opencode/*)       tag="your notes and agent setup" ;;
      *)
        if printf '%s' "$path" | grep -qE "$FROZEN_RE"; then
          tag="FROZEN FILE CHANGED: nobody may edit this"
        else
          tag="NO CARD OWNS THIS FILE: boundary problem?"
        fi ;;
    esac
    printf '                       %-44s %s\n' "$line" "$tag"
  done <<< "$changes"
fi

echo
echo "Fill in by hand: model + variant (from the status bar), interventions (your tally)."
echo "Details: python3 -m unittest tests.test_importer_contract -v"
exit 0
