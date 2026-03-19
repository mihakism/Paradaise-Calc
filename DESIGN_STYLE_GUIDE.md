# 파라다이스 계산기 — Design Style Guide
> 최종 버전 · 2026.03  
> 실제 구현(index.html) 기준 디자인 시스템

---

## 1. 디자인 원칙

| 원칙 | 설명 |
|------|------|
| **미니멀** | 불필요한 장식 없이 숫자와 그래프가 주인공 |
| **라이트 테마** | 연한 회색 배경에 흰 카드, 높은 명암 대비 |
| **즉각적 반응** | 슬라이더 조작 → 차트·카드 즉시 업데이트 (debounce 300ms) |
| **모바일 퍼스트** | 좌우 패딩, 카드 그리드 모두 반응형 |

---

## 2. 디자인 토큰 (CSS Custom Properties)

```css
:root {
  /* 배경 */
  --bg-base:        #EBEBEB;   /* 페이지 배경 */
  --bg-card:        #FFFFFF;   /* 카드·패널 배경 */
  --bg-card-hover:  #F5F5F5;   /* 카드 호버 상태 */
  --bg-input:       #E0E0E0;   /* 입력 필드·프리셋 배경 */

  /* 보더 */
  --border:         #E0E0E0;
  --border-light:   #E0E0E0;

  /* 브랜드 컬러 */
  --primary:        #111111;   /* 메인 액션·텍스트 */
  --primary-dim:    #333333;   /* 호버 시 어두운 상태 */
  --primary-glow:   rgba(17, 17, 17, 0.08);

  /* 그린 (성공·강조) */
  --gold:           #81CE16;
  --gold-dim:       #A0B800;
  --gold-glow:      rgba(129, 206, 22, 0.12);

  /* 서브 컬러 */
  --violet:         #999999;
  --violet-glow:    rgba(153, 153, 153, 0.08);
  --danger:         #F4907A;
  --success:        #81CE16;
  --warning:        #F97316;

  /* 텍스트 계층 */
  --text-1:         #111111;   /* 주요 텍스트 */
  --text-2:         #666666;   /* 보조 텍스트 */
  --text-3:         #999999;   /* 힌트·단위·레이블 */

  /* 타이포·스페이싱 토큰 */
  --font: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --r-sm:  8px;
  --r-md:  12px;
  --r-lg:  16px;
  --r-xl:  24px;
  --ease:  150ms ease;
}
```

---

## 3. 컬러 팔레트

### 3-1. 시맨틱 컬러

| 역할 | 토큰 | Hex |
|------|------|-----|
| 주요 텍스트·버튼 | `--primary` | `#111111` |
| 성공·그린 강조 | `--gold` / `--success` | `#81CE16` |
| 위험·경고 (낮은 달성률) | `--danger` | `#F4907A` |
| 힌트·비활성 | `--text-3` | `#999999` |
| 페이지 배경 | `--bg-base` | `#EBEBEB` |
| 카드 배경 | `--bg-card` | `#FFFFFF` |

### 3-2. 인원(Person) 컬러 팔레트

차트 라인 및 레전드 도트에 사용. 인원 0번부터 순서대로 배정.

| 인덱스 | 이름 (참고) | Hex | 용도 |
|--------|------------|-----|------|
| 0 | 코코넛 (기본/나) | `#81CE16` | 기본 사용자 라인 |
| 1 | 망고 | `#B8A8E8` | 두 번째 인원 |
| 2 | 파파야 | `#F4907A` | 세 번째 인원 |
| 3 | 선인장 | `#54D4E8` | 네 번째 인원 |
| 4 | 보라 | `#6B3FA0` | 다섯 번째 인원 |

---

## 4. 타이포그래피

### 폰트
- **한글·UI**: Pretendard (Google Fonts)
- **아이콘**: Material Symbols Outlined (weight 300, fill 0)

### 텍스트 스케일

