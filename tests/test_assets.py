"""
盼趣网 — 资产页 (test.panqu.com/aiproperty) 功能测试

依赖 config/auth.json（已登录状态）
"""

from playwright.sync_api import Page, expect

ASSETS_URL = "https://test.panqu.com/aiproperty"


class TestAssetsPage:
    """资产页基础功能"""

    def test_page_loaded(self, logged_in_page: Page):
        """已登录 → 资产页正常加载"""
        logged_in_page.goto(ASSETS_URL, wait_until="networkidle")
        assert "/login" not in logged_in_page.url
        assert "资产" in logged_in_page.title()

    def test_page_has_tabs(self, logged_in_page: Page):
        """资产页包含分类 Tab"""
        logged_in_page.goto(ASSETS_URL, wait_until="networkidle")

        expect(logged_in_page.get_by_text("音色训练")).to_be_visible()
        expect(logged_in_page.get_by_text("虚拟人像")).to_be_visible()
        expect(logged_in_page.get_by_text("真人人像")).to_be_visible()
        expect(logged_in_page.get_by_text("趣艺数人像")).to_be_visible()

    def test_default_tab_virtual_portrait(self, logged_in_page: Page):
        """默认展示「虚拟人像」Tab 内容"""
        logged_in_page.goto(ASSETS_URL, wait_until="networkidle")
        assert "tab=virtualportrait" in logged_in_page.url

    def test_switch_tab_timbre(self, logged_in_page: Page):
        """切换到「音色训练」Tab"""
        logged_in_page.goto(ASSETS_URL, wait_until="networkidle")

        logged_in_page.get_by_text("音色训练").click()
        logged_in_page.wait_for_timeout(2000)

        assert "tab=timbre" in logged_in_page.url or "音色训练" in logged_in_page.title()

    def test_switch_tab_real_portrait(self, logged_in_page: Page):
        """切换到「真人人像」Tab"""
        logged_in_page.goto(ASSETS_URL, wait_until="networkidle")

        logged_in_page.get_by_text("真人人像").click()
        logged_in_page.wait_for_timeout(2000)

        assert "tab=realportrait" in logged_in_page.url or "真人人像" in logged_in_page.title()

    def test_switch_tab_fun_portrait(self, logged_in_page: Page):
        """切换到「趣艺数人像」Tab"""
        logged_in_page.goto(ASSETS_URL, wait_until="networkidle")

        logged_in_page.get_by_text("趣艺数人像").click()
        logged_in_page.wait_for_timeout(2000)

        assert "tab=funportrait" in logged_in_page.url or "趣艺数人像" in logged_in_page.title()
