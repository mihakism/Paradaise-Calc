# 파라다이스 계산기 v2.0 — DESIGN SPEC

> Cursor 구현 지시서 · 2026.03
> 이 문서는 PRD.md와 함께 사용합니다.

---

## 0. 레퍼런스 사이트


| 사이트              | URL                                                            | 참고할 요소                                        |
| ---------------- | -------------------------------------------------------------- | --------------------------------------------- |
| savor.it         | [https://www.savor.it/](https://www.savor.it/)                 | 온보딩 구조 — 풀스크린 섹션마다 배경이 전환되는 스크롤 경험            |
| ProjectionLab    | [https://projectionlab.app/](https://projectionlab.app/)       | 대시보드 레이아웃 — 왼쪽 입력 패널 + 오른쪽 그래프 고정 2-column 구조 |
|                  |                                                                |                                               |
| Stripe Dashboard | [https://dashboard.stripe.com/](https://dashboard.stripe.com/) | 결과 카드 컴포넌트 — 숫자 크게 강조, 깔끔한 metric card 스타일    |
| Robinhood        | [https://robinhood.com/](https://robinhood.com/)               | 자산 성장 그래프 — 감성적인 라인 차트, 호버 인터랙션               |


---

## 1. UI Flow

```
[온보딩 페이지] ──→ [대시보드 페이지] ──→ [설정 모달]
   첫 진입 시            메인 경험           값 수정 시만
   (풀스크린 스텝)       (계산 결과)          (오버레이)
```

- 온보딩 완료 후 대시보드로 이동 시 페이지 전환 애니메이션 적용
- 설정 모달은 대시보드 위에 오버레이로 등장 (별도 페이지 이동 없음)
- 새로고침 시 온보딩부터 다시 시작 (localStorage 저장 없음)

---

## 2. 컬러 시스템

```css
--bg-primary:    #0F1117;   /* 메인 배경 */
--bg-card:       #1A1D2E;   /* 카드 배경 */
--color-primary: #1E4FBF;   /* 브랜드 블루 */
--color-accent:  #0FAD77;   /* 낙원 그린 */
--color-warning: #F59E0B;   /* 강조 오렌지 */
--text-primary:  #F9FAFB;   /* 메인 텍스트 */
--text-sub:      #6B7280;   /* 서브 텍스트 */
--border:        #2D3148;   /* 보더 */
```

---

## 3. 타이포그래피

```css
/* 폰트 */
한글: Pretendard
숫자/영문: Inter

/* 결과 숫자 (카드 메인) */
font-size: 48px;
font-weight: 800;
color: var(--color-accent);

/* 단위 텍스트 (억, 만원, 세) */
font-size: 28px;   /* 숫자의 60% 크기 */
font-weight: 600;
color: var(--text-sub);

/* 섹션 타이틀 */
font-size: 32px;
font-weight: 700;

/* 본문 */
font-size: 16px;
font-weight: 400;
```

---

## 4. 온보딩 페이지

### 4-1. 전체 구조

- 5개 섹션, 각 섹션 height: 100vh
- **스크롤은 시각적 효과만** / 실제 진행은 버튼 또는 Enter 키
- 마우스 휠·터치 스와이프로는 섹션 이동 불가 → `wheel` 이벤트 `preventDefault()` 처리

### 4-2. 섹션 구성

```
Section 1  현재 나이       배경: #0F1117 → #1A1D2E  (새벽)
Section 2  월 저축액       배경: #1A1D2E → #1E3A5F  (일출)
Section 3  은퇴 희망 나이  배경: #1E3A5F → #0D4F3C  (노을)
Section 4  희망 월 인출액  배경: #0D4F3C → #0FAD77  (낙원)
Section 5  결과 프리뷰     배경: #0FAD77 → #1E4FBF  (도달)
```

각 섹션 중앙에 질문 텍스트 + 슬라이더 + 숫자 입력 필드 배치

### 4-3. 진행 방식

- 값 입력 후 **Enter 키** 또는 **"다음 →" 버튼** 클릭 → 다음 섹션으로 이동
- 섹션 이동: `scrollIntoView({ behavior: 'smooth' })` duration 800ms, ease-in-out
- 입력값 없이 다음 클릭 시 → 입력 필드 shake 애니메이션 (Framer Motion)
- 이전 섹션 돌아갈 때 입력값 유지
- 각 섹션 진입 시 입력 필드 자동 포커스 (autoFocus)

### 4-4. 배경 전환 애니메이션

- Framer Motion `AnimatePresence` 사용
- 배경: opacity + scale 크로스페이드 (duration 600ms)
- 콘텐츠: y: 20 → 0, opacity: 0 → 1 (duration 500ms, ease-out)

### 4-5. Section 5 결과 프리뷰

```
"35세부터 시작하면 50세에 낙원 도달 가능 🌴"

[필요 자산 미리보기]  [월 저축 미리보기]

페르소나 선택:  [ 안정형 ]  [ 공격형 ]
(선택 시 수익률·저축증가율 자동 세팅)

[ 내 낙원 보기 → ]  ← CTA 버튼, 호버 시 글로우 효과
```

### 4-6. 온보딩 → 대시보드 전환

- CTA 클릭 시 전체 페이지 페이드아웃 후 대시보드 페이드인 (duration 600ms)

---

## 5. 대시보드 페이지

### 5-1. 레이아웃 (데스크탑)

```
┌──────────────────────────────────────────────────┐
│  Header: 로고 + "내 낙원까지 D-17년"  +  ⚙️ 설정  │
├──────────────────────────────────────────────────┤
│  결과 카드 3종 (가로 배열, 1/3씩)                  │
│  [필요 자산 9억]   [월 저축 187만]   [은퇴 50세]   │
├──────────────────────────────────────────────────┤
│                                                  │
│  자산 성장 그래프 (메인 영역, height: 400px)       │
│                                                  │
├──────────────────────────────────────────────────┤
│  시나리오 A/B 비교 토글  +  공유 버튼              │
└──────────────────────────────────────────────────┘
```

### 5-2. 레이아웃 (모바일)

```
그래프 → 결과 카드 3종 (세로 스택) → 시나리오 비교
```

### 5-3. 결과 카드 스펙

- 대시보드 첫 진입 시 카드 3종 순차 페이드인 (stagger 0.15초)
- 숫자 카운트업 애니메이션: `react-countup`, duration 1.2초, 0에서 목표값까지
- 카드 구성:

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  필요 은퇴 자산  │  │  월 필요 저축액  │  │  은퇴 가능 나이  │
│                 │  │                 │  │                 │
│    9억          │  │    187만원       │  │    50세          │
│                 │  │                 │  │                 │
│ 현재 페이스 기준 │  │ 지금 저축 + α   │  │ 🌴 낙원까지     │
│                 │  │                 │  │    D-15년        │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### 5-4. 그래프 스펙 (Recharts 기준)

```jsx
// 진입 애니메이션
isAnimationActive={true}
animationDuration={1500}
animationEasing="ease-out"

// 은퇴 시점 표시
<ReferenceLine
  x={retirementYear}
  stroke="#0FAD77"
  strokeDasharray="6 3"
  label={{ value: "🌴 낙원 도달", fill: "#0FAD77", fontSize: 13 }}
/>

// 커스텀 툴팁
// 해당 연도 / 자산액 / 은퇴까지 N년 표시

// 슬라이더 변경 시 부드러운 업데이트
// key prop 변경으로 리렌더 트리거, 300ms ease-out
```

---

## 6. 설정 모달

### 6-1. 진입

- 대시보드 우상단 ⚙️ 버튼 클릭
- 배경 블러 (`backdrop-filter: blur(8px)`) + 모달 슬라이드인 (y: 40 → 0, duration 400ms)

### 6-2. 구성

```
기본 설정
  • 현재 나이
  • 월 저축액
  • 은퇴 희망 나이
  • 희망 월 인출액

고급 설정 (접이식 토글)
  • 기대 수익률 (기본값: 페르소나 프리셋)
  • 인플레이션율 (기본값: 2.5%)
  • 저축 증가율

[ 다시 계산하기 ]  버튼 → 모달 닫힘 + 그래프 업데이트
```

---

## 7. 공통 컴포넌트 스펙

### 슬라이더

- 슬라이더 + 숫자 직접 입력 병행
- 드래그 시 숫자 카운터 애니메이션 (react-countup)
- 주요 입력값에 추천 기본값 툴팁 표시

### 버튼

```css
/* Primary CTA */
background: var(--color-accent);
border-radius: 12px;
font-weight: 700;
/* 호버 시 */
box-shadow: 0 0 20px rgba(15, 173, 119, 0.4);  /* 글로우 */
transform: translateY(-1px);
transition: all 200ms ease;
```

### 카드

```css
background: var(--bg-card);
border: 1px solid var(--border);
border-radius: 16px;
padding: 24px;
box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
```

---

## 8. 기술 스택

```
프레임워크:     Next.js (App Router)
스타일링:       Tailwind CSS
애니메이션:     Framer Motion
그래프:         Recharts
숫자 애니메이션: react-countup
폰트:           Pretendard (한글), Inter (영문)
아이콘:         lucide-react
```

---

## 9. 성능 제약

- 초기 로드: LCP < 2.5초 (모바일 4G)
- 그래프 반응: 입력 변경 후 < 300ms
- 모든 계산: 클라이언트 사이드 only (서버 요청 없음)
- 브라우저: Chrome / Safari / Firefox 최신 2버전

---

*이 문서는 PRD.md와 함께 Cursor에 제공합니다.*
*디자인 결정이 바뀔 때마다 이 파일을 업데이트하세요.*