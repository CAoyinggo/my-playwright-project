from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 启动 Chromium 浏览器，headless=False 表示你会看到浏览器弹出来
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(f"当前页面标题是: {page.title()}")
    browser.close()
