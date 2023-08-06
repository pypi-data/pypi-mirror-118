#!/bin/sh

CWD="$(dirname "$(readlink -f "$0")")"

show_diff="git log --color=always -n 1 {1}; seq -s_ 150|tr -d '[:digit:]' && \
  git diff --color=always {1}~ {1}"

git log --color=always --format="%C(auto)%h %s" | fzf --ansi \
  --preview="$show_diff" --preview-window=right:55% \
  --bind "ctrl-t:execute($CWD/files.sh {1})"
