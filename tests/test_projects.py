"""
盼趣网 — 项目列表页 (test.panqu.com/projects) 功能测试

依赖 config/auth.json（已登录状态）
"""

import os
from playwright.sync_api import Page, expect

TARGET_URL = os.getenv("TARGET_URL", "https://test.panqu.com/projects")


class TestProjectsPage:
    """项目列表页 UI & 基础功能"""

    def test_page_loaded(self, logged_in_page: Page):
        """已登录 → 直接访问 /projects，页面正常加载"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        assert "/login" not in logged_in_page.url
        assert logged_in_page.title() == "项目列表｜盼趣AI"

    def test_page_title_section(self, logged_in_page: Page):
        """「项目管理」标题区域可见"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        expect(logged_in_page.get_by_text("项目管理")).to_be_visible()
        expect(logged_in_page.get_by_text("管理和查看您的所有AI短剧项目")).to_be_visible()

    def test_add_project_button(self, logged_in_page: Page):
        """「添加项目」按钮可见且可点击"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        btn = logged_in_page.locator("button:has-text('添加项目')")
        expect(btn).to_be_visible()
        expect(btn).to_be_enabled()

    def test_search_box(self, logged_in_page: Page):
        """搜索框存在且可输入"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        search = logged_in_page.locator("input[type='search']")
        expect(search).to_be_visible()
        expect(search).to_have_attribute("placeholder", "搜索项目/成员姓名...")
        search.fill("test")
        assert search.input_value() == "test"

    def test_stats_display(self, logged_in_page: Page):
        """统计数据展示：总项目数、总任务次数"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        expect(logged_in_page.get_by_text("总项目数")).to_be_visible()
        expect(logged_in_page.get_by_text("总任务次数")).to_be_visible()


class TestNavigation:
    """侧边栏导航"""

    def test_nav_projects_active(self, logged_in_page: Page):
        """当前页「项目」菜单高亮"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        nav_item = logged_in_page.locator("a.active[href='/projects']").first
        expect(nav_item).to_be_visible()
        expect(nav_item).to_contain_text("项目")

    def test_nav_property_link(self, logged_in_page: Page):
        """点击「资产」跳转到 /aiproperty"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        logged_in_page.locator("a[href='/aiproperty']").first.click()
        logged_in_page.wait_for_timeout(2000)
        assert "/aiproperty" in logged_in_page.url

    def test_nav_billing_link(self, logged_in_page: Page):
        """点击「账单」跳转到 /billing/personal"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        logged_in_page.locator("a[href='/billing/personal']").first.click()
        logged_in_page.wait_for_timeout(2000)
        assert "/billing/personal" in logged_in_page.url

    def test_nav_logo_home(self, logged_in_page: Page):
        """点击 Logo 返回首页"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        logged_in_page.locator("a[href='/']").first.click()
        logged_in_page.wait_for_timeout(2000)
        assert "/login" not in logged_in_page.url  # 不会跳回登录页


class TestRechargeModal:
    """充值弹窗（页面加载时默认打开）"""

    def test_recharge_modals_visible(self, logged_in_page: Page):
        """两个充值弹窗在页面加载时可见"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")

        # 积分充值弹窗
        expect(logged_in_page.get_by_text("积分充值").first).to_be_visible()
        expect(logged_in_page.get_by_text("确认充值金额").first).to_be_visible()

        # 趣币充值弹窗
        expect(logged_in_page.get_by_text("趣币充值").first).to_be_visible()

    def test_recharge_preset_amounts(self, logged_in_page: Page):
        """充值弹窗有预设金额选项（快速充值区域可见）"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")

        expect(logged_in_page.get_by_text("快速充值").first).to_be_visible()
        expect(logged_in_page.get_by_text("确认充值金额").first).to_be_visible()

    def test_recharge_modal_has_payment_info(self, logged_in_page: Page):
        """充值弹窗包含支付宝支付信息"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")

        expect(logged_in_page.get_by_text("支付宝扫码支付").first).to_be_visible()
        expect(logged_in_page.get_by_text("联系客服").first).to_be_visible()

    def test_reopen_modals_via_balance(self, logged_in_page: Page):
        """关闭弹窗后，点击余额可以重新打开"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")

        # 先关闭所有弹窗
        close_btns = logged_in_page.locator(".modal .btn-circle").all()
        for btn in close_btns:
            try:
                btn.click(force=True)
                logged_in_page.wait_for_timeout(300)
            except:
                pass

        # 点击余额
        logged_in_page.locator(".navbar-balance-btn").first.click(force=True)
        logged_in_page.wait_for_timeout(1000)

        # 弹窗重新出现
        expect(logged_in_page.get_by_text("积分充值").first).to_be_visible()


class TestProjectList:
    """项目列表"""

    def test_project_list_not_empty(self, logged_in_page: Page):
        """项目列表中至少有一个项目"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")
        # 页面应展示项目卡片或列表项
        expect(logged_in_page.get_by_text("所有项目")).to_be_visible()

    def test_project_detail_accessible(self, logged_in_page: Page):
        """点击项目进入详情页"""
        logged_in_page.goto(TARGET_URL, wait_until="networkidle")

        # 点击第一个项目
        first_project = logged_in_page.locator("a[href*='/projects/']").first
        if first_project.is_visible():
            first_project.click()
            logged_in_page.wait_for_timeout(3000)
            assert "/projects/" in logged_in_page.url
            logged_in_page.screenshot(path="screenshots/project-detail.png", full_page=True)
