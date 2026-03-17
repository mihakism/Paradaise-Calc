#!/usr/bin/env python3
"""Onboarding flow screenshots: sections 1-5, persona select, dashboard."""
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        try:
            print("Navigating...")
            page.goto("http://localhost:8787/index.html", wait_until="domcontentloaded", timeout=8000)
            page.reload(wait_until="domcontentloaded")
            print("Hard refresh done.")

            # Ensure onboarding is visible (not skipped by URL params)
            page.wait_for_selector("#page-onboarding", timeout=3000)
            page.wait_for_selector("#s1", timeout=2000)
            page.wait_for_timeout(500)

            # 1. Section 1 - initial load
            page.screenshot(path=OUT / "ob1.png", full_page=False)
            print("Saved: ob1.png (section 1)")

            # Click "다음 →" 4 times to reach section 5
            for i in range(4):
                btn = page.locator("button.btn-next").first
                btn.click()
                page.wait_for_timeout(600)  # scroll + animation

            # 5. Section 5 - preview + persona cards
            page.wait_for_timeout(400)
            page.screenshot(path=OUT / "ob5.png", full_page=False)
            print("Saved: ob5.png (section 5)")

            # Click "이지현 · 안정형" persona card
            page.locator("#pc-stable").click()
            page.wait_for_timeout(300)

            # Click "내 낙원 보기 →" CTA
            page.locator("#btn-cta").click()
            page.wait_for_timeout(800)  # transition to dashboard

            # Dashboard
            page.wait_for_selector("#page-dashboard", timeout=3000)
            page.wait_for_timeout(500)
            page.screenshot(path=OUT / "dash_new.png", full_page=True)
            print("Saved: dash_new.png (dashboard)")

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    main()
