---
# 프로젝트 글입니다. 본문은 일반 Markdown입니다.
# 그림: 같은 폴더에 이미지를 넣고 ![대체 텍스트](./파일.png "캡션") 형식으로 씁니다.
title: "측면주사 소나 기뢰유사물체 탐지 · 분류 평가"
subtitle: "Side-Scan Sonar 공개 영상에서 중복 장면과 촬영 연도 변화가 평가에 미치는 영향"
kind: "능동 소나 · 영상"
order: 2
summary: "공개 측면주사 소나 영상에서 탐지기와 패치 분류기를 따로 평가하고, 물리 특징과 AI 특징을 같은 분할 규약에서 비교했습니다."
result: "미학습 연도 탐지 성능을 좌우한 것은 모델 규모가 아니라 학습 자료의 표적 크기 분포였음. 크기 맞춤 증강으로 탐지율 +13%p, 경량 모델(3.1 M)로 CPU 추론 14배 단축."
repo: "https://github.com/jongchan-joseph-lee/sss-mine-detection-benchmark"
cover: "./sss_augmentation_froc.png"
coverAlt: "원본 · 증강 학습의 시험 연도 FROC와 물체 크기별 Pd"
updated: 2026-11-10
---

공개 AUV 측면주사 소나(SSS) 영상으로 기뢰유사물체 탐지기를 구축하고, 학습에 쓰지 않은 촬영 연도에서 성능을 검증한 프로젝트

## 1. 연구 배경

![Research background timeline](./sss_research_background.png "물리 모델 기반 ATR → 소나 딥러닝 → 현재 과제, 그리고 이 프로젝트에서 쓴 방법")

| 구분 | 이 프로젝트 | 근거 |
|---|---|---|
| 고전 기준선 | 정합필터 · 하이라이트–그림자 특징 | Turin (1960) · Reed 등 (2003) |
| 1단계 탐지기 (CNN) | YOLOv8n · YOLOv8s | Redmon 등 (2016) · Ultralytics (2023) |
| Transformer 탐지기 | RT-DETR-l | Zhao 등 (2024) |
| 사전학습 특징 | DINOv2 | McKay 등 (2017) · Oquab 등 (2024) |
| 소형 표적 보강 | 그림자 보존 붙여넣기 증강 | Kisantal 등 (2019) |
| 남은 과제 | 자료 부족 · 소형 표적 오경보 · 조사 조건 변화 | Santos 등 (2024) · Cui 등 (2025) · de Bodinat 등 (2020) |

## 2. 연구 목적

![Pipeline](./sss_pipeline.png "연도 분할 → 학습(크기 맞춤 증강) · 시험(분할 추론) → 평가")

| 검토 사항 | 실험 | 지표 |
|---|---|---|
| 미학습 연도 탐지 성능 | 학습 2015 · 2017 · 2021 → 시험 2010 · 2018 (영상 578장, 물체 114개) | 영상당 평균 오경보 수(FA/image)별 탐지율 Pd |
| 성능 저하 요인 | 미탐지 표적의 크기 · 연도 분석 | 크기 구간별 Pd |
| 자료 보강 vs 모델 규모 | 크기 맞춤 증강 유무 × YOLOv8n · YOLOv8s · RT-DETR-l | Pd · 추론 시간 (CPU · GPU) |
| 물리 특징의 기여 | 하이라이트–그림자 재판정 · 패치 분류 | Pd · macro F1 |

## 3. 결과

| 검토 사항 | 결과 |
|---|---|
| 미학습 연도 탐지 성능 | YOLOv8n Pd 59.6% (FA/image 1) · 78.1% (4). 정합필터 4.3% (1) |
| 성능 저하 요인 | 미탐지가 30–50 px 표적에 집중 (Pd 59%). 학습 표적 중앙값 55 px > 시험 39 px |
| 자료 보강 vs 모델 규모 | 크기 맞춤 증강 Pd +13%p (8). 모델 3.1 → 32.8 M: Pd 변화 없음, CPU 추론 2.5–14배 |
| 물리 특징의 기여 | 재판정 Pd 59.6 → 70.2% (1). 연도 변화 시 분류 저하폭 물리 0.04 < DINOv2 0.15 |

### 크기 맞춤 증강

![Augmentation examples](./sss_augmentation_examples.png "(a) 원본 · (b) 축소 · (c) 다른 연도 해저면에 그림자째 합성 · (d) 광도 증강")

