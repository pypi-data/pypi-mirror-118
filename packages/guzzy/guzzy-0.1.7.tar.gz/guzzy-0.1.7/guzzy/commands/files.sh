#!/bin/sh

# help : list all files in specified commit/tag/branch with preview
# arg1 : commit - commit hash, branch or tag name

[ "$1" ] && commit_hash="$1" || commit_hash="HEAD"

commit="git --no-pager log --color=always -n 1 $commit_hash"
delimiter="seq -s_ 150 | tr -d '[:digit:]'"
file_content="git show $commit_hash:{}"
pager="bat --style numbers --decorations always --file-name {}"

git ls-tree -r --name-only "$commit_hash" |
    fzf --ansi --preview "$commit && $delimiter && $file_content | $pager" \
        --preview-window=right:70%