| 역할 | size | weight | color |
|------|------|--------|-------|
| 히어로 타이틀 | 36px | 400 | `--text-1` |
| 결과 카드 숫자 | 30px | 800 | 상황별 강조색 |
| 페이지 타이틀 | 30px | 700 | `--text-1` |
| 카드 소제목 | 40px | 400 | `--text-1` |
| 섹션 헤더 | 14px | 500 | `--text-1` |
| 본문 / 슬라이더 레이블 | 13px | 500 | `--text-1` |
| 슬라이더 값 | 15px | 800 | `--text-1` |
| 카드 레이블 (UPPER) | 11px | 700 | `--text-3` |
| 서브·보조 | 12px | 400 | `--text-3` |
| 섹션 헤더 태그 | 12px | 600 | `--text-3` |

---

## 5. 레이아웃

### 5-1. 전체 구조

```
┌──────────────────────────────────────────────────┐  ← Topbar (height: 56px, fixed)
│  로고  |  히어로 메시지  |  [수정 버튼] [아이콘]   │
├──────────────────────────────────────────────────┤
│                                                  │
│  히어로 섹션 (환영 문구 + 목표 비율)               │  ← .content (padding: 0 40px)
│  결과 카드 4종 (grid 4열)                         │
│  자산 성장 로드맵 차트                             │
│  인플레이션 배너 (조건부)                          │
│                                                  │
└──────────────────────────────────────────────────┘
                              ↑ 플로팅 사이드바 (right: 20px)
```

### 5-2. Topbar

```css
height: 56px;
position: fixed; top: 0; left: 0; right: 0;
background: var(--bg-card);
border-bottom: 1px solid var(--border);
z-index: 100;
```

- 로고 영역: `width: 52px`, 우측 border 구분선
- 내부 여백: `padding: 0 20px`

### 5-3. 사이드바 (조정 패널)

```css
position: fixed;
top: 20px; right: 20px; bottom: 20px;
width: 380px;
background: rgba(255, 255, 255, 0.97);
border-radius: 16px;
box-shadow: 0 8px 40px rgba(0,0,0,0.14), 0 2px 12px rgba(0,0,0,0.08);
backdrop-filter: blur(20px);
transform: translateX(calc(100% + 24px));        /* 닫힘 상태 */
transition: transform 320ms cubic-bezier(0.4, 0, 0.2, 1);
z-index: 200;
```

- 열림: `transform: translateX(0)`
- 내부 패딩: `20px`
- 스크롤바: 기본 숨김, 스크롤 중 `rgba(0,0,0,0.18)` 얇은 형태로 등장

### 5-4. 콘텐츠 영역

```css
margin-top: 56px;      /* topbar 높이만큼 */
padding: 0 40px 48px;
```

---

## 6. 컴포넌트

### 6-1. 결과 카드

```css
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);     /* 16px */
  padding: 22px 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  transition: all var(--ease);
}
.card:hover { background: var(--bg-card-hover); }
```

구조:
```
.card-ico   아이콘 (Material Symbols, 22px)
.card-lbl   레이블 (11px, 700, uppercase, letter-spacing 0.5px)
.card-val   주요 숫자 (30px, 800)
.card-sub   부가 설명 (12px, text-3)
```

카드 값 컬러 클래스:
| 클래스 | 컬러 |
|--------|------|
| `.cv-primary` | `#111111` |
| `.cv-gold` | `#81CE16` |
| `.cv-violet` | `#999999` |
| `.cv-danger` | `#F4907A` |
| `.cv-success` | `#81CE16` |

### 6-2. 버튼

```css
/* 공통 */
.btn {
  padding: 8px 16px;
  border-radius: var(--r-sm);  /* 8px */
  font-size: 13px; font-weight: 600;
  transition: all var(--ease);
}

/* Primary (검정 배경) */
.btn-primary { background: #111111; color: #fff; }
.btn-primary:hover { background: #333333; transform: translateY(-1px); }

/* Outline */
.btn-outline { background: transparent; border: 1px solid var(--border-light); }
.btn-outline:hover { background: var(--bg-input); }

/* Ghost */
.btn-ghost { background: transparent; padding: 8px 10px; }
.btn-ghost:hover { background: var(--bg-input); }
```

