"""
Build the home-page spectrogram strip from real Watkins recordings.
홈 첫 화면 스펙트로그램(실제 Watkins 녹음)과 신호 측정값을 만드는 스크립트입니다.

    python scripts/hero/build_hero.py --wav-dir <WAV 폴더>

Outputs (출력)
    public/hero/strip.webp   log-frequency spectrogram strip (로그 주파수 스펙트로그램 띠)
    src/data/hero.json       per-clip metadata and measurements (클립 정보 · 측정값)

Measurements (측정 방법) — computed inside each clip's selection box
    noise N(f)   : 20th percentile of power per frequency bin over the whole clip
                   (주파수 bin별 전체 클립 파워의 20번째 백분위수 = 배경 잡음)
    signal S     : max(P - N, 0) inside the selection box (잡음 차감 파워)
    duration 90% : t95 - t5 of cumulative energy over time (시간 누적 에너지 5–95%)
    f_peak       : frequency of the maximum of the summed spectrum (합산 스펙트럼 최대 주파수)
    f50          : frequency at 50 % cumulative spectral energy (중앙 주파수)
    BW -3 dB     : contiguous width around f_peak where the spectrum is within 3 dB of the peak
    box          : t5–t95 and f5–f95 (에너지 90% 구간)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import soundfile as sf
import yaml
from PIL import Image
from scipy.signal import ShortTimeFFT
from scipy.signal.windows import hann

ROOT = Path(__file__).resolve().parents[2]

F0, F1 = 20.0, 24000.0          # display range (화면 주파수 범위)
ROWS = 360                       # strip height in px (띠 높이)
COLS_PER_SEC = 240               # strip columns per second (초당 열 수, 화면 120 px/s의 2배)
GAP_SEC = 0.45                   # gap between clips (클립 사이 간격)
DB_RANGE = (2.0, 30.0)           # display: dB above median noise → dark..white
NYQ_VALUE = 10                   # pixel value above Nyquist (나이퀴스트 위 영역)
GAP_VALUE = 16


def stft_power(x: np.ndarray, sr: int, win_s: float):
    n = int(2 ** np.round(np.log2(max(32, sr * win_s))))
    hop = max(1, int(round(sr / COLS_PER_SEC)))
    sft = ShortTimeFFT(hann(n, sym=False), hop=hop, fs=sr, scale_to="psd")
    P = sft.spectrogram(x)                       # (freq, time)
    f = sft.f
    t = sft.t(len(x))
    keep = (t >= 0) & (t <= len(x) / sr)
    return f, t[keep], P[:, keep], n


def measure(f, t, P, noise, sel):
    t0, t1, fl, fh = sel
    fi = (f >= fl) & (f <= fh)
    ti = (t >= t0) & (t <= t1)
    S = np.maximum(P[np.ix_(fi, ti)] - noise[fi, None], 0.0)
    ff, tt = f[fi], t[ti]
    E = S.sum(axis=0)
    c = np.cumsum(E) / E.sum()
    i5, i95 = np.searchsorted(c, 0.05), np.searchsorted(c, 0.95)
    ts, te = tt[i5], tt[min(i95, len(tt) - 1)]
    A = S[:, i5:i95 + 1].sum(axis=1)
    ca = np.cumsum(A) / A.sum()
    f5, f50, f95 = (ff[np.searchsorted(ca, q)] for q in (0.05, 0.5, 0.95))
    k = int(np.argmax(A))
    half = A[k] / 2.0                                   # -3 dB in power
    lo = k
    while lo > 0 and A[lo - 1] >= half:
        lo -= 1
    hi = k
    while hi < len(A) - 1 and A[hi + 1] >= half:
        hi += 1
    df = ff[1] - ff[0]
    bw = (ff[hi] - ff[lo]) + df
    return {
        "t5": float(ts), "t95": float(te), "duration": float(te - ts),
        "f5": float(f5), "f95": float(f95), "f50": float(f50),
        "fpeak": float(ff[k]), "bw3": float(bw), "df": float(df),
    }


def to_log_rows(f, P, sr):
    edges = np.exp(np.linspace(np.log(F1), np.log(F0), ROWS + 1))  # top → bottom
    out = np.full((ROWS, P.shape[1]), np.nan)
    for r in range(ROWS):
        hi, lo = edges[r], edges[r + 1]
        if lo >= sr / 2:
            continue
        m = (f >= lo) & (f < hi)
        if m.any():
            out[r] = P[m].max(axis=0)
        else:
            fc = np.sqrt(lo * hi)
            j = np.searchsorted(f, fc)
            j = np.clip(j, 1, len(f) - 1)
            w = (fc - f[j - 1]) / (f[j] - f[j - 1])
            out[r] = (1 - w) * P[j - 1] + w * P[j]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wav-dir", required=True)
    ap.add_argument("--clips", default=str(ROOT / "scripts/hero/clips.yaml"))
    args = ap.parse_args()

    clips = yaml.safe_load(open(args.clips, encoding="utf-8"))
    columns, meta = [], []
    cursor = 0.0
    gap_cols = int(round(GAP_SEC * COLS_PER_SEC))

    for c in clips:
        x, sr = sf.read(Path(args.wav_dir) / c["file"], always_2d=True)
        x = x[:, 0].astype(np.float64)
        f, t, P, n = stft_power(x, sr, c["window"])
        noise = np.percentile(P, 20, axis=1)
        m = measure(f, t, P, noise, c["select"])

        a, b = c["crop"]
        ti = (t >= a) & (t < b)
        # display normalisation: dB above the per-bin median (표시용: bin별 중앙값 대비 dB)
        med = np.median(P, axis=1)
        D = 10 * np.log10(P[:, ti] + 1e-30) - 10 * np.log10(med[:, None] + 1e-30)
        L = to_log_rows(f, D, sr)
        v = np.clip((L - DB_RANGE[0]) / (DB_RANGE[1] - DB_RANGE[0]), 0, 1) ** 1.1
        img = (24 + v * (238 - 24))
        img[np.isnan(L)] = NYQ_VALUE
        columns.append(img.astype(np.uint8))
        seg_cols = img.shape[1]

        start = cursor
        meta.append({
            "record": str(c["record"]),
            "name_ko": c["name_ko"], "name_en": c["name_en"], "scientific": c["scientific"],
            "signal": c["signal"], "signal_type": c["signal_type"],
            "year": c["year"], "place": c["place"],
            "fs": int(sr), "nfft": int(n),
            "seg_start": start, "seg_end": start + seg_cols / COLS_PER_SEC,
            "t0": start + (m["t5"] - a), "t1": start + (m["t95"] - a),
            "fmin": m["f5"], "fmax": m["f95"],
            "duration": round(m["duration"], 3), "f50": round(m["f50"], 1),
            "fpeak": round(m["fpeak"], 1), "bw3": round(m["bw3"], 1), "df": round(m["df"], 2),
        })
        cursor += seg_cols / COLS_PER_SEC
        columns.append(np.full((ROWS, gap_cols), GAP_VALUE, np.uint8))
        cursor += gap_cols / COLS_PER_SEC
        print(f"{c['record']:>9} {c['name_en']:<28} fs={sr:>6}  dur={m['duration']:.3f}s  "
              f"f50={m['f50']:.0f}  fpeak={m['fpeak']:.0f}  bw3={m['bw3']:.0f}  (df={m['df']:.1f})")

    strip = np.concatenate(columns, axis=1)
    out_img = ROOT / "public/hero/strip.webp"
    out_img.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(strip, "L").convert("RGB").save(out_img, quality=80, method=6)

    data = {
        "source": "Watkins Marine Mammal Sound Database (WHOI)",
        "f_min": F0, "f_max": F1, "rows": ROWS,
        "cols_per_sec": COLS_PER_SEC, "loop_sec": strip.shape[1] / COLS_PER_SEC,
        "clips": meta,
    }
    (ROOT / "src/data/hero.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("strip", strip.shape, f"{out_img.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
