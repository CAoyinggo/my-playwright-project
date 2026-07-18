"""
保存登录状态 — 自动填入账号密码，你只需输入验证码。

用法:
    python scripts/save_auth.py
"""

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv("config/.env")

AUTH_FILE = "config/auth.json"
LOGIN_URL = os.getenv("LOGIN_URL", "https://test.panqu.com/login")
USERNAME = os.getenv("LOGIN_USERNAME", "161")
PASSWORD = os.getenv("LOGIN_PASSWORD", "123456")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(LOGIN_URL, wait_until="networkidle")

    page.locator("#pd-form-username").fill(USERNAME)
    page.locator("#pd-form-password").fill(PASSWORD)

    print("=" * 50)
    print(f"  账号: {USERNAME}")
    print(f"  密码: {PASSWORD}")
    print("  已自动填入！")
    print("=" * 50)
    print()
    print("  → 在浏览器中输入验证码，点击「登 录」")
    print("  → 登录成功后，回到这里按 Enter")
    print()

    input()

    context.storage_state(path=AUTH_FILE)
    print(f"\n✅ 登录状态 → {AUTH_FILE}")
    browser.close()