Pill 버튼 (수정·공유 등 상단 액션):
```css
.pill-icon-btn {
  height: 30px; border-radius: 30px;
  padding: 0 10px; gap: 4px;
  border: 1px solid var(--border);
  font-size: 12px; font-weight: 500;
  transition: all 200ms ease;
}
.pill-icon-btn:hover {
  background: #111111; color: #ffffff;
  border-color: #111111; max-width: 180px;
  padding: 0 14px 0 10px;
}
```

### 6-3. 슬라이더 그룹

```
.sg                     ← 컨테이너 (flex column, gap: 7px)
  .sg-hd                ← 헤더 (레이블 ↔ 값)
    .sg-label           ← 13px, 500, text-1
    .sg-val-wrap        ← flex, align-items: baseline, gap: 3px, margin-top: 2px
      .sg-val           ← 15px, 800, min-width: 64px, text-right
      .sg-unit          ← 12px, text-3
  input[type="range"]   ← 커스텀 슬라이더
```

슬라이더 스타일:
```css
input[type="range"] {
  height: 2px;
  background: linear-gradient(to right, {color} {pct}%, #E0E0E0 {pct}%);
  /* 채움 색상 = PERSON_COLORS[인원 인덱스].line */
}
input[type="range"]::-webkit-slider-thumb {
  width: 11px; height: 11px; border-radius: 50%;
  background: var(--knob-color, var(--primary));
  transition: transform .15s ease;
}
input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}
```

### 6-4. 토글 스위치

```css
.sw {
  width: 38px; height: 21px;
  background: var(--border-light); border-radius: 11px;
}
.sw::after {
  width: 16px; height: 16px;
  background: #fff; border-radius: 50%;
  transition: transform var(--ease);
}
.toggle.on .sw { background: var(--primary); }
.toggle.on .sw::after { transform: translateX(17px); }
```

### 6-5. 프리셋 카드

```css
.preset-card {
  padding: 10px 12px;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
}
.preset-card.active {
  border-color: var(--primary);
  background: var(--primary-glow);
}
```

---

## 7. 차트 (자산 성장 로드맵)

라이브러리: **Chart.js 4.4.0**

### 7-1. 라인 스타일

```javascript
{
  type: 'line',
  borderColor: PERSON_COLORS[i % PERSON_COLORS.length].line,
  borderWidth: 2,
  borderCapStyle: 'round',
  borderJoinStyle: 'round',
  borderDash: [],            // solid (점선 없음)
  pointRadius: 0,
  pointHoverRadius: 0,
  pointHitRadius: 0,
  spanGaps: false,           // null 구간에서 라인 끊김
  clip: false,
}
```

글로벌 기본값 (initChart):
```javascript
Chart.defaults.elements.point.radius      = 0;
Chart.defaults.elements.point.hoverRadius = 0;
Chart.defaults.elements.point.hitRadius   = 0;
```

### 7-2. 축 스타일

```javascript
// X축
xAxis: {
  grid: { display: false },
  ticks: {
    font: { size: 10 },
    color: '#AAAAAA',
    callback: (val, index, ticks) => index === 0 ? `${age}세` : `${age}`,
  }
}

// Y축
yAxis: {
  grid: { display: false },
  ticks: {
    font: { size: 10 },
    color: '#AAAAAA',
    callback: (val, index, ticks) =>
      index === ticks.length - 1 ? `${uk}억` : `${uk}`,
  }
}
```

### 7-3. 툴팁

커스텀 HTML 툴팁. 기본 Chart.js 툴팁 비활성화.

```
┌──────────────────────────┐
│ [은퇴 시점 행]  ← hover 나이가 은퇴 나이와 일치 시에만 표시
│  59세          은퇴 예상  │  ← 13px bold / 11px gray
│  55세          목표 은퇴  │
│──────────────────────────│
│ [나이 행]  ← 은퇴 라벨 없을 때만 표시
│ 45세                     │  ← 11px, #6B7280
│──────────────────────────│
│ ● 미학        17.4억     │  ← 11px, 800
│──────────────────────────│
│ 차이          +0.0억     │  ← 보라색 (#7C3AED) / 빨간색
└──────────────────────────┘
```

