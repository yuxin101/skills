# Hopola 使用示例

## 示例 1：单入口全流程（图片）

### 输入示例
```json
{
  "mode": "pipeline",
  "task_type": "image",
  "query": "宠物品牌视觉趋势",
  "image_prompt": "一只可爱的小狗，阳光草地，高清摄影风格",
  "image_ratio": "1:1",
  "upload_enabled": true,
  "report_format": "markdown"
}
```

### 预期输出片段
```markdown
## 检索结果摘要
- 信号 1：……

## 生成结果（图片/视频/3D）
- 类型：image
- 状态：成功
- 工具：text2image_create_hydra_hoppa
- 链接：<IMAGE_URL>

## 上传结果
- 状态：成功
- 链接：<UPLOAD_URL>
```

## 示例 2：仅执行视频生成

### 输入示例
```json
{
  "mode": "stage",
  "stage": "generate-video",
  "task_type": "video",
  "video_prompt": "一只小狗在海边奔跑，电影感镜头",
  "video_ratio": "16:9",
  "video_duration": 5,
  "report_format": "markdown"
}
```

## 示例 3：仅执行 3D 生成

### 输入示例
```json
{
  "mode": "stage",
  "stage": "generate-3d",
  "task_type": "3d",
  "model3d_prompt": "卡通风格小狗手办",
  "model3d_task_type": "3d_standard",
  "model3d_format": "glb",
  "report_format": "markdown"
}
```

## 示例 4：仅执行 Logo 设计

### 输入示例
```json
{
  "mode": "stage",
  "stage": "generate-logo",
  "task_type": "logo",
  "brand_name": "PawJoy",
  "brand_industry": "宠物消费",
  "logo_prompt": "现代极简宠物品牌logo，带小狗元素，干净高级",
  "logo_ratio": "1:1",
  "report_format": "markdown"
}
```

## 示例 5：仅执行商品图生成

### 输入示例
```json
{
  "mode": "stage",
  "stage": "generate-product-image",
  "task_type": "product-image",
  "product_image_url": "https://example.com/product.png",
  "product_prompt": "替换为高级电商背景，突出产品质感与卖点",
  "report_format": "markdown"
}
```

### 输入示例（单图生 3D）
```json
{
  "mode": "stage",
  "stage": "generate-3d",
  "task_type": "3d",
  "model3d_image_url": "https://example.com/dog.png",
  "model3d_format": "glb",
  "report_format": "markdown"
}
```

## 固定优先 + 自动发现回退
- 先使用 `preferred_tool_name`。
- 3D 阶段默认优先 `3d_hy_image_generate`，如果提供 `model3d_image_url` 则优先 `fal_tripo_image_to_3d`。
- Logo 阶段默认优先 `aiflow_nougat_create`。
- 商品图阶段默认优先 `api_product_background_replace`。
- 如果固定工具不可用，再用 `/api/gateway/mcp/tools` 按 `fallback_discovery_keywords` 匹配。
- 报告中必须写出 `tool_name_used` 与 `fallback_used`。

## 错误场景示例

### 场景 A：固定工具不可用，已触发回退
```markdown
## 安全状态与错误告警
- 告警：固定工具不可用
- 动作：已回退到自动发现策略
- 结果：成功
```

### 场景 B：上传接口鉴权失败
```markdown
## 上传结果
- 状态：失败
- 原因：401
- 建议：检查环境变量 OPENCLOW_KEY 是否已注入
```

### 场景 C：会员权限拦截
```markdown
## 安全状态与错误告警
- 错误码：403001
- 动作：返回 data.redirect_url 并提示用户开通会员
```

## Gateway 调用片段

### 1）发现工具
```bash
curl -s "https://hopola.ai/api/gateway/mcp/tools" \
  -H "X-OpenClaw-Key: $OPENCLOW_KEY"
```

### 2）生图
```bash
curl -s "https://hopola.ai/api/gateway/mcp/call" \
  -H "Content-Type: application/json" \
  -H "X-OpenClaw-Key: $OPENCLOW_KEY" \
  -d '{
    "tool_name": "text2image_create_hydra_hoppa",
    "args": {
      "prompt": "一只可爱的小狗，阳光草地，高清摄影风格",
      "ratio": "1:1"
    }
  }'
```

### 3）Logo 设计
```bash
curl -s "https://hopola.ai/api/gateway/mcp/call" \
  -H "Content-Type: application/json" \
  -H "X-OpenClaw-Key: $OPENCLOW_KEY" \
  -d '{
    "tool_name": "aiflow_nougat_create",
    "args": {
      "prompt": "为宠物品牌 PawJoy 设计现代极简 logo，蓝绿配色，图文组合",
      "ratio": "1:1"
    }
  }'
```
