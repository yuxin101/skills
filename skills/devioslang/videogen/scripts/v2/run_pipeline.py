#!/usr/bin/env python3
"""
videogen v2 — Unified Pipeline Entry Point

用法:
    python run_pipeline.py gen "AI将取代哪些职业" --mode auto
    python run_pipeline.py gen "失业后的第30天，我决定..." --mode auto
    python run_pipeline.py analyze "选题文本或URL"
    python run_pipeline.py storyboard "选题" --mode B --save storyboard.json
"""

import argparse
import json
import os
import sys
import subprocess
import time
from pathlib import Path

# ─── 路径设置 ───
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent  # skills/videogen/
MINIMAX_OUTPUT = SKILL_DIR / "minimax-output"
MINIMAX_OUTPUT.mkdir(exist_ok=True)

# 添加 minimax-multimodal 到 Python 路径
MM_DIR = SKILL_DIR.parent / "minimax-multimodal"
sys.path.insert(0, str(MM_DIR))

sys.path.insert(0, str(Path(__file__).parent))
from topic_analyzer import analyze as analyze_topic
from storyboard_generator import (
    generate_storyboard,
    save_storyboard,
    ContentSegment,
    StoryboardPanel,
)


# ─── MiniMax API Key ───

def get_minimax_key() -> str:
    key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_KEY")
    if not key:
        # 尝试从 .env 读取
        env_path = Path.home() / ".openclaw" / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if "MINIMAX" in line and "API_KEY" in line:
                    key = line.split("=")[-1].strip()
                    break
    return key or ""


# ─── TTS 配音 ───

def generate_tts(narration_text: str, output_path: str, voice: str = "female-shaonv") -> bool:
    """调用 TTS 生成配音"""
    key = get_minimax_key()
    if not key:
        print("⚠️  MINIMAX_API_KEY 未设置，跳过 TTS")
        return False

    tts_script = MM_DIR / "scripts" / "tts" / "generate_voice.py"
    cmd = [
        sys.executable, str(tts_script), "tts",
        narration_text,
        "-v", voice,
        "-o", str(output_path),
    ]
    try:
        env = os.environ.copy()
        env["MINIMAX_API_KEY"] = key
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)
        if result.returncode == 0:
            print(f"  ✅ TTS: {output_path}")
            return True
        else:
            print(f"  ⚠️ TTS 失败: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ⚠️ TTS 异常: {e}")
        return False


# ─── 视频片段生成 ───

def generate_video_clip(
    prompt: str,
    first_frame: str = "",
    mode: str = "t2v",
    duration: int = 6,
    output: str = "",
) -> bool:
    """调用 Hailuo 生成视频片段"""
    key = get_minimax_key()
    if not key:
        print("  ⚠️  MINIMAX_API_KEY 未设置，跳过视频生成")
        return False

    video_script = MM_DIR / "scripts" / "video" / "generate_video.py"
    cmd = [
        sys.executable, str(video_script),
        "--mode", mode,
        "--prompt", prompt,
        "--duration", str(duration),
        "--resolution", "768P",
        "--output", output,
    ]
    if first_frame:
        cmd += ["--first-frame", first_frame]

    try:
        env = os.environ.copy()
        env["MINIMAX_API_KEY"] = key
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, env=env)
        if result.returncode == 0:
            print(f"  ✅ 视频片段: {output}")
            return True
        else:
            err = result.stderr
            # 处理 usage limit
            if "usage limit exceeded" in err or "2056" in err:
                print(f"  ⚠️  额度耗尽，跳过: {output}")
            else:
                print(f"  ⚠️  视频生成失败: {err[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  视频生成超时: {output}")
        return False
    except Exception as e:
        print(f"  ⚠️  视频生成异常: {e}")
        return False


# ─── 指令解析 ───

