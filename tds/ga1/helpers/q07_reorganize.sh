#!/usr/bin/env bash
# Run inside the extracted folder (the one that contains docs/, content/, ...).
set -euo pipefail
rm -f README.md                     # the zip's instructions file is not part of the expected tree
find . -type f -name '*.txt' -print0 | while IFS= read -r -d '' file; do
  category=$(grep -m 1 '^category:' "$file" | cut -d' ' -f2- | tr -d '\r')
  rel=${file#./}                    # drop leading ./
  new=$(printf '%s' "$rel" | tr '/' '-')
  mkdir -p "$category"
  mv "$file" "$category/$new"
done
find . -type d -empty -delete
find . -type f | LC_ALL=C sort | sha256sum
