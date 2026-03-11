#!/usr/bin/env bash
CMD="$1"; shift 2>/dev/null; INPUT="$*"
case "$CMD" in
  page) cat << 'PROMPT'
You are an expert. Help with: 生成完整HTML页面. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  landing) cat << 'PROMPT'
You are an expert. Help with: 落地页/着陆页. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  portfolio) cat << 'PROMPT'
You are an expert. Help with: 个人作品集. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  email) cat << 'PROMPT'
You are an expert. Help with: 邮件HTML模板. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  form) cat << 'PROMPT'
You are an expert. Help with: 表单页面. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  preview) cat << 'PROMPT'
You are an expert. Help with: 代码预览. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  *) cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HTML Builder — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  page            生成完整HTML页面
  landing         落地页/着陆页
  portfolio       个人作品集
  email           邮件HTML模板
  form            表单页面
  preview         代码预览

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
    ;;
esac
