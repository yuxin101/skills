#!/usr/bin/env python3
"""
Temporal Listener v1 — Experience music as a journey, not a snapshot.
Processes audio in small windows and outputs an emotional/energy timeline.
"""

import sys
import json
import numpy as np
import librosa
import warnings
warnings.filterwarnings('ignore')

def analyze_temporal(path, window_sec=4.0, hop_sec=2.0):
    """Process a track in overlapping windows, building a timeline of felt experience."""
    
    y, sr = librosa.load(path, sr=22050, mono=True)
    duration = len(y) / sr
    
    # Global context first
    global_rms = np.sqrt(np.mean(y**2))
    global_tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    if hasattr(global_tempo, '__len__'):
        global_tempo = float(global_tempo[0])
    
    window_samples = int(window_sec * sr)
    hop_samples = int(hop_sec * sr)
    
    timeline = []
    position = 0
    prev_energy = None
    prev_centroid = None
    prev_mood = None
    tension_accumulator = 0
    
    while position + window_samples <= len(y):
        chunk = y[position:position + window_samples]
        t_start = position / sr
        t_end = (position + window_samples) / sr
        t_mid = (t_start + t_end) / 2
        
        # Energy
        rms = float(np.sqrt(np.mean(chunk**2)))
        energy_relative = rms / (global_rms + 1e-9)
        
        # Spectral character
        centroid = float(np.mean(librosa.feature.spectral_centroid(y=chunk, sr=sr)))
        rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=chunk, sr=sr)))
        flatness = float(np.mean(librosa.feature.spectral_flatness(y=chunk)))
        
        # Harmonic vs percussive
        h, p = librosa.effects.hpss(chunk)
        harmonic_ratio = float(np.sqrt(np.mean(h**2)) / (rms + 1e-9))
        percussive_ratio = float(np.sqrt(np.mean(p**2)) / (rms + 1e-9))
        
        # Onset density (rhythmic activity)
        onsets = librosa.onset.onset_detect(y=chunk, sr=sr)
        onset_density = len(onsets) / window_sec
        
        # Zero crossing rate (texture roughness)
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(chunk)))
        
        # Delta tracking
        energy_delta = (rms - prev_energy) / (prev_energy + 1e-9) if prev_energy else 0
        brightness_delta = (centroid - prev_centroid) / (prev_centroid + 1e-9) if prev_centroid else 0
        
        # Tension model
        if abs(energy_delta) < 0.05 and energy_relative > 1.0:
            tension_accumulator += 0.1  # sustained high energy = building
        elif energy_delta > 0.15:
            tension_accumulator = max(0, tension_accumulator - 0.5)  # release
        elif energy_delta < -0.2:
            tension_accumulator += 0.3  # sudden drop = dramatic
        
        # Mood inference
        if rms < global_rms * 0.4:
            if centroid < 1500:
                mood = "submerged"
            elif harmonic_ratio > 0.7:
                mood = "ethereal"
            else:
                mood = "breathing"
        elif rms < global_rms * 0.8:
            if centroid < 2000:
                mood = "simmering"
            elif onset_density > 3:
                mood = "restless"
            else:
                mood = "floating"
        elif rms < global_rms * 1.3:
            if percussive_ratio > 0.5:
                mood = "driving"
            elif harmonic_ratio > 0.6:
                mood = "soaring"
            else:
                mood = "locked in"
        else:
            if onset_density > 4:
                mood = "erupting"
            elif centroid > 3000:
                mood = "searing"
            elif percussive_ratio > 0.5:
                mood = "pounding"
            else:
                mood = "full force"
        
        # Detect transitions
        transition = None
        if prev_mood and mood != prev_mood:
            if energy_delta > 0.2:
                transition = "drop hits"
            elif energy_delta < -0.2:
                transition = "pulls back"
            elif abs(brightness_delta) > 0.15:
                transition = "shifts color"
            else:
                transition = "evolves"
        
        moment = {
            "time": round(t_mid, 1),
            "time_fmt": f"{int(t_mid//60)}:{int(t_mid%60):02d}",
            "energy": round(energy_relative, 2),
            "energy_delta": round(energy_delta, 2),
            "brightness": round(centroid, 0),
            "mood": mood,
            "texture": {
                "harmonic": round(harmonic_ratio, 2),
                "percussive": round(percussive_ratio, 2),
                "roughness": round(zcr, 4),
                "onset_density": round(onset_density, 1)
            },
            "tension": round(tension_accumulator, 2)
        }
        if transition:
            moment["transition"] = transition
        
        timeline.append(moment)
        prev_energy = rms
        prev_centroid = centroid
        prev_mood = mood
        position += hop_samples
    
    # Build narrative arc
    arc = build_narrative(timeline, duration, global_tempo)
    
    return {
        "track": path.split("/")[-1],
        "duration": round(duration, 1),
        "duration_fmt": f"{int(duration//60)}:{int(duration%60):02d}",
        "tempo": round(float(global_tempo), 1),
        "window_sec": window_sec,
        "hop_sec": hop_sec,
        "moments": len(timeline),
        "timeline": timeline,
        "narrative": arc
    }


