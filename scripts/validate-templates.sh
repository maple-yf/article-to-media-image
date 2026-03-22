#!/bin/bash
echo "Validating slide card templates..."
for file in /Users/mapleyf/projects/myDev/article-to-media-image/templates/*.html; do
  count=$(grep -c 'slide-card' "$file" 2>/dev/null || echo "0")
  if [ "$count" -gt 0 ]; then
    echo "✓ $file has $count slide cards"
  else
    echo "✗ $file has no slide cards"
  fi
done
