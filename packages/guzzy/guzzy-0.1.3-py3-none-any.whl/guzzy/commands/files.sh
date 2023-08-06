#!/bin/sh

[ "$1" ] && commit_hash="$1" || commit_hash="HEAD"

commit="git --no-pager show -q $commit_hash"
limiter="-------------------------------------------------"

file_content="git show $commit_hash:{}"

git ls-tree -r --name-only "$commit_hash" |
    fzf --ansi --preview "$commit && echo $limiter && $file_content" \
        --preview-window=right:70%
