# Locator Discovery Notes

## Environment

- Browser: Chromium
- Mode: headed
- Tool: Playwright codegen
- URL: https://map.baidu.com
- Keyword: 北京大学

## Search Flow Manual Observation

1. 打开页面后是否有弹窗：
   - 页面会请求“我的地址”相关权限或定位能力。
   - 页面右侧存在广告卡片，但不阻塞搜索框。

2. 搜索框是否直接可见：
   - 是，搜索框直接可见。

3. 搜索框 locator：
   - `page.get_by_role("textbox", name="搜地点、查公交、找路线")`

4. 输入“北京大学”后是否出现联想结果：
   - 是，左侧出现包含“北京大学”的联想候选。

5a. 点击搜索按钮是否能提交：
   - 可以提交，但触发百度安全验证。
5b. 直接按 Enter：
   - 同样可以提交，也触发百度安全验证

6. 搜索按钮 locator：
   - `page.locator("#search-button")`

7. 是否触发安全验证：
   - 是。
   - 出现“百度安全验证”“请完成下方验证后继续操作”。
   - 验证方式包括图像旋转、滑块、扫码验证。
   - 自动化脚本不应尝试绕过该验证。

8. 人工完成验证后是否出现搜索结果：
   - 是。

9. 页面中是否能看到“北京大学”：
   - 能。

10. 搜索结果区域：
   - 左侧搜索结果面板。
   - 候选 locator：`page.locator("#card-1").get_by_role("list")`

11. 结果页 URL：
   - 人工验证后浏览器进入 `https://map.baidu.com/search/%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6/@12931654.56,4855939.47,12z?querytype=s&da_src=shareurl&wd=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6&c=131&src=0&pn=0&sug=0&l=12&b=(12918278.56,4802307.47;13000198.56,4848387.47)&from=webmap&biz_forward=%7B%22scaler%22:1,%22styles%22:%22pl%22%7D&device_ratio=1` 页面。

## Candidate Locators

- Search input:
  - `page.get_by_role("textbox", name="搜地点、查公交、找路线")`

- Search button:
  - `page.locator("#search-button")`

- Security challenge indicator:
  - `page.get_by_text("百度安全验证")`
  - `page.get_by_text("请完成下方验证后继续操作")`

- Result indicator:
  - `page.get_by_text("北京大学").first`
  - `page.locator("#card-1").get_by_text("北京大学").first`

## Decision

- Stage 2 不再强行要求自动完成完整搜索流程。
- 正式测试分为：
  1. 搜索提交结果分类测试：结果页或安全验证均作为可观察结果记录。
  2. 已知搜索结果页渲染测试：直接访问人工验证得到的搜索结果 URL，验证结果页可展示“北京大学”。
- 不自动化滑块、图像旋转、扫码验证等安全验证流程。
- 不断言地图瓦片、实时路况、结果数量或精确坐标。

codegen 附录:
```python
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://map.baidu.com/@12959238.56,4825347.47,12z")
    page.get_by_role("textbox", name="搜地点、查公交、找路线").click()
    page.get_by_role("textbox", name="搜地点、查公交、找路线").fill("")
    page.get_by_role("textbox", name="搜地点、查公交、找路线").press("ControlOrMeta+ ")
    page.get_by_role("textbox", name="搜地点、查公交、找路线").fill("")
    page.get_by_role("textbox", name="搜地点、查公交、找路线").click()
    page.get_by_role("textbox", name="搜地点、查公交、找路线").fill("北京大学")
    page.locator("#search-button").click()
    page.locator(".passMod_slide-btn").click()
    page.get_by_text("扫码验证|").click()
    page.goto("https://map.baidu.com/search/%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6/@12931654.56,4855939.47,12z?querytype=s&da_src=shareurl&wd=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6&c=131&src=0&pn=0&sug=0&l=12&b=(12918278.56,4802307.47;13000198.56,4848387.47)&from=webmap&biz_forward=%7B%22scaler%22:1,%22styles%22:%22pl%22%7D&device_ratio=1")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
```