툴팁 컨테이너:
```css
background: #fff;
border: 0.5px solid rgba(0,0,0,0.1);
border-radius: 10px;
padding: 10px 13px;
box-shadow: 0 4px 16px rgba(0,0,0,0.08);
min-width: 130px;
```

### 7-4. 수직 보조선 플러그인 (vertLinePlugin)

- hover 시 현재 x 위치에 수직 점선 표시
- `strokeStyle: rgba(0,0,0,0.15)`, `lineWidth: 1`, `setLineDash([4,4])`

### 7-5. 은퇴 시점 수직선 플러그인 (retirePlugin)

두 시점 표시:
- **은퇴 예상** (`_retire1Age`): 현재 페이스 기준 FIRE 달성 나이 → `rgba(0,0,0,0.12)`
- **목표 은퇴** (`_retire2Age`): 사용자 희망 은퇴 나이 → `rgba(0,0,0,0.07)`

```javascript
ctx.setLineDash([4, 4]);
ctx.lineWidth = 1;
ctx.strokeStyle = 'rgba(0,0,0,0.12)';   // 은퇴 예상
ctx.strokeStyle = 'rgba(0,0,0,0.07)';   // 목표 은퇴
```

---

## 8. 애니메이션

| 요소 | 방식 | 지속 시간 |
|------|------|-----------|
| 사이드바 열림/닫힘 | `translateX` cubic-bezier(0.4, 0, 0.2, 1) | 320ms |
| 카드 등장 | `fadeUp` (y: 12 → 0, opacity 0 → 1) | 0.45s, delay 0.1~0.3s |
| 히어로 숫자 등장 | scale + opacity spring | 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) |
| 버튼 호버 | `transform: translateY(-1px)` | 150ms ease |
| 슬라이더 썸 호버 | `scale(1.15)` | 150ms ease |
| 인플레이션 배너 | `fadeUp` | 0.5s cubic-bezier(0.4, 0, 0.2, 1) |

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

---

## 9. 아이콘 시스템

**Material Symbols Outlined** (Google Fonts CDN)

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,300,0,0" rel="stylesheet" />
```

사용법:
```html
<span class="ms">favorite</span>
<span class="ms">trending_up</span>
<span class="ms">bar_chart</span>
```

`.ms` 클래스: `font-family: 'Material Symbols Outlined'`, `font-weight: normal`, `vertical-align: middle`

---

## 10. 반응형 (미디어 쿼리)

```css
/* 모바일: ~768px */
@media (max-width: 768px) {
  .content { padding: 0 16px 48px; }
  .cards   { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .sidebar { top: 0; right: 0; bottom: 0; border-radius: 0; width: 100%; }
  .page-hd { flex-direction: column; align-items: flex-start; }
  .hero-row{ flex-direction: column; }
}
```

---

## 11. 스크롤바

```css
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
```

사이드바 내부: 평시 숨김 → 스크롤 중 `rgba(0,0,0,0.18)` 얇은 형태

---

## 12. 기술 스택 (현재 구현)

| 항목 | 선택 |
|------|------|
| 구조 | Single HTML file (vanilla) |
| 스타일 | Tailwind CSS CDN + 인라인 `<style>` |
| 차트 | Chart.js 4.4.0 (CDN) |
| 스크린샷 | html2canvas 1.4.1 (CDN) |
| 아이콘 | Material Symbols Outlined (Google Fonts) |
| 폰트 | Pretendard (시스템 폴백 포함) |
| 상태 | 전역 객체 `S` + URL 파라미터 공유 |

---

*이 문서는 index.html 구현 기준으로 작성되었습니다. 디자인 결정이 바뀔 때 함께 업데이트하세요.*
