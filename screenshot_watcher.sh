#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  파라다이스 계산기 — 디자인 변경 감지 & 자동 스크린샷 저장
#  저장 위치: ~/Downloads/paradise_vXXX_YYYY-MM-DD_HHmmss.png
#
#  사용법: bash screenshot_watcher.sh
#  종료:   Ctrl+C
# ─────────────────────────────────────────────────────────────

WATCH_DIR="$(cd "$(dirname "$0")" && pwd)"
WATCH_FILES=("index.html" "onboarding.html")
DOWNLOADS="$HOME/Downloads"
SERVER_PORT=8787
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VERSION=1

log() { echo "[$(date '+%H:%M:%S')] $*"; }

# ── 서버 시작 ──────────────────────────────────────────────
start_server() {
  if lsof -ti:$SERVER_PORT >/dev/null 2>&1; then
    log "서버 이미 실행 중 (port $SERVER_PORT)"
    return
  fi
  cd "$WATCH_DIR"
  python3 -m http.server $SERVER_PORT >/dev/null 2>&1 &
  SERVER_PID=$!
  sleep 1
  log "서버 시작 (PID $SERVER_PID, port $SERVER_PORT)"
}

# ── 스크린샷 촬영 ──────────────────────────────────────────
take_screenshot() {
  local page="$1"  # index or onboarding
  local ts=$(date '+%Y-%m-%d_%H%M%S')
  local fname="paradise_v$(printf '%03d' $VERSION)_${page}_${ts}.png"
  local out="$DOWNLOADS/$fname"

  log "📸 스크린샷: $fname"
  sleep 1.5  # 브라우저 렌더링 대기

  "$CHROME" \
    --headless=new \
    --screenshot="$out" \
    --window-size=1440,900 \
    --no-sandbox \
    --disable-gpu \
    --hide-scrollbars \
    "http://localhost:$SERVER_PORT/${page}.html" \
    >/dev/null 2>&1

  if [[ -f "$out" ]]; then
    log "✅ 저장: ~/Downloads/$fname ($(du -h "$out" | cut -f1))"
  else
    log "❌ 스크린샷 실패"
  fi
  VERSION=$((VERSION + 1))
}

# ── 변경 감지 루프 ─────────────────────────────────────────
watch_loop() {
  declare -A last_mtime

  # 초기 mtime 기록
  for f in "${WATCH_FILES[@]}"; do
    local fpath="$WATCH_DIR/$f"
    [[ -f "$fpath" ]] && last_mtime[$f]=$(stat -f '%m' "$fpath" 2>/dev/null || stat -c '%Y' "$fpath" 2>/dev/null)
  done

  log "🔍 감지 시작: ${WATCH_FILES[*]}"
  log "   변경될 때마다 ~/Downloads/ 에 자동 저장됩니다"

  while true; do
    for f in "${WATCH_FILES[@]}"; do
      local fpath="$WATCH_DIR/$f"
      [[ ! -f "$fpath" ]] && continue
      local cur_mtime=$(stat -f '%m' "$fpath" 2>/dev/null || stat -c '%Y' "$fpath" 2>/dev/null)

      if [[ "${last_mtime[$f]}" != "$cur_mtime" ]]; then
        log "🔄 변경 감지: $f"
        last_mtime[$f]="$cur_mtime"
        local page="${f%.html}"
        take_screenshot "$page"
      fi
    done
    sleep 2
  done
}

# ── 초기 스크린샷 ──────────────────────────────────────────
initial_screenshots() {
  log "📸 초기 스크린샷 촬영..."
  for f in "${WATCH_FILES[@]}"; do
    take_screenshot "${f%.html}"
  done
}

# ── 종료 핸들러 ────────────────────────────────────────────
cleanup() {
  log "👋 종료"
  [[ -n "$SERVER_PID" ]] && kill "$SERVER_PID" 2>/dev/null
  exit 0
}
trap cleanup INT TERM

# ── 메인 ──────────────────────────────────────────────────
log "🌴 파라다이스 계산기 스크린샷 와처 시작"
start_server
initial_screenshots
watch_loop
