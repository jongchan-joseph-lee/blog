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

Watkins 해양포유류 음향 DB에서 사전학습 오디오 모델의 종 분류 성능을 녹음 출처 분리(source-disjoint) 조건으로 다시 평가한 프로젝트입니다.

## Overview

- **문제**: Watkins DB에서 높은 종 분류 성능을 보고한 선행연구들은 대부분 클립 단위 무작위 분할로 평가했습니다. 이 경우 같은 녹음에서 잘린 클립이 학습과 시험에 함께 들어갑니다.
- **방법**: 5개 표현(AST, VGGish, EfficientNet-B3, MFCC, 물리 특징 51개) + linear probe로 무작위 분할과 녹음 출처 분리 분할을 비교하고, 오디오 없이 메타데이터(샘플레이트 · 길이)만 쓴 기준선과 대조했습니다.
- **결과**: 녹음 출처를 분리하면 종 분류 균형정확도(BA)가 0.21–0.33으로 낮아져 메타데이터 기준선(0.24)과 비슷해집니다.
- **MVP**: 클립별 물리량 14개로 신호 유형을 먼저 판정하고 분류군 확률을 내는 분류기를 만들었습니다. 녹음 출처 분리 조건에서 분류군 BA 0.75입니다.

![Data selection, feature extractors and evaluation](./pam_fig1_study_design.png)

<details>
<summary>특징 추출기별 처리 예시</summary>

![One right whale clip passed through each feature extractor](./pam_extractor_example.png "북대서양긴수염고래 moan 클립 1개의 입력, 처리 구조, 출력 벡터")

</details>

## Results

| Balanced accuracy | 무작위 분할 | 녹음 출처 분리 |
|---|---|---|
| 종 (10) | 0.64–0.76 | 0.21–0.33 (기준선 0.24) |
| 콜 타입 (7) | 0.55–0.74 | 0.29–0.48 |
| 분류군 (3) | 0.82–0.93 | 0.63–0.80 |

![Balanced accuracy under random and source-disjoint splits](./pam_fig3_balanced_accuracy.png)

<details>
<summary>임베딩 분포 (UMAP · t-SNE)</summary>

![UMAP of VGGish vectors](./pam_fig4_umap.png "VGGish 표현 UMAP (3,539 클립)")

![t-SNE of VGGish vectors](./pam_fig4b_tsne.png "VGGish 표현 t-SNE — 종별 색, 분류군별 색")

</details>

- 녹음 출처가 달라져도 신호 유형(tonal · impulsive · pulsed)과 주파수 대역 기준의 구분은 유지되었습니다 (탐색적 분석).

<details>
<summary>신호 유형 · 물리량 · 주파수 대역</summary>

![Balanced accuracy for three signal types](./pam_fig5_signal_type.png "신호 유형 3분류 균형정확도 (탐색적)")

![Distributions of single physical descriptors](./pam_fig6_physical_quantities.png "단일 물리량 분포 (탐색적)")

![Taxon composition by signal type and frequency band](./pam_fig7_taxon_by_band.png "신호 유형 × 주파수 대역별 분류군 구성 (탐색적)")

</details>

- AST 부분 미세조정: 전체 BA 0.784 → 0.752. 수염고래 · 이빨고래 재현율은 오르고 기각류는 내려갔습니다 ([결과](https://github.com/jongchan-joseph-lee/marine-mammal-classifier-benchmark/blob/main/results/ast_finetune_results.json)).

## MVP: Signal-type-first classifier

신호 유형(tonal · impulsive · pulsed)을 먼저 판정하고, 그 확률과 주파수 대역으로 분류군(수염고래 · 이빨고래 · 기각류) 확률을 내는 분류기입니다. 입력은 클립별 물리량 14개이고, 신뢰도가 낮은 클립은 검토 대상으로 넘깁니다.

| 분류군 BA, 녹음 출처 분리 | 전체 (3,539 클립) | fs ≥ 40 kHz, 이빨고래 vs 기각류 |
|---|---|---|
| 샘플레이트만 | 0.66 | 0.50 |
| 주파수 대역만 | 0.71 | 0.49 |
| 신호 유형 + 대역 | 0.72 | 0.51 |
| 신호 유형 + 대역 + 모양 물리량 | 0.75 | 0.71 |
| 물리량 전체, 단일 단계 | 0.76 | 0.73 |

출처 7-fold를 20회 다른 분할로 반복한 평균입니다. 참고로 같은 과제에서 AST는 0.75–0.80, 물리 특징 51개는 0.74였습니다(분할 방식은 같고 fold 배정은 다름).

![Taxon accuracy by model, sampling-rate control and abstention](./pam_fig8_mvp.png)

- 샘플레이트를 40 kHz 이상으로 맞추면 주파수 대역은 구분력이 없고, 모양 물리량(임펄스 비율, 반복 간격, 조화성 등)이 구분을 유지했습니다.
- 샘플레이트 기준선 대비 개선폭은 +0.07이지만, 출처 단위 부트스트랩 95% 구간(−0.04–0.18)이 0을 포함합니다.
- 신호 유형 단계를 거친 모델은 단일 단계 모델과 비슷했습니다. 신호 유형을 중간 결과로 함께 내므로 주석(annotation) 도구의 첫 단계로 쓸 수 있습니다.
- 신뢰도 하위 30%를 검토로 넘기면 나머지 70%의 BA는 0.80입니다.

## Dataset

- [Watkins Marine Mammal Sound Database](https://whoicf2.whoi.edu/science/B/whalesounds/index.cfm) (WHOI), Earth Species Project 공개본 v0.1.0
- 10,694 클립 (36종, 녹음 출처 49개) → 평가 표본 3,539 클립
- 원음은 저장소에 포함하지 않습니다.

<details>
<summary>자료 구조</summary>

![Species by number of recording sources and sampling-rate family by taxon](./pam_fig2_data_structure.png "종별 녹음 출처 수, 분류군별 샘플레이트 구성")

</details>

## Limitations

- Watkins DB 내부 평가입니다. 외부 자료, 연속 녹음, 실해역 운용은 다루지 않았습니다.
- 녹음 출처는 메타데이터(지역 + 연도)로 정한 근사 단위입니다.
- 신호 유형 분석은 첫 결과 이후 정의한 탐색적 분석입니다.
- MVP는 클립 단위 물리량을 씁니다. 연속 녹음에서의 신호 구간 검출은 아직 포함하지 않았습니다.
