"""
pytest 全局配置 & fixtures
"""

import os
import sys
import pytest
from playwright.sync_api import sync_playwright

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件路径
AUTH_FILE = os.path.join(ROOT_DIR, "config", "auth.json")
HAS_AUTH = os.path.exists(AUTH_FILE)
CAPTCHA_CODE = os.getenv("CAPTCHA_CODE")
NEEDS_CAPTCHA_INPUT = not CAPTCHA_CODE

# pytest mark: 需要手动输入验证码的测试自动跳过
requires_captcha = pytest.mark.skipif(
    NEEDS_CAPTCHA_INPUT,
    reason="需要验证码但未设置 CAPTCHA_CODE。用法: CAPTCHA_CODE=xxxx pytest -v",
)


@pytest.fixture(scope="session")
def browser():
    """浏览器实例（session 级别，整个测试运行共享）"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """空白页面 — 无登录状态，用于测试登录表单本身"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_in_page(browser):
    """已登录页面 — 加载 auth.json，用于测试登录后功能"""
    if not HAS_AUTH:
        pytest.skip("auth.json 不存在，请先运行 scripts/save_auth.py 保存登录状态")
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()
    yield page
    context.close()
