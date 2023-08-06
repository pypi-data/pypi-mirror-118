#!/bin/sh

git status | awk '/modified/ { print $2 }' | fzf --preview \
	'git diff --color=always {}'
