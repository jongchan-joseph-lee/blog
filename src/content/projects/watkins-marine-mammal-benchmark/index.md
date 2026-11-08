---
# 프로젝트 글입니다. 본문은 일반 Markdown입니다.
# 그림: 같은 폴더에 이미지를 넣고 ![대체 텍스트](./파일.png "캡션") 형식으로 씁니다.
title: "What generalises across recordings?"
subtitle: "Watkins 해양포유류 음향 DB에서 레퍼런스 표현의 일반화 평가"
kind: "수동음향 (PAM)"
order: 1
summary: "공개 해양포유류 음향 DB에서 보고된 높은 종 분류 성능이 녹음 출처를 분리한 평가에서도 유지되는지 검토했습니다."
result: "녹음 출처를 분리하자 종 균형정확도가 0.64–0.76에서 0.21–0.33으로 내려가 오디오를 읽지 않는 기준선(0.24)과 비슷해졌습니다. 신호 유형 우선 MVP의 분류군 균형정확도는 0.75입니다."
repo: "https://github.com/jongchan-joseph-lee/marine-mammal-classifier-benchmark"
cover: "./pam_fig3_balanced_accuracy.png"
coverAlt: "표현별 균형정확도: 클립 무작위 분할과 녹음 출처 분리 비교"
updated: 2026-11-09
---

Watkins 해양포유류 음향 DB에서 종 분류 성능이 녹음 출처를 분리해도 유지되는지 검토하고, 일반화되는 단서로 분류기를 만든 프로젝트입니다.

![Data selection, feature extractors and evaluation](./pam_fig1_study_design.png "자료 선택 · 특징 추출 · 평가 설계")

| 항목 | 내용 |
|---|---|
| 자료 | Watkins (WHOI) · ESP 공개본 v0.1.0 · 평가 3,539 클립 (녹음 출처 49) |
| 표현 | AST · VGGish · EfficientNet-B3 · MFCC · 물리 특징 51 + linear probe |
| 평가 | 클립 무작위 분할 vs 녹음 출처 분리 |
| 결과 | 종 BA 0.64–0.76 → 0.21–0.33 (메타데이터 기준선 0.24) |

## 무작위 분할 vs 녹음 출처 분리

![Balanced accuracy under random and source-disjoint splits](./pam_fig3_balanced_accuracy.png "표현별 균형정확도(BA)")

| Balanced accuracy | 무작위 분할 | 녹음 출처 분리 |
|---|---|---|
| 종 (10) | 0.64–0.76 | 0.21–0.33 |
| 콜 타입 (7) | 0.55–0.74 | 0.29–0.48 |
| 분류군 (3) | 0.82–0.93 | 0.63–0.80 |

- 출처를 분리하면 종 분류는 샘플레이트 · 길이만 쓴 기준선(0.24) 수준

## 일반화되는 단서: 신호 유형 · 주파수 대역

![Balanced accuracy for three signal types](./pam_fig5_signal_type.png "신호 유형(tonal · impulsive · pulsed) 3분류 BA (탐색적)")

![Taxon composition by signal type and frequency band](./pam_fig7_taxon_by_band.png "신호 유형 × 주파수 대역별 분류군 구성 (탐색적)")

## MVP: 신호 유형 우선 분류기

![Taxon accuracy by model, sampling-rate control and abstention](./pam_fig8_mvp.png "모델별 분류군 BA, 샘플레이트 통제, 검토 위임")

| 분류군 BA (녹음 출처 분리) | 전체 | fs ≥ 40 kHz |
|---|---|---|
| 샘플레이트만 | 0.66 | 0.50 |
| 주파수 대역만 | 0.71 | 0.49 |
| 신호 유형 + 대역 | 0.72 | 0.51 |
| 신호 유형 + 대역 + 모양 물리량 | 0.75 | 0.71 |
| 물리량 전체, 단일 단계 | 0.76 | 0.73 |

- fs ≥ 40 kHz에서는 대역 구분력이 사라지고 모양 물리량(임펄스 비율 · 반복 간격 · 조화성)이 유지
- 신뢰도 하위 30%를 검토로 넘기면 나머지 BA 0.80
- 기준선 대비 +0.07, 95% 구간 −0.04–0.18 (0 포함)

<details>
<summary>임베딩 분포 · 특징 추출 예시 · 자료 구조</summary>

![UMAP of VGGish vectors](./pam_fig4_umap.png "VGGish 표현 UMAP (3,539 클립)")

![t-SNE of VGGish vectors](./pam_fig4b_tsne.png "VGGish 표현 t-SNE")

![One right whale clip passed through each feature extractor](./pam_extractor_example.png "클립 1개의 특징 추출기별 입력 · 출력")

![Distributions of single physical descriptors](./pam_fig6_physical_quantities.png "단일 물리량 분포 (탐색적)")

![Species by number of recording sources and sampling-rate family by taxon](./pam_fig2_data_structure.png "종별 녹음 출처 수, 분류군별 샘플레이트 구성")

</details>

## 한계

- Watkins 내부 평가 (외부 자료 · 연속 녹음 미포함)
- 녹음 출처는 메타데이터(지역 + 연도) 기반 근사
- 신호 유형 분석은 첫 결과 이후 정의한 탐색적 분석

[결과 수치](https://github.com/jongchan-joseph-lee/marine-mammal-classifier-benchmark/tree/main/results)