def cmd_analyze(args):
    """分析选题"""
    result = analyze_topic(args.topic)
    print(f"\n{'='*50}")
    print(f"📊 选题模式分析")
    print(f"{'='*50}")
    print(f"推荐模式: Mode {result.mode}")
    print(f"置信度: {result.confidence:.0%}")
    print(f"推理: {result.reasoning}")
    print(f"模式说明: {result.mode_description}")
    print(f"推荐开场钩子:")
    for h in result.suggested_hooks:
        print(f"  • {h}")


def cmd_storyboard(args):
    """生成分镜"""
    # 自动模式检测
    if args.mode == "auto":
        analysis = analyze_topic(args.topic)
        mode = analysis.mode
        print(f"🔍 自动检测结果: Mode {mode}（{analysis.mode_description}）")
    else:
        mode = args.mode

    # 估算配音段落
    segments = []
    if args.narrations:
        for i, n in enumerate(args.narrations):
            segments.append(ContentSegment(segment_id=i+1, narration=n, duration=12))

    result = generate_storyboard(
        topic=args.topic,
        mode=mode,
        narration_segments=segments or None,
        total_duration=args.duration,
    )

    output_path = args.save or str(MINIMAX_OUTPUT / "storyboard.json")
    save_storyboard(result, output_path)

    print(f"\n📋 分镜摘要")
    print(f"  模式: Mode {result['mode']} ({result['summary']['mode_description']})")
    print(f"  镜头数: {result['summary']['total_panels']}")
    print(f"  预计时长: {result['summary']['total_duration']}s")


def cmd_gen(args):
    """
    完整流水线：选题 → 分析 → 分镜 → TTS → AI视频 → 混剪
    """
    print(f"\n{'='*55}")
    print(f"🎬 videogen v2 自动化流水线")
    print(f"{'='*55}")
    start_time = time.time()

    # ── Step 1: 选题分析 ──
    print(f"\n[Step 1/6] 选题分析...")
    if args.mode == "auto":
        analysis = analyze_topic(args.topic)
        mode = analysis.mode
        print(f"  → 自动选择 Mode {mode}: {analysis.mode_description}")
        print(f"  → 置信度: {analysis.confidence:.0%}")
    else:
        mode = args.mode
        print(f"  → 指定 Mode {mode}")

    # ── Step 2: 分镜生成 ──
    print(f"\n[Step 2/6] 生成分镜...")
    storyboard = generate_storyboard(
        topic=args.topic,
        mode=mode,
        total_duration=args.duration,
    )
    storyboard_path = MINIMAX_OUTPUT / "storyboard.json"
    save_storyboard(storyboard, str(storyboard_path))
    print(f"  → 生成了 {storyboard['summary']['total_panels']} 个镜头")

    # ── Step 3: TTS 配音 ──
    print(f"\n[Step 3/6] 生成配音...")
    narration_text = " ".join(p["narration"] for p in storyboard["panels"] if p["narration"])
    voice_path = MINIMAX_OUTPUT / "voiceover.mp3"
    if narration_text.strip():
        generate_tts(narration_text, str(voice_path))
    else:
        print(f"  ⚠️  无配音文本")

    # ── Step 4: 生成 AI 视频片段（关键帧动画化）──
    print(f"\n[Step 4/6] 生成 AI 视频片段...")
    clips_dir = MINIMAX_OUTPUT / "clips"
    clips_dir.mkdir(exist_ok=True)

    # 找出需要 AI 视频的镜头（video_prompt 非空的）
    video_panels = [p for p in storyboard["panels"] if p.get("video_prompt")]
    print(f"  → 需要生成视频的镜头: {len(video_panels)}")

    for i, panel in enumerate(video_panels[:6]):  # 最多6个，避免额度耗尽
        clip_path = clips_dir / f"clip_{panel['panel_number']:02d}.mp4"
        prompt = panel["video_prompt"]
        duration = panel.get("duration", 6)
        scene_type = panel.get("scene_type", "")

        # 剧情类用 i2v（如果有图），知识类用 t2v
        if scene_type == "剧情场景" and panel.get("description"):
            # 先用描述生成图，再用 i2v（简化版：直接 t2v）
            mode_v = "t2v"
        else:
            mode_v = "t2v"

        print(f"  [{i+1}/{min(len(video_panels),6)}] 镜头{panel['panel_number']}...", end=" ")
        ok = generate_video_clip(
            prompt=prompt,
            mode=mode_v,
            duration=min(duration, 10),
            output=str(clip_path),
        )
        if not ok:
            print(f"跳过")

    # ── Step 5: 混剪合成 ──
    print(f"\n[Step 5/6] FFmpeg 混剪...")
    composite_path = MINIMAX_OUTPUT / "video_complete.mp4"
    # 检查是否有生成的片段
    existing_clips = sorted(clips_dir.glob("clip_*.mp4"))
    if existing_clips:
        # 简单 concat（每个片段6秒）
        concat_list = clips_dir / "concat_list.txt"
        with open(concat_list, "w") as f:
            for clip in existing_clips:
                f.write(f"file '{clip.name}'\n")

        concat_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c:v", "libx264", "-crf", "22", "-preset", "fast",
            str(composite_path),
        ]
        result = subprocess.run(concat_cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"  ✅ 混剪完成: {composite_path}")
        else:
            print(f"  ⚠️  混剪失败: {result.stderr[:200]}")
    else:
        print(f"  ⚠️  无视频片段，跳过混剪")

    # ── Step 6: 添加配音 ──
    print(f"\n[Step 6/6] 添加配音...")
    final_path = MINIMAX_OUTPUT / "video_final.mp4"
    if composite_path.exists() and voice_path.exists():
        add_audio_cmd = [
            "ffmpeg", "-y",
            "-i", str(composite_path),
            "-i", str(voice_path),
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
            str(final_path),
        ]
        result = subprocess.run(add_audio_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"  ✅ 最终视频: {final_path}")
            print(f"\n{'='*55}")
            print(f"🎉 完成！总耗时: {time.time() - start_time:.1f}s")
        else:
            print(f"  ⚠️  添加配音失败")
    else:
        print(f"  ⚠️  缺少素材，跳过最终合成")

    print(f"\n📁 输出目录: {MINIMAX_OUTPUT}/")
    for f in sorted(MINIMAX_OUTPUT.rglob("*")):
        if f.is_file():
            size = f.stat().st_size / 1024
            print(f"  {f.name:30s} {size:>8.1f} KB")


