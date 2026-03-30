#!/bin/bash
# check_local_knowledge.sh - 检查本地知识库中是否有相关内容

KEYWORD="${1:-1panel}"
DOC_DIR="./skills/doc-web-assistant-skill"

echo "🔍 检查本地知识库：$KEYWORD"
echo "================================"

# 检查 fetched_doc.md
if [ -f "$DOC_DIR/fetched_doc.md" ]; then
    echo ""
    echo "📄 fetched_doc.md:"
    if grep -qi "$KEYWORD" "$DOC_DIR/fetched_doc.md"; then
        echo "   ✅ 找到相关内容"
        grep -n -i "$KEYWORD" "$DOC_DIR/fetched_doc.md" | head -5
    else
        echo "   ❌ 未找到相关内容"
    fi
else
    echo "   ⚠️  文件不存在"
fi

# 检查 doc_store
if [ -d "$DOC_DIR/doc_store" ]; then
    echo ""
    echo "📁 doc_store/:"
    if [ -f "$DOC_DIR/doc_store/chunks.json" ]; then
        if grep -qi "$KEYWORD" "$DOC_DIR/doc_store/chunks.json"; then
            echo "   ✅ 找到相关内容"
        else
            echo "   ❌ 未找到相关内容"
        fi
    else
        echo "   ⚠️  chunks.json 不存在"
    fi
else
    echo "   ⚠️  目录不存在"
fi

echo ""
echo "================================"
echo "💡 提示：如果本地没有内容，使用 web_fetch 获取文档后 import"
