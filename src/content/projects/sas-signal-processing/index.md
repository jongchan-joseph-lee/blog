---
# 프로젝트 글입니다. 본문은 일반 Markdown입니다.
# 그림: 같은 폴더에 이미지를 넣고 ![대체 텍스트](./파일.png "캡션") 형식으로 씁니다.
title: "Synthetic Aperture Sonar Imaging and Navigation-Error Sensitivity"
subtitle: "공개 SAS 시뮬레이션 원시 신호로 영상 형성 · 항법 오차 보정을 구현하고 기준 영상으로 검증한 벤치마크"
kind: "능동 소나 · 원시 신호"
order: 3
summary: "원시 신호부터 역투영 영상까지 직접 구현하고, 항법 오차가 영상에 주는 영향과 지표 기반 보정의 효과를 기준 영상으로 측정했습니다."
result: "수신기 이동 보상으로 위치 오차 15.1 → 1.8 mm. 좌우 2 mm 항법 오차만으로 영상 일치도 0.50, 보정은 근거리 0.98까지 회복하나 거리가 멀수록 감소."
repo: "https://github.com/jongchan-joseph-lee/SAS_signal_processing"
cover: "./sas_scene_comparison.png"
coverAlt: "기준 영상, 직접 만든 역투영 영상, 항법 오차를 넣은 영상 비교"
updated: 2026-11-10
---

공개 합성개구 소나(SAS) 시뮬레이션의 원시 신호로 영상 형성과 항법 오차 보정을 직접 구현하고, 기준 영상과 비교해 항법 오차의 영향을 측정한 벤치마크

![Provided ASASIN SLC, own backprojection, and own backprojection with 2 mm sway error](./sas_scene_comparison.png "기준 영상(ASASIN SLC) · 직접 만든 역투영 영상 · 좌우 2 mm 항법 오차")

## Background

![Background timeline](./sas_research_background.png "영상 형성 → 지표 기반 보정 → 남은 과제, 그리고 이 벤치마크에서 쓴 방법")

| 영상 형성의 전제 | 근거 |
|---|---|
| 정지 가정은 저속 · 짧은 펄스에서만 성립 | Hawkins & Gough (2004) |
| 핑 간 좌우 위치를 수십 μm 수준으로 알아야 함 | Bellettini & Pinto (2002) |
| 위상 오차는 PGA · 엔트로피 최소화로 보정 | Wahl 등 (1994) · Xi, Liu & Ni (1999) |

## Benchmark Setup

| 항목 | 내용 |
|---|---|
| 자료 | PoSSM (MGDS) · 11장면 · 원시 IQ + 기준 영상 · 무잡음 시뮬레이션 |
| 영상 형성 | 정합필터 → 송수신 분리 역투영, 정지 가정 vs 수신기 이동 반영 |
| 항법 오차 | 처리용 항적에 진행 · 좌우 오차와 음속 편향을 넣어 민감도 측정 |
| 보정 | local GPGA · 핑별 엔트로피 최소화 |
| 지표 | 산란체 위치 오차(mm) · 기준 영상과의 복소 상관(NCC) |
| 평가 규칙 | 개발용 자료로 조건 · 기준을 정한 뒤 시험 자료로 1회 평가 |

## Results

| 비교 | 결과 |
|---|---|
| 정지 가정 vs 수신기 이동 반영 | 위치 오차 15.1 → 1.8 mm |
| 항법 오차 민감도 (2 mm RMS) | 좌우 NCC 0.50 · 진행 방향 0.99 |
| 항법 오차 보정 | NCC 0.442 → 0.830 (사전 기준 0.90) |
| 거리별 보정 효과 | NCC 0.977 → 0.726 → 0.594 (15–35 · 35–55 · 55–80 m) |

### 영상 형성

![Position error with stop-and-hop versus receiver-motion model](./sas_motion_compensation.png "정지 가정과 수신기 이동 반영 모델의 위치 오차 (산란체 24개)")

<details>
<summary>처리 설정 (보간 · 창 · PSF)</summary>

![Development-point NCC for interpolation and window settings](./sas_window_ablation_dev.png "개발용 3점 보간 배율 · 창 설정 비교")

![Test-point correlation before and after window settings](./sas_window_test_points.png "시험 24점 복소수 상관 · 진폭 상관")

![Point spread function before and after window settings](./sas_psf_window.png "창 적용 전후 PSF (NCC 0.672 → 0.875는 창 처리 일치의 결과, 주엽은 24.4 → 26.8 mm로 넓어짐)")

</details>

### 항법 오차 민감도

![NCC versus navigation error and sound speed bias](./sas_navigation_sensitivity.png "항적 오차(진행 · 좌우 · 동시)와 음속 편향에 따른 영상 일치도 (24점 × 5경로)")

| 2 mm RMS 오차 | 진행 방향 | 좌우 방향 |
|---|---|---|
| 기준 영상 NCC | 0.99 | 0.50 |

### 항법 오차 보정

![Autofocus NCC by range band](./sas_autofocus_by_range.png "거리 구간별 항법 오차 보정 결과")

| 거리 | 15–35 m | 35–55 m | 55–80 m |
|---|---|---|---|
| 보정 후 NCC | 0.977 | 0.726 | 0.594 |

<details>
<summary>부록: 객체 탐지 시도 (사전 기준 미달)</summary>

| 시험 4장면 · 물체 36개 | 재현율 | 장면당 오경보 |
|---|---|---|
| 후보 생성 + Random Forest | 0.25 (9/36) | 2.75 |

![Point FROC on four test scenes](./sas_detection_froc.png "시험 4장면 점 단위 FROC")

![Candidate detections on a test scene](./sas_detection_map.png "시험 장면 04 탐지 예시와 클래스 결과")

</details>

## Takeaways

- 수신기 이동 반영\
  → 정지 가정 대비 위치 오차 약 1/8 (15.1 → 1.8 mm). mm급 영상 형성의 전제 조건
- 항법 오차의 영향\
  → 좌우 방향 mm 단위 오차가 영상 품질을 좌우함. 미세항법 정확도 요구(Bellettini & Pinto, 2002)를 수치로 확인
- 지표 기반 보정\
  → 근거리에서는 거의 완전 회복(NCC 0.98), 거리가 멀수록 효과 감소

## Limitations → Next Steps

- 먼 거리(35 m 이상)에서 보정 효과 감소\
  → 합성개구 길이 · 신호 대 잡음비 · 공간 가변 오차 요인 분리, 스트립맵 PGA(Callow) 방식 비교
- 지표 기반 보정의 한계 (연산량 · 파라미터 민감도 · 선명도 지표의 국소해)\
  → 딥러닝 기반 보정(Gerg & Monga, 2020; 2021)과 같은 자료에서 비교
- 무잡음 시뮬레이션 한 종류\
  → 잡음을 넣은 시뮬레이션으로 재평가 후 실측 SAS로 확장. 시뮬레이션 자료의 충실도 문제(Blanford & Williams, 2024) 고려
- 항법 오차를 원시 신호가 아닌 처리용 항적에 넣어 생성\
  → 원시 신호 단계에서 항법 오차를 넣은 시뮬레이션으로 검증
- 기준 영상과의 장면 전체 차이 원인 미분리\
  → 거리별 진폭 규약 · 보간 · 창 처리를 단계별로 분리 비교

[저장소 · 참고문헌](https://github.com/jongchan-joseph-lee/SAS_signal_processing) · [보고서](https://github.com/jongchan-joseph-lee/SAS_signal_processing/blob/main/report_v3/report.html)
