#!/bin/sh

git ls-files --modified | fzf --preview 'git diff --color=always {}'
