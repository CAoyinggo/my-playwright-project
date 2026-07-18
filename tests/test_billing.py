"""
盼趣网 — 账单页 (test.panqu.com/billing/personal) 功能测试

依赖 config/auth.json（已登录状态）
"""

from playwright.sync_api import Page, expect

BILLING_URL = "https://test.panqu.com/billing/personal"


class TestBillingPage:
    """账单页基础功能"""

    def test_page_loaded(self, logged_in_page: Page):
        """已登录 → 账单页正常加载"""
        logged_in_page.goto(BILLING_URL, wait_until="networkidle")
        assert "/login" not in logged_in_page.url
        expect(logged_in_page.get_by_text("个人账单")).to_be_visible()

    def test_stats_cards(self, logged_in_page: Page):
        """统计卡片：可用积分、累计消耗、近7天数据"""
        logged_in_page.goto(BILLING_URL, wait_until="networkidle")

        expect(logged_in_page.get_by_text("可用积分")).to_be_visible()
        expect(logged_in_page.get_by_text("累计消耗")).to_be_visible()
        expect(logged_in_page.get_by_text("近7天消耗积分")).to_be_visible()
        expect(logged_in_page.get_by_text("近7天任务总数")).to_be_visible()

    def test_date_filter_selects(self, logged_in_page: Page):
        """日期筛选下拉框存在（页面有多个 combobox 用于各模块筛选）"""
        logged_in_page.goto(BILLING_URL, wait_until="networkidle")

        # 日期筛选通过可见的 select 下拉框实现
        visible_selects = logged_in_page.locator("select:visible")
        count = visible_selects.count()
        assert count > 0, "页面应至少有一个可见的日期筛选下拉框"

        # 检查第一个可见 select 包含日期选项
        first_select = visible_selects.first
        options = first_select.locator("option").all()
        option_texts = [opt.inner_text().strip() for opt in options if opt.inner_text().strip()]
        assert "今日" in option_texts or "近7天" in option_texts, \
            f"下拉选项中缺少日期筛选项: {option_texts}"

    def test_click_date_filter(self, logged_in_page: Page):
        """通过 select 切换日期 → 页面正常"""
        logged_in_page.goto(BILLING_URL, wait_until="networkidle")

        # 操作第一个可见的 select
        select = logged_in_page.locator("select:visible").first
        select.select_option("today")
        logged_in_page.wait_for_timeout(2000)

        assert "/billing/personal" in logged_in_page.url

    def test_consumption_table(self, logged_in_page: Page):
        """消费明细表格可见"""
        logged_in_page.goto(BILLING_URL, wait_until="networkidle")

        expect(logged_in_page.get_by_role("heading", name="消费明细")).to_be_visible()
        expect(logged_in_page.get_by_text("导出").first).to_be_visible()

    def test_model_ranking_top5(self, logged_in_page: Page):
        """模型消耗排名 TOP5 可见"""
        logged_in_page.goto(BILLING_URL, wait_until="networkidle")

        expect(logged_in_page.get_by_text("模型消耗排名TOP5")).to_be_visible()
        expect(logged_in_page.locator("#modelTopViewAllBtn")).to_be_visible()

    def test_project_ranking_top5(self, logged_in_page: Page):
        """项目消耗排名 TOP5 可见"""
        logged_in_page.goto(BILLING_URL, wait_until="networkidle")

        expect(logged_in_page.get_by_text("项目消耗排名TOP5")).to_be_visible()

    def test_consumption_trend_chart(self, logged_in_page: Page):
        """消费趋势图表区域可见"""
        logged_in_page.goto(BILLING_URL, wait_until="networkidle")

        expect(logged_in_page.get_by_text("消费趋势")).to_be_visible()
        expect(logged_in_page.get_by_text("各模型积分消耗趋势图")).to_be_visible()
