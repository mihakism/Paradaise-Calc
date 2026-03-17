#!/usr/bin/env python3
"""
파라다이스 계산기 — 디자인 변경 감지 & 자동 풀페이지 스크린샷 저장
저장 위치: ~/Downloads/스크린샷/paradise_vXXX_<page>_YYYY-MM-DD_HHmmss.png

사용법: python3 screenshot_watcher.py
종료:   Ctrl+C
"""

import os, sys, time, signal, socket, subprocess, struct
from datetime import datetime
from pathlib import Path

WATCH_DIR   = Path(__file__).parent.resolve()
WATCH_FILES = ["index.html", "onboarding.html"]
SAVE_DIR    = Path.home() / "Downloads" / "스크린샷"
HTTP_PORT   = 8787
CHROME      = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 페이지별 뷰포트 높이 (모든 콘텐츠가 보이는 높이)
PAGE_HEIGHTS = {
    "index":      3000,   # 대시보드: 카드 2행 + 차트 + 제안영역
    "onboarding": 1200,   # 온보딩: 랜딩/스텝 화면
}
WIDTH       = 1440
RENDER_WAIT = 1.8          # JS 렌더링 대기 (초)

version     = [1]
server_proc = [None]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

SAVE_DIR.mkdir(parents=True, exist_ok=True)

# ─── HTTP 서버 ────────────────────────────────
def start_http_server():
    with socket.socket() as s:
        if s.connect_ex(('localhost', HTTP_PORT)) == 0:
            log(f"HTTP 서버 이미 실행 중 (:{HTTP_PORT})")
            return
    p = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(HTTP_PORT)],
        cwd=str(WATCH_DIR),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    server_proc[0] = p
    time.sleep(0.8)
    log(f"HTTP 서버 시작 (PID {p.pid}, :{HTTP_PORT})")

# ─── 스크린샷 촬영 ───────────────────────────
def take_screenshot(page: str):
    height = PAGE_HEIGHTS.get(page, 2000)
    ts     = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    fname  = f"paradise_v{version[0]:03d}_{page}_{ts}.png"
    out    = SAVE_DIR / fname

    log(f"📸 {fname}")
    time.sleep(RENDER_WAIT)

    result = subprocess.run(
        [
            CHROME, "--headless=new",
            f"--screenshot={out}",
            f"--window-size={WIDTH},{height}",
            "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--disable-features=TranslateUI",
            f"http://localhost:{HTTP_PORT}/{page}.html",
        ],
        capture_output=True, timeout=30,
    )

    if out.exists():
        # PNG 헤더에서 실제 크기 읽기
        try:
            raw = out.read_bytes()
            w = struct.unpack(">I", raw[16:20])[0]
            h = struct.unpack(">I", raw[20:24])[0]
            size_kb = out.stat().st_size // 1024
            log(f"✅ 저장: {fname}  ({w}×{h}px, {size_kb}KB)")
        except Exception:
            log(f"✅ 저장: {fname}  ({out.stat().st_size // 1024}KB)")
        version[0] += 1
    else:
        err = result.stderr.decode(errors="ignore")[:200]
        log(f"❌ 실패: {err}")

# ─── 변경 감지 루프 ──────────────────────────
def watch_loop():
    mtimes = {f: (WATCH_DIR / f).stat().st_mtime
              for f in WATCH_FILES if (WATCH_DIR / f).exists()}
    log(f"🔍 감지 시작: {', '.join(WATCH_FILES)}")
    log( "   파일 저장 → ~/Downloads/스크린샷/ 에 자동 저장됩니다")

    while True:
        for f in WATCH_FILES:
            p = WATCH_DIR / f
            if not p.exists(): continue
            cur = p.stat().st_mtime
            if mtimes.get(f) != cur:
                log(f"🔄 변경 감지: {f}")
                mtimes[f] = cur
                take_screenshot(f.replace(".html", ""))
        time.sleep(2)

# ─── 종료 처리 ───────────────────────────────
def cleanup(*_):
    log("👋 종료")
    if server_proc[0]:
        try: server_proc[0].terminate()
        except: pass
    sys.exit(0)

signal.signal(signal.SIGINT,  cleanup)
signal.signal(signal.SIGTERM, cleanup)

# ─── 메인 ────────────────────────────────────
if __name__ == "__main__":
    log("🌴 파라다이스 계산기 풀페이지 스크린샷 와처 시작")
    log(f"   저장 폴더: {SAVE_DIR}")

    start_http_server()

    log("📸 초기 스크린샷 촬영...")
    for f in WATCH_FILES:
        take_screenshot(f.replace(".html", ""))

    watch_loop()
