---
name: gajago-sns
description: 경기도교육청 취창업지원센터 SNS 콘텐츠 자동 생성. /가자고 명령어로 텍스트/키워드/이미지를 입력하면 인스타그램, 페이스북, 밴드용 카피 + 이미지 + 20초 영상을 자동 생성. Trigger on /가자고 command.
---

# 가자고 SNS 자동화 스킬

경기도교육청 취창업지원센터 홍보 콘텐츠를 자동 생성하는 스킬.

## 트리거
- `/가자고 [내용]` — 텍스트/키워드로 SNS 콘텐츠 생성
- `/가자고` (내용 없음) — 웹앱 열기

## 브랜드 아이덴티티
- 기관명: 경기도교육청 취창업지원센터
- 주 컬러: #FF5733 (코랄), #1A2E5A (네이비), #6DCC5A (라임)
- 폰트: Pretendard (한글), Space Grotesk (영문)
- 채널: 인스타그램 피드(1080×1080), 페이스북(1200×630), 밴드(1080×1080)

## 실행 흐름

### 1단계: 입력 파싱
- 슬래시 명령어 뒤 텍스트를 콘텐츠 소스로 사용
- 첨부 이미지가 있으면 → 나노바나나로 사진 오버레이 합성
- 첨부 이미지가 없으면 → 나노바나나로 AI 이미지 생성
- 텍스트만 있으면 → 카피라이팅만 생성

### 2단계: Gemini API로 카피 생성
```bash
# 웹앱 API 호출
curl -s -X POST http://localhost:3000/api/copy \
  -H "Content-Type: application/json" \
  -d '{
    "text": "[입력내용]",
    "channels": ["instagram-feed", "facebook", "band"]
  }'
```

웹앱이 꺼져있으면 먼저 실행:
```bash
cd /Users/isangsu/.openclaw/workspace/artifacts/gajago-sns && npm run dev > /tmp/gajago-dev.log 2>&1 &
sleep 4
```

### 3단계: 이미지 생성

#### A. 첨부 사진이 있을 때 (사진 + 오버레이 합성)
나노바나나 스킬 사용 — 실제 사진 위에 세련된 텍스트 오버레이:
```bash
GEMINI_API_KEY=AIzaSyBQT2FhiIJL_j69kDdOVYkP5P69avNrHsc \
uv run ~/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[채널별 오버레이 프롬프트 - 아래 참조]" \
  --input-image "[첨부파일경로]" \
  --filename "YYYY-MM-DD-gajago-[채널].png" \
  --resolution 4K
```

**채널별 오버레이 프롬프트 템플릿:**

인스타그램:
```
World-class Korean editorial designer. Keep the photo as main subject with cinematic color grade.
Add premium overlay: top-left coral badge '[배지텍스트]', bottom dark navy gradient (60% opacity),
coral accent line, white bold Korean title '[타이틀]', light gray subtitle '[서브]', date '[날짜]'.
Apple product launch aesthetic. Zero cartoon elements. Editorial magazine quality.
```

페이스북:
```
Premium Facebook landscape post. Two-column: left 40% deep navy panel with white Korean text
'[타이틀]' ExtraBold, coral divider, '[서브]' details, coral badge '[배지]'. 
Right 60%: the actual photo with edge blend. Bloomberg/FT editorial style.
```

밴드:
```
Premium Korean Band community post. Photo as hero with warm cinematic grade.
Top frosted glass bar: '[기관명]' white bold. Bottom gradient: coral badge '[배지]',
white ExtraBold '[타이틀]', subtitle '[서브]', 3 checkmark items.
Warm, trustworthy, premium magazine style.
```

#### B. 첨부 사진이 없을 때 (AI 이미지 생성)
```bash
GEMINI_API_KEY=AIzaSyBQT2FhiIJL_j69kDdOVYkP5P69avNrHsc \
uv run ~/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Professional Korean government SNS poster. [내용]. Navy #1A2E5A, Coral #FF5733, Lime #6DCC5A. Modern editorial style." \
  --filename "YYYY-MM-DD-gajago-[채널].png" \
  --resolution 2K
```

### 4단계: 영상 생성 (사진 있을 때)
Python 스크립트로 20초 슬라이드쇼 영상 생성:

```bash
python3 /Users/isangsu/.openclaw/workspace/skills/gajago-sns/scripts/make_video.py \
  --photos "[사진경로들 쉼표구분]" \
  --scenes "[장면텍스트 JSON]" \
  --output "/Users/isangsu/.openclaw/media/outbound/YYYY-MM-DD-gajago-video.mp4"
```

### 5단계: 결과 전달
- 이미지 3장 (인스타/페이스북/밴드) → 텔레그램으로 전송
- 카피 텍스트 → 채널별 정리해서 메시지로 전송
- 영상 → Finder 폴더 열기 (파일 크기 커서 텔레그램 직접 전송 대신)
- 저장 위치 안내: `/Users/isangsu/.openclaw/media/outbound/`

## 출력 파일명 규칙
- `YYYY-MM-DD-gajago-instagram.png`
- `YYYY-MM-DD-gajago-facebook.png`
- `YYYY-MM-DD-gajago-band.png`
- `YYYY-MM-DD-gajago-video.mp4`
- `YYYY-MM-DD-gajago-카피.txt`

## 환경변수
- `GEMINI_API_KEY=AIzaSyBQT2FhiIJL_j69kDdOVYkP5P69avNrHsc`
- 웹앱: `http://localhost:3000` (gajago-sns Next.js 앱)
- 웹앱 경로: `/Users/isangsu/.openclaw/workspace/artifacts/gajago-sns/`

## 웹앱 직접 접속
- 로컬: http://localhost:3000
- 배우자분 사용: Vercel 배포 후 URL 공유

## 주의사항
- 실제 인물 사진 있으면 반드시 사진 기반으로 제작 (AI 생성보다 훨씬 퀄리티↑)
- 이미지 3채널 병렬 생성 (`&` 백그라운드)
- 생성 완료 후 Finder에서 폴더 자동 오픈
- 배경음악: `/tmp/gajago-bgm-new.mp3` 우선 사용 (없으면 SoundHelix Song-8 다운로드)
  ```bash
  curl -L "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3" -o /tmp/gajago-bgm-new.mp3
  ```
- 텍스트 오버레이: 화면 **하단** 배치 (bottom_margin=52, 하단 30% 그라데이션)
- 영상 스크립트: `scripts/make_video.py` (v3 — 하단 텍스트 + 밝은 BGM 반영)
