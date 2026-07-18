# ═══════════════════════════════════════════
# 盼趣网 Playwright 自动化测试
# ═══════════════════════════════════════════

## 🚀 快速开始

```bash
# 1. 安装依赖
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# 2. 首次使用：保存登录状态（只需一次）
python scripts/save_auth.py

# 3. 运行测试
python -m pytest tests/ -v
```

## 📁 项目结构

```
├── tests/                  # 测试用例
│   ├── conftest.py         #   pytest 全局配置 & fixtures
│   └── test_login.py       #   登录测试（10 个用例）
├── config/                 # 配置文件
│   ├── .env                #   账号密码等凭据
│   └── auth.json           #   已保存的浏览器登录状态
├── scripts/                # 工具脚本
│   └── save_auth.py        #   一次性保存登录状态
├── screenshots/            # 测试截图输出
├── requirements.txt        # Python 依赖
└── .github/workflows/      # CI 自动化
```

## 🧪 测试用例

| 用例 | 说明 |
|------|------|
| `test_login_success` | 正确凭据登录成功 |
| `test_wrong_password` | 错误密码被拒绝 |
| `test_wrong_username` | 不存在用户被拒绝 |
| `test_empty_captcha` | 空验证码拦截 |
| `test_empty_username` | 空用户名拦截 |
| `test_keep_login_checkbox` | 保持会话复选框 |
| `test_page_elements` | 登录页 UI 完整性 |
| `test_direct_access` | 登录后直接访问 |
| `test_page_title` | 页面标题检查 |
| `test_screenshot` | 登录后截图 |

## 🔐 验证码处理

- 无 `CAPTCHA_CODE` 环境变量时，需要验证码的测试自动 **跳过**
- 设置 `CAPTCHA_CODE=xxxx` 跑全部测试
- 或者用 `python scripts/save_auth.py` 保存登录状态后，登录后测试不再需要验证码
