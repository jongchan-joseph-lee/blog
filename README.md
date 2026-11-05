# jlee_blog

이종찬(Jongchan Lee)의 개인 연구 블로그 · 포트폴리오입니다.
주소: https://jongchan-joseph-lee.github.io/jlee_blog/

[Astro](https://astro.build)로 만든 정적 사이트이며, `main` 브랜치에 push하면 GitHub Actions가 자동으로 빌드해 GitHub Pages에 배포합니다.

## 내용 고치는 법

코드를 몰라도 아래 파일만 고치면 됩니다. GitHub 웹에서 파일을 열고 연필 아이콘(Edit)으로 고친 뒤 **Commit changes**를 누르면 1–2분 뒤 사이트에 반영됩니다.
사이트 각 페이지 맨 아래의 **"GitHub에서 이 페이지 수정"** 링크를 누르면 해당 파일 편집 화면으로 바로 갑니다.

| 바꾸고 싶은 것 | 고칠 파일 | 형식 |
|---|---|---|
| 이름 · 소속 · 소개 문단 · 링크 · 이메일 · "지금 하고 있는 일" | `src/data/site.yaml` | YAML |
| 연구 · 산업 과제 목록 | `src/data/work.yaml` | YAML |
| 첫 화면(프로필) 본문: 학력 · 경력 · 논문 · 발표 · 기술 | `src/content/pages/profile.md` | Markdown |
| 공개 연구 프로젝트 글 | `src/content/projects/<폴더>/index.md` | Markdown |
| 블로그 글 | `src/content/posts/` | Markdown |
| 프로필 사진 | `public/images/profile.jpg` | 같은 이름으로 교체 |
| 색 · 글꼴 | `src/styles/global.css` 맨 위 `:root` 블록 | CSS |

### 과제 하나 추가하기 (`src/data/work.yaml`)

맨 위에 아래 블록을 복사해 붙이고 내용을 바꿉니다. 들여쓰기(띄어쓰기 2칸)를 맞춰 주세요.

```yaml
- start: 2026
  end: 2027            # 진행 중이면 비워 두기
  title: Project title in English
  funder: 발주 기관
  group: pam           # pam | realtime | array | modeling | education
  role: 맡은 역할 한두 문장
```

### 새 글 쓰기 (`src/content/posts/`)

1. `_template.md`를 복사해 `2026-11-10-my-note.md`처럼 이름을 바꿉니다 (밑줄 `_`로 시작하는 파일은 사이트에 나오지 않습니다).
2. 맨 위 `title`, `date`, `summary`를 고치고 아래에 본문을 씁니다.
3. 글이 하나라도 생기면 상단 메뉴에 **글**이 자동으로 나타납니다.
4. 아직 공개하지 않을 글은 `draft: true`로 둡니다.

그림이 있는 글은 폴더로 만들면 편합니다: `src/content/posts/my-note/index.md` 옆에 그림을 두고 `![설명](./그림.png "캡션")`.

### 새 프로젝트 추가하기 (`src/content/projects/`)

기존 폴더 하나를 통째로 복사해 이름을 바꾸고, `index.md` 맨 위 항목(`title`, `summary`, `result`, `repo`, `cover` 등)과 본문을 고칩니다. `order` 숫자가 작을수록 앞에 나옵니다.

### Markdown 그림 + 캡션

```markdown
![대체 텍스트(그림 설명)](./figure.png "그림 아래에 보일 캡션")
```

따옴표 안의 캡션이 있으면 자동으로 그림 아래 캡션으로 표시됩니다.

## 내 컴퓨터에서 미리 보기 (선택)

Node.js 22 이상이 필요합니다.

```bash
npm install
npm run dev      # http://localhost:4321/jlee_blog/
npm run build    # dist/ 에 정적 파일 생성
```

## 구조

```
src/
├── data/            site.yaml, work.yaml        ← 자주 고치는 정보
├── content/
│   ├── pages/       profile.md                  ← 프로필 본문
│   ├── projects/    <폴더>/index.md + 그림      ← 프로젝트 글
│   └── posts/       블로그 글
├── components/      Spectrogram.astro           ← 홈 첫 화면 스펙트로그램
├── layouts/         Base.astro                  ← 머리글 · 바닥글
├── pages/           각 페이지 주소
└── styles/          global.css                  ← 색 · 글꼴 · 레이아웃
```

홈 첫 화면의 스펙트로그램은 실제 녹음이 아닌 합성 그림입니다 (해양포유류 소리 유형과 자동 주석 예시).

## 라이선스

- 사이트 코드: MIT
- 프로젝트 그림은 각 원 저장소와 원자료의 조건을 따릅니다. 측면주사 소나 자료는 Santos et al. 2024 (CC BY 4.0), SAS 자료는 PoSSM (CC BY-NC-SA 3.0 US)입니다.
