#!/bin/sh

# help : list modified, uncommited files and diff for each one

git ls-files --modified | fzf --preview 'git diff --color=always {}'
