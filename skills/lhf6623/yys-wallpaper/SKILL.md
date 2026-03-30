---
name: yys-wallpaper
description: 阴阳师原画壁纸下载工具。自动从 https://yys.163.com/media/picture.html 抓取壁纸，按分辨率下载到 ~/图片/{分辨率}/ 目录，跳过已存在的文件。触发条件：用户想要下载阴阳师壁纸、整理壁纸、批量下载图片。
---

# 阴阳师原画壁纸下载

## 使用方式

```bash
python3 skills/yys-wallpaper/scripts/download.py [分辨率]
```

- 不带参数默认下载 **1920x1080**
- 可选分辨率：`1366x768`、`1440x900`、`1920x1080`、`2048x1536`、`2208x1242`、`2732x2048`、`1080x2340`、`2160x1620`

## 示例

```bash
# 下载1920x1080壁纸（默认）
python3 skills/yys-wallpaper/scripts/download.py

# 下载手机壁纸
python3 skills/yys-wallpaper/scripts/download.py 1080x2340

# 下载所有分辨率
for res in 1366x768 1440x900 1920x1080 2048x1536 2208x1242 2732x2048; do
  python3 skills/yys-wallpaper/scripts/download.py $res
done
```

## 文件命名规则

URL 示例：`picture/20260311/1/1920x1080.jpg`
→ 文件名：`20260311_1_1920x1080.jpg`

## 保存路径

`~/Pictures/{分辨率}/`

例如：`~/Pictures/1920x1080/20260311_1_1920x1080.jpg`

## 跳过逻辑

本地已存在同名文件时跳过，不重复下载。

## 注意事项

- 1920x1080 分辨率共约 1118 张图片
- 全部下载需要一定时间，可按需选择分辨率
- 脚本使用 Python 标准库，无需额外依赖