# ─── 主入口 ───

def main():
    parser = argparse.ArgumentParser(description="videogen v2 — 视频号 AI 短视频流水线")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # analyze 子命令
    p_analyze = sub.add_parser("analyze", help="分析选题，推荐内容模式")
    p_analyze.add_argument("topic", help="选题文本或URL")

    # storyboard 子命令
    p_sb = sub.add_parser("storyboard", help="生成分镜脚本")
    p_sb.add_argument("topic", help="选题")
    p_sb.add_argument("--mode", default="auto", choices=["A", "B", "C", "auto"],
                      help="内容模式（auto=自动检测）")
    p_sb.add_argument("--duration", type=int, default=60, help="目标时长(秒)")
    p_sb.add_argument("--narrations", nargs="+", help="旁白/台词片段")
    p_sb.add_argument("--save", help="保存路径")

    # gen 子命令（完整流水线）
    p_gen = sub.add_parser("gen", help="运行完整流水线")
    p_gen.add_argument("topic", help="选题")
    p_gen.add_argument("--mode", default="auto", choices=["A", "B", "C", "auto"],
                       help="内容模式（auto=自动检测）")
    p_gen.add_argument("--duration", type=int, default=60, help="目标时长(秒)")

    args = parser.parse_args()

    if args.cmd == "analyze":
        cmd_analyze(args)
    elif args.cmd == "storyboard":
        cmd_storyboard(args)
    elif args.cmd == "gen":
        cmd_gen(args)


if __name__ == "__main__":
    main()
