#!/usr/bin/env python3
"""
Test script for 낙원계산기 (Paradise Calculator) - captures screenshots at each step.
Run: python3 test_paradise_calc.py
Requires: pip install playwright && playwright install chromium
"""

import asyncio
import os
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install chromium")
    exit(1)


BASE_URL = "http://localhost:8787/index.html"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


async def main():
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    screenshots = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            ignore_https_errors=True,
        )
        page = await context.new_page()

        # Capture console messages
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

        try:
            # Step 1: Navigate and screenshot
            print("Step 1: Navigating to", BASE_URL)
            await page.goto(BASE_URL, wait_until="networkidle", timeout=15000)
            await asyncio.sleep(1.5)  # Let chart render
            path1 = SCREENSHOT_DIR / "01_initial.png"
            await page.screenshot(path=path1, full_page=True)
            screenshots.append(("Initial page load", path1))
            print(f"  Screenshot: {path1}")

            # Step 2: Move monthly savings slider to far right
            print("Step 2: Moving 월 저축액 slider to max")
            slider = page.locator('#sl-a-monthlySavings')
            await slider.evaluate("el => { el.value = el.max; el.dispatchEvent(new Event('input', { bubbles: true })); }")
            await asyncio.sleep(0.5)
            path2 = SCREENSHOT_DIR / "02_slider_max.png"
            await page.screenshot(path=path2, full_page=True)
            screenshots.append(("Monthly savings at max", path2))
            print(f"  Screenshot: {path2}")

            # Step 3: Click 김민준 preset
            print("Step 3: Clicking 김민준 preset")
            preset = page.locator('.preset-btn').filter(has_text='김민준')
            await preset.click()
            await asyncio.sleep(0.5)
            path3 = SCREENSHOT_DIR / "03_preset_minjun.png"
            await page.screenshot(path=path3, full_page=True)
            screenshots.append(("김민준 preset applied", path3))
            print(f"  Screenshot: {path3}")

            # Step 4: Toggle 시나리오 B 비교
            print("Step 4: Enabling 시나리오 B 비교")
            toggle_b = page.locator('#toggle-scenario-b')
            await toggle_b.click()
            await asyncio.sleep(0.5)
            path4 = SCREENSHOT_DIR / "04_scenario_b.png"
            await page.screenshot(path=path4, full_page=True)
            screenshots.append(("Scenario B enabled", path4))
            print(f"  Screenshot: {path4}")

            # Step 5: Toggle 인플레이션 반영
            print("Step 5: Enabling 인플레이션 반영")
            toggle_inf = page.locator('#toggle-inflation')
            await toggle_inf.click()
            await asyncio.sleep(0.5)
            path5 = SCREENSHOT_DIR / "05_inflation.png"
            await page.screenshot(path=path5, full_page=True)
            screenshots.append(("Inflation enabled", path5))
            print(f"  Screenshot: {path5}")

            # Step 6: Click 공유하기 button
            print("Step 6: Clicking 공유하기 (share) button")
            share_btn = page.locator('#btn-share')
            await share_btn.click()
            await asyncio.sleep(0.8)  # Wait for "복사됨!" feedback
            path6 = SCREENSHOT_DIR / "06_share_clicked.png"
            await page.screenshot(path=path6, full_page=True)
            screenshots.append(("Share button clicked", path6))
            print(f"  Screenshot: {path6}")

        except Exception as e:
            print(f"Error: {e}")
            await page.screenshot(path=SCREENSHOT_DIR / "error.png", full_page=True)
            raise
        finally:
            await browser.close()

    # Print console logs
    print("\n--- Console output ---")
    for log in console_logs:
        print(log)

    print("\n--- Screenshots saved ---")
    for label, path in screenshots:
        print(f"  {label}: {path}")

    return screenshots, console_logs


if __name__ == "__main__":
    asyncio.run(main())
