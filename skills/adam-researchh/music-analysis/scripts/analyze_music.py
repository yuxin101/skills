#!/usr/bin/env python3
import argparse, json, math, subprocess, statistics
from pathlib import Path


def ffprobe_meta(path: Path):
    cmd = [
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-print_format", "json", str(path)
    ]
    out = subprocess.check_output(cmd, text=True)
    j = json.loads(out)
    astream = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), {})
    return {
        "duration_sec": float(j.get("format", {}).get("duration", 0) or 0),
        "sample_rate": int(astream.get("sample_rate", 0) or 0),
        "channels": int(astream.get("channels", 0) or 0),
        "codec": astream.get("codec_name"),
    }


def analyze_with_librosa(path: Path):
    import numpy as np
    import librosa

    y, sr = librosa.load(path, sr=None, mono=True)
    if y.size == 0:
        return {"error": "empty audio"}

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    # librosa may return scalar or 1-element ndarray depending on backend/version
    try:
        tempo = float(tempo)
    except Exception:
        import numpy as np
        tempo = float(np.atleast_1d(tempo)[0])

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    key_idx = int(chroma_mean.argmax())
    key_guess = notes[key_idx]

    rms = librosa.feature.rms(y=y)[0]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

    # coarse section boundaries via onset strength novelty peaks
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    peaks = librosa.util.peak_pick(
        onset_env,
        pre_max=16,
        post_max=16,
        pre_avg=16,
        post_avg=16,
        delta=0.5,
        wait=16,
    )
    times = librosa.frames_to_time(peaks, sr=sr)
    coarse_sections = [round(float(t), 2) for t in times[:30]]

    return {
        "tempo_bpm": round(tempo, 2),
        "key_estimate": key_guess,
        "energy": {
            "rms_mean": round(float(rms.mean()), 6),
            "rms_std": round(float(rms.std()), 6),
            "rms_p95": round(float(np.percentile(rms, 95)), 6),
        },
        "spectral": {
            "centroid_mean": round(float(centroid.mean()), 2),
            "rolloff_mean": round(float(rolloff.mean()), 2),
            "contrast_mean": [round(float(x), 3) for x in contrast.mean(axis=1)],
        },
        "coarse_section_boundaries_sec": coarse_sections,
        "analysis_notes": [
            "Key estimate is best-effort (mode/tonic ambiguity possible).",
            "Section boundaries are novelty-based coarse markers, not labeled verse/chorus.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()

    p = Path(args.audio).expanduser()
    if not p.exists():
        raise SystemExit(f"audio not found: {p}")

    report = {"file": str(p), "meta": ffprobe_meta(p)}

    try:
        report["music"] = analyze_with_librosa(p)
        report["engine"] = "librosa"
    except Exception as e:
        report["engine"] = "ffprobe-only"
        report["music"] = {
            "error": f"librosa analysis unavailable: {e}",
            "hint": "Create local venv and install librosa+numpy for full analysis."
        }

    out_text = json.dumps(report, indent=2)
    if args.out:
        Path(args.out).write_text(out_text)
    if args.json or not args.out:
        print(out_text)


if __name__ == "__main__":
    main()