| Pd (YOLOv8n) | FA/image 4 | 8 | 30–50 px |
|---|---|---|---|
| 기본 증강만 | 71.9% | 71.9% | 58.8% |
| + 크기 맞춤 증강 | 84.2% | 91.2% | 79.4% |

<details>
<summary>시험 연도 FROC · 크기별 Pd</summary>

![Test-year FROC and recall by object size](./sss_augmentation_froc.png "기본 증강만 · 크기 맞춤 증강의 FROC와 크기별 Pd")

</details>

### 모델 규모와 추론 시간

![Recall versus latency](./sss_detector_tradeoff.png "탐지율(FA/image 8) vs 영상 1장당 추론 시간 (분할 추론, RTX 3070 Ti PC)")

| + 크기 맞춤 증강 | 파라미터 | Pd @ 8 | CPU | GPU |
|---|---|---|---|---|
| YOLOv8n | 3.1 M | 86.8% | 132 ms | 20 ms |
| YOLOv8s | 11.1 M | 85.1% | 325 ms | 29 ms |
| RT-DETR-l | 32.8 M | 78.9% | 1,816 ms | 97 ms |

<details>
<summary>모델 구조</summary>

![Model architecture](./sss_architecture.png "(a) YOLOv8n 탐지기 · (b) 하이라이트–그림자 재판정 분류기")

</details>

### 하이라이트–그림자 물리 특징

![Highlight-shadow profiles](./sss_highlight_shadow.png "횡방향 하이라이트–그림자 프로파일과 nadir 기준 정렬 패치")

| 재판정 | FA/image 0.5 | 1 |
|---|---|---|
| YOLOv8n 단독 | 48.2% | 59.6% |
| + 물리 특징 재판정 | 53.5% | 70.2% |

| 패치 분류 macro F1 | 장면 분할 | 연도 분할 | 하락폭 |
|---|---|---|---|
| 물리 특징 | 0.719 | 0.679 | 0.04 |
| DINOv2 | 0.751 | 0.606 | 0.15 |

<details>
<summary>탐지 기준선 · 자료 점검</summary>

![Detection FROC](./sss_detection_froc.png "YOLOv8n과 정합필터 FROC, 시험 연도 탐지 예시")

![Data diagnosis](./sss_data_diagnosis.png "연도별 물체 수, 축소 복사본 예시, 표적 크기")

</details>

## 4. 고찰

| 결과 | 문헌 근거 | 해석 |
|---|---|---|
| 미탐지가 소형 표적에 집중, 크기 맞춤 증강으로 향상 | 소형 객체는 학습 표본 · 앵커 정합이 부족하고, 복제 · 붙여넣기로 7.1% 향상 (Kisantal 등, 2019) | 일반 영상의 소형 객체 문제와 같은 양상. 그림자 방향을 보존하도록 소나에 맞게 변형 |
| 모델을 키워도 Pd 변화 없음 | 해저 질감 변화가 ATR 성능을 좌우 (de Bodinat 등, 2020). DETR 계열은 소형 객체에 약함 (Zhu 등, 2021) | 병목은 모델 표현력이 아니라 자료 분포 차이 |
| 물리 특징이 연도 변화에 강하고 오경보를 줄임 | 그림자는 기뢰유사물체 판별의 핵심 단서 (Reed 등, 2003; Mukherjee 등, 2011) | 학습 기반 탐지기의 조사 조건 의존성을 보완 |
| 경량 모델이 대등한 Pd, CPU 14배 빠름 | AUV 탑재 시 모델 크기가 실질 제약 (Aubard 등, 2024) | 탑재용 경량 모델의 실용성 확인 |
| 영상당 오경보로 보고 | 운용 평가는 면적당 오경보 밀도 사용 (arXiv:2404.18663) | 다음 단계: 메타데이터 확보 · 새 해역 소량 라벨로 임계값 재보정 |

## 한계

- JPEG 영상 · 단일 자료 · 검증 장면 26장
- 증강 방향은 시험 연도 진단을 보고 설정
- 실행 간 차이 약 9%p (같은 설정 재학습 기준)

[저장소 · 참고문헌](https://github.com/jongchan-joseph-lee/sss-mine-detection-benchmark) · [실행 기록](https://github.com/jongchan-joseph-lee/sss-mine-detection-benchmark/tree/main/src/gpu_runs)
