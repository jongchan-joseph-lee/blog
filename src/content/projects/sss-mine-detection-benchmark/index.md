---
# 프로젝트 글입니다. 본문은 일반 Markdown입니다.
# 그림: 같은 폴더에 이미지를 넣고 ![대체 텍스트](./파일.png "캡션") 형식으로 씁니다.
title: "측면주사 소나 기뢰유사물체 탐지 · 분류 평가"
subtitle: "Side-Scan Sonar 공개 영상에서 중복 장면과 촬영 연도 변화가 평가에 미치는 영향"
kind: "능동 소나 · 영상"
order: 2
summary: "공개 측면주사 소나 영상에서 탐지기와 패치 분류기를 따로 평가하고, 물리 특징과 AI 특징을 같은 분할 규약에서 비교했습니다."
result: "처음 보는 연도에서 YOLOv8n 객체 재현율 78.1%(화면당 오경보 4건), 정합필터 기준선은 4.3%(오경보 1건)였습니다."
repo: "https://github.com/jongchan-joseph-lee/sss-mine-detection-benchmark"
cover: "./sss_detection_froc.png"
coverAlt: "시험 연도 FROC 곡선과 탐지 예시"
updated: 2026-11-08
---

공개 측면주사 소나(Side-Scan Sonar, SSS) 영상에서 기뢰유사물체(mine-like object) 탐지기와 패치 분류기를 촬영 연도 분할 조건으로 평가한 프로젝트입니다.

## Overview

- **문제**: 공개 AUV 측면주사 영상 자료에는 같은 장면의 축소 복사본이 많고(1,170장 중 417쌍), 연도별 물체 구성이 크게 달라 이미지 단위 무작위 분할에서는 성능이 과대평가될 수 있습니다.
- **방법**: 중복 장면을 점검한 뒤 공식 연도 분할(학습 2015 · 2017 · 2021 → 시험 2010 · 2018)로 평가했습니다. 탐지는 고전 정합필터와 YOLOv8n, 분류는 하이라이트–그림자 물리 특징과 DINOv2를 비교했습니다.
- **결과**: 처음 보는 연도에서 YOLOv8n의 객체 재현율은 78.1%(화면당 오경보 4건), 정합필터는 4.3%(1건)였습니다. 연도가 바뀔 때 분류 성능 하락은 물리 특징(0.04)이 DINOv2(0.15)보다 작았습니다.

![Side-scan frame, across-track highlight-shadow profiles and oriented patches](./sss_highlight_shadow.png)

## Results

| 탐지 (시험 연도 2010 · 2018) | 재현율 @ 화면당 오경보 1건 | 재현율 @ 4건 |
|---|---|---|
| YOLOv8n | 59.6% | 78.1% |
| 고전 정합필터 | 4.3% | — |

![FROC curves for YOLOv8n and the classical matched filter on test years](./sss_detection_froc.png)

| 패치 3분류 macro F1 | 이미지 분할 | 장면 분할 | 연도 분할 |
|---|---|---|---|
| 물리 특징 + 로지스틱 회귀 | 0.734 | 0.719 | 0.679 |
| DINOv2 고정 특징 + 선형 분류기 | 0.814 | 0.751 | 0.606 |
| DINOv2 미세조정 | — | — | 0.645 |

<details>
<summary>분할별 분류 결과 · 혼동 행렬</summary>

![Three-class macro F1 by evaluation split and year-split confusion matrices](./sss_classification_splits.png "분할별 3분류 macro F1과 연도 분할 혼동 행렬 (정답 위치 패치 조건)")

</details>

- 하이라이트–그림자 대비는 물체와 해저 배경을 구분했지만(AUROC 0.830), 물체 종류(MILCO vs NOMBO) 구분력은 낮았습니다(0.513).
- 결과 수치: [`src/b3_yolo.json`](https://github.com/jongchan-joseph-lee/sss-mine-detection-benchmark/blob/main/src/b3_yolo.json), [`src/b2_results.json`](https://github.com/jongchan-joseph-lee/sss-mine-detection-benchmark/blob/main/src/b2_results.json), [`src/b3_patch.json`](https://github.com/jongchan-joseph-lee/sss-mine-detection-benchmark/blob/main/src/b3_patch.json) · 결과 리포트: [`docs/milco-report.html`](https://github.com/jongchan-joseph-lee/sss-mine-detection-benchmark/blob/main/docs/milco-report.html)

## Dataset

- Santos et al. 2024, *Data in Brief* (CC BY 4.0) — Gavia AUV · Marine Sonic 900/1800 kHz, JPEG 1,170장(고유 장면 753개), MILCO · NOMBO 라벨
- 원자료는 저장소에 포함하지 않으며 `src/download_data.sh`로 받습니다.

<details>
<summary>자료 점검 (중복 장면 · 연도별 구성)</summary>

![Objects per year, duplicated scene exports and box sizes](./sss_data_diagnosis.png "연도별 고유 물체 수, 축소 복사본 예시, 표적 크기")

</details>

## Limitations

- CPU로 학습한 소형 모델(YOLOv8n, 25 epoch)이며, 입력은 원시 신호가 아닌 JPEG 영상입니다.
- 분류는 정답 위치 패치 조건의 결과입니다. 탐지 → 분류 연계 성능은 측정하지 않았습니다.
- 한 자료(한 장비 · 해역 계열)의 결과입니다.
