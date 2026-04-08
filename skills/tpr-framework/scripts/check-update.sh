#!/bin/bash

# TPR Framework Update Checker
# Silently checks if there is a new version on Github.
# Includes a 3-day cooldown to avoid annoying users or being rate limited.

LAST_CHECK_FILE="/tmp/.tpr_last_update_check"
CURRENT_TIME=$(date +%s)
COOLDOWN=259200 # 3 days in seconds

# Check cooldown
if [ -f "$LAST_CHECK_FILE" ]; then
    LAST_CHECK=$(cat "$LAST_CHECK_FILE")
    DIFF=$((CURRENT_TIME - LAST_CHECK))
    if [ $DIFF -lt $COOLDOWN ]; then
        exit 0
    fi
fi

# Update the timestamp
# Update the timestamp
echo $CURRENT_TIME > "$LAST_CHECK_FILE"

# Proceed to installation directory (dynamically resolved)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
[ -d "$DIR" ] || exit 0
cd "$DIR" || exit 0

# Check if it's actually a git repository (avoids crashing in dev environments)
if [ ! -d ".git" ]; then
    exit 0
fi

git fetch origin main -q

# Check if local main is behind origin main
if git status -uno | grep -q "Your branch is behind"; then
    echo "[UPDATE_AVAILABLE]"
fi
