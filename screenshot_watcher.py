#!/usr/bin/env python3
"""
파라다이스 계산기 — 디자인 변경 감지 & 자동 스크린샷 저장
저장 위치: ~/Downloads/paradise_vXXX_<page>_YYYY-MM-DD_HHmmss.png

사용법: python3 screenshot_watcher.py
종료:   Ctrl+C
"""

import os
import sys
import time
import signal
import subprocess
import threading
from datetime import datetime
from pathlib import Path

WATCH_DIR   = Path(__file__).parent.resolve()
WATCH_FILES = ["index.html", "onboarding.html"]
DOWNLOADS   = Path.home() / "Downloads"
PORT        = 8787
CHROME      = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
version     = [1]   # mutable counter
server_proc = [None]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# ── HTTP 서버 ──────────────────────────────────────────────
def start_server():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', PORT)) == 0:
            log(f"서버 이미 실행 중 (port {PORT})")
            return
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=str(WATCH_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    server_proc[0] = proc
    time.sleep(1)
    log(f"서버 시작 (PID {proc.pid}, port {PORT})")

# ── 스크린샷 촬영 ──────────────────────────────────────────
def take_screenshot(page: str):
    ts    = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    fname = f"paradise_v{version[0]:03d}_{page}_{ts}.png"
    out   = str(DOWNLOADS / fname)

    log(f"📸 스크린샷: {fname}")
    time.sleep(1.5)   # 렌더링 대기

    subprocess.run(
        [
            CHROME,
            "--headless=new",
            f"--screenshot={out}",
            "--window-size=1440,900",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            f"http://localhost:{PORT}/{page}.html",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if os.path.isfile(out):
        size_kb = os.path.getsize(out) // 1024
        log(f"✅ 저장: ~/Downloads/{fname} ({size_kb}KB)")
    else:
        log("❌ 스크린샷 실패")

    version[0] += 1

# ── 변경 감지 루프 ─────────────────────────────────────────
def watch_loop():
    mtimes = {}
    for f in WATCH_FILES:
        p = WATCH_DIR / f
        if p.exists():
            mtimes[f] = p.stat().st_mtime

    log(f"🔍 감지 시작: {', '.join(WATCH_FILES)}")
    log("   파일이 저장될 때마다 ~/Downloads/ 에 자동 스크린샷이 저장됩니다")

    while True:
        for f in WATCH_FILES:
            p = WATCH_DIR / f
            if not p.exists():
                continue
            cur = p.stat().st_mtime
            if mtimes.get(f) != cur:
                log(f"🔄 변경 감지: {f}")
                mtimes[f] = cur
                page = f.replace(".html", "")
                take_screenshot(page)
        time.sleep(2)

# ── 종료 핸들러 ────────────────────────────────────────────
def cleanup(sig=None, frame=None):
    log("👋 종료")
    if server_proc[0]:
        server_proc[0].terminate()
    sys.exit(0)

signal.signal(signal.SIGINT,  cleanup)
signal.signal(signal.SIGTERM, cleanup)

# ── 메인 ──────────────────────────────────────────────────
if __name__ == "__main__":
    log("🌴 파라다이스 계산기 스크린샷 와처 시작")
    log(f"   감지 폴더: {WATCH_DIR}")
    log(f"   저장 폴더: {DOWNLOADS}")

    start_server()

    log("📸 초기 스크린샷 촬영...")
    for f in WATCH_FILES:
        take_screenshot(f.replace(".html", ""))

    watch_loop()
