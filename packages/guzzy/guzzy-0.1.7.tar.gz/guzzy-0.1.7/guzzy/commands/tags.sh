#!/bin/sh

# help : list all tags with tag messages

git --no-pager tag --sort=-taggerdate -l |
    fzf --preview "git --no-pager tag -l {} --format='%(contents)'"
