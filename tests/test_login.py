"""
盼趣网 (test.panqu.com) 登录测试

用法:
    # 日常使用（登录后测试直接复用 auth.json）
    python -m pytest tests/ -v

    # 有验证码时跑全部
    CAPTCHA_CODE=xxxx python -m pytest tests/ -v

    # 首次使用：先保存登录状态
    python scripts/save_auth.py
"""

import os
import pytest
from playwright.sync_api import Page, expect
from dotenv import load_dotenv

# ── 配置 ──────────────────────────────────────────────
load_dotenv("config/.env")

AUTH_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "auth.json")
HAS_AUTH = os.path.exists(AUTH_FILE)
CAPTCHA_CODE = os.getenv("CAPTCHA_CODE")

requires_captcha = pytest.mark.skipif(
    not CAPTCHA_CODE,
    reason="需要验证码但未设置 CAPTCHA_CODE。用法: CAPTCHA_CODE=xxxx pytest -v",
)

LOGIN_URL = os.getenv("LOGIN_URL", "https://test.panqu.com/login")
TARGET_URL = os.getenv("TARGET_URL", "https://test.panqu.com/projects")
USERNAME = os.getenv("LOGIN_USERNAME", "161")
PASSWORD = os.getenv("LOGIN_PASSWORD", "123456")


# ── 工具函数 ──────────────────────────────────────────

def _fill_captcha(page: Page) -> str:
    """获取验证码并返回。优先读环境变量，否则截图让用户手动输入。"""
    code = os.getenv("CAPTCHA_CODE")
    if code:
        print(f"   验证码（环境变量）: {code}")
        return code

    page.locator(".captcha-img").screenshot(path="screenshots/captcha.png")
    print("   验证码截图 → screenshots/captcha.png")
    return input("   请输入验证码: ").strip()


# ── 登录表单测试 ──────────────────────────────────────

class TestLoginForm:
    """登录页表单验证"""

    @requires_captcha
    def test_login_success(self, page: Page):
        """正确凭据 + 验证码 → 跳转到 /projects"""
        page.goto(LOGIN_URL, wait_until="networkidle")
        page.locator("#pd-form-username").fill(USERNAME)
        page.locator("#pd-form-password").fill(PASSWORD)
        page.locator("input[name='captcha']").fill(_fill_captcha(page))
        page.locator(".btn-login").click()
        page.wait_for_timeout(4000)

        assert "/projects" in page.url or page.url.rstrip("/") == "https://test.panqu.com", \
            f"登录失败: {page.url}"

    @requires_captcha
    def test_wrong_password(self, page: Page):
        """错误密码 → 登录失败"""
        page.goto(LOGIN_URL, wait_until="networkidle")
        page.locator("#pd-form-username").fill(USERNAME)
        page.locator("#pd-form-password").fill("wrongpassword")
        page.locator("input[name='captcha']").fill(_fill_captcha(page))
        page.locator(".btn-login").click()
        page.wait_for_timeout(2000)

        assert "/login" in page.url

    @requires_captcha
    def test_wrong_username(self, page: Page):
        """不存在用户 → 登录失败"""
        page.goto(LOGIN_URL, wait_until="networkidle")
        page.locator("#pd-form-username").fill("no_such_user_999")
        page.locator("#pd-form-password").fill(PASSWORD)
        page.locator("input[name='captcha']").fill(_fill_captcha(page))
        page.locator(".btn-login").click()
        page.wait_for_timeout(2000)

        assert "/login" in page.url

    def test_empty_captcha(self, page: Page):
        """空验证码 → 提示'验证码不能为空'"""
        page.goto(LOGIN_URL, wait_until="networkidle")
        page.locator("#pd-form-username").fill(USERNAME)
        page.locator("#pd-form-password").fill(PASSWORD)
        page.locator(".btn-login").click()
        page.wait_for_timeout(2000)

        assert "验证码不能为空" in page.locator("body").inner_text()

    @requires_captcha
    def test_empty_username(self, page: Page):
        """空用户名 → 停留在登录页"""
        page.goto(LOGIN_URL, wait_until="networkidle")
        page.locator("#pd-form-password").fill(PASSWORD)
        page.locator("input[name='captcha']").fill(_fill_captcha(page))
        page.locator(".btn-login").click()
        page.wait_for_timeout(2000)

        assert "/login" in page.url

    def test_keep_login_checkbox(self, page: Page):
        """保持会话复选框可勾选"""
        page.goto(LOGIN_URL, wait_until="networkidle")
        cb = page.locator("#keeplogin")
        expect(cb).to_be_visible()
        assert not cb.is_checked()
        cb.check()
        assert cb.is_checked()

    def test_page_elements(self, page: Page):
        """登录页 UI 元素完整性"""
        page.goto(LOGIN_URL, wait_until="networkidle")

        expect(page.locator(".logo-img")).to_be_visible()
        expect(page.locator("#pd-form-username")).to_have_attribute("placeholder", "用户名")
        expect(page.locator("#pd-form-password")).to_have_attribute("placeholder", "密码")
        expect(page.locator("input[name='captcha']")).to_be_visible()
        expect(page.locator(".captcha-img")).to_be_visible()
        expect(page.locator(".btn-login")).to_have_text("登 录")
        expect(page.locator("span[onclick*='register']").first).to_be_visible()


# ── 登录后功能测试 ──────────────────────────────────────

class TestAfterLogin:
    """登录后页面功能（依赖 config/auth.json）"""

    def test_direct_access(self, logged_in_page: Page):
        """直接访问 /projects，无需重新登录"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        assert "/login" not in logged_in_page.url

    def test_page_title(self, logged_in_page: Page):
        """页面标题非空"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        assert len(logged_in_page.title()) > 0

    def test_screenshot(self, logged_in_page: Page):
        """截图保存"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        logged_in_page.screenshot(path="screenshots/projects.png", full_page=True)
        assert "/login" not in logged_in_page.url