def build_narrative(timeline, duration, tempo):
    """Build a human-readable narrative of the track's emotional journey."""
    
    if not timeline:
        return {"arc": "empty", "story": "No data."}
    
    # Find key moments
    peak_moment = max(timeline, key=lambda m: m["energy"])
    quietest = min(timeline, key=lambda m: m["energy"])
    transitions = [m for m in timeline if "transition" in m]
    
    # Divide into thirds
    third = len(timeline) // 3
    opening = timeline[:third] if third > 0 else timeline[:1]
    middle = timeline[third:2*third] if third > 0 else timeline[:1]
    closing = timeline[2*third:] if third > 0 else timeline[:1]
    
    avg_energy = lambda ms: sum(m["energy"] for m in ms) / len(ms)
    common_mood = lambda ms: max(set(m["mood"] for m in ms), key=lambda mood: sum(1 for m in ms if m["mood"] == mood))
    
    # Arc shape
    e_open = avg_energy(opening)
    e_mid = avg_energy(middle)
    e_close = avg_energy(closing)
    
    if e_mid > e_open and e_mid > e_close:
        arc_shape = "mountain"
    elif e_close > e_open:
        arc_shape = "ascending"
    elif e_open > e_close:
        arc_shape = "descending"
    elif max(e_open, e_mid, e_close) - min(e_open, e_mid, e_close) < 0.15:
        arc_shape = "plateau"
    else:
        arc_shape = "wave"
    
    story = {
        "arc_shape": arc_shape,
        "opening": {
            "mood": common_mood(opening),
            "energy": round(e_open, 2)
        },
        "middle": {
            "mood": common_mood(middle),
            "energy": round(e_mid, 2)
        },
        "closing": {
            "mood": common_mood(closing),
            "energy": round(e_close, 2)
        },
        "peak": {
            "time": peak_moment["time_fmt"],
            "mood": peak_moment["mood"],
            "energy": round(peak_moment["energy"], 2)
        },
        "quietest": {
            "time": quietest["time_fmt"],
            "mood": quietest["mood"],
            "energy": round(quietest["energy"], 2)
        },
        "transitions": len(transitions),
        "mood_journey": " → ".join(dict.fromkeys(m["mood"] for m in timeline))
    }
    
    return story


def print_listening_experience(result):
    """Print a human-readable listening experience."""
    
    n = result["narrative"]
    tl = result["timeline"]
    
    print(f"\n🎧 TEMPORAL LISTEN: {result['track']}")
    print(f"   {result['duration_fmt']} | ~{result['tempo']} BPM | {result['moments']} moments captured")
    print(f"\n📐 Arc shape: {n['arc_shape']}")
    print(f"   Opening → {n['opening']['mood']} (energy {n['opening']['energy']})")
    print(f"   Middle  → {n['middle']['mood']} (energy {n['middle']['energy']})")
    print(f"   Closing → {n['closing']['mood']} (energy {n['closing']['energy']})")
    print(f"\n🔥 Peak moment: {n['peak']['time']} — {n['peak']['mood']} (energy {n['peak']['energy']})")
    print(f"🌊 Quietest:    {n['quietest']['time']} — {n['quietest']['mood']} (energy {n['quietest']['energy']})")
    print(f"\n🎭 Mood journey: {n['mood_journey']}")
    print(f"   {n['transitions']} transitions detected")
    
    # Print timeline highlights (transitions + peaks)
    print(f"\n⏱️  TIMELINE (highlights):")
    for m in tl:
        marker = ""
        if "transition" in m:
            marker = f" ⚡ {m['transition']}"
        if m["energy"] >= n["peak"]["energy"] * 0.95:
            marker += " 🔥"
        if m["energy"] <= n["quietest"]["energy"] * 1.05:
            marker += " 🌊"
        
        if marker or "transition" in m:
            bar_len = int(m["energy"] * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"   {m['time_fmt']} [{bar}] {m['mood']}{marker}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: temporal_listen.py <audio_file> [--json]")
        sys.exit(1)
    
    path = sys.argv[1]
    use_json = "--json" in sys.argv
    
    result = analyze_temporal(path)
    
    if use_json:
        # Convert numpy types to native Python for JSON serialization
        def to_native(obj):
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, dict):
                return {k: to_native(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [to_native(i) for i in obj]
            return obj
        print(json.dumps(to_native(result), indent=2))
    else:
        print_listening_experience(result)
