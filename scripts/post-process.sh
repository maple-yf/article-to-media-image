#!/bin/bash
# HTML 后处理脚本
# 用法: scripts/post-process.sh <html_file>

set -e

HTML_FILE="$1"

if [ -z "$HTML_FILE" ]; then
  echo "用法: $0 <html_file>"
  exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
  echo "错误: 文件不存在: $HTML_FILE"
  exit 1
fi

echo "后处理: $HTML_FILE"

# 备份原文件
cp "$HTML_FILE" "${HTML_FILE}.bak"

# 确保 container 使用 min-height
sed -i.tmp 's/height: 1440px/min-height: 1440px/g' "$HTML_FILE"
rm -f "${HTML_FILE}.tmp"

# 确保没有 margin: 0 auto
sed -i.tmp 's/margin: 0 auto;/margin: 0;/g' "$HTML_FILE"
rm -f "${HTML_FILE}.tmp"

# 确保宽度固定
sed -i.tmp 's/max-width: 1080px/width: 1080px/g' "$HTML_FILE"
rm -f "${HTML_FILE}.tmp"

echo "✅ 后处理完成"
