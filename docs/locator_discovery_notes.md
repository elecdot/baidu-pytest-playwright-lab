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

## Route Entry Manual Observation

Tool:

- `uv run playwright codegen https://map.baidu.com`

Environment:

- Browser: Chrome for Testing
- Mode: headed
- URL: `https://map.baidu.com`

Manual steps:

1. 打开百度地图首页。
2. 点击左侧搜索框旁边的路线入口按钮。
3. 页面左侧出现路线规划面板。
4. 面板顶部出现公交、驾车、步行、骑行等交通方式入口。
5. 出现起点输入框。
6. 出现终点输入框。

Observed locators:

- Route entry:
  - `page.locator(".searchbox-content-button")`

- Start input:
  - `page.get_by_role("textbox", name="输入起点或在图区上选点")`

- End input, initial state:
  - `page.get_by_role("textbox", name="输入终点")`

- End input, focused/expanded state:
  - `page.get_by_role("textbox", name="输入终点或在图区上选点")`

Stable assertions:

- 路线面板出现后可以断言以下元素之一：
  - `page.get_by_role("textbox", name="输入起点或在图区上选点")`
  - `page.get_by_role("textbox", name="输入终点")`
  - 页面文本包含 `公交`
  - 页面文本包含 `驾车`
  - 页面文本包含 `步行`
  - 页面文本包含 `骑行`

Decision:

- Stage 3A 先实现 Route Panel Smoke。
- 该测试只验证路线入口可点击、路线面板可打开、起点/终点输入框可见。
- 暂不在 Stage 3A 中输入起点和终点。
codegen:
```python
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://map.baidu.com/@11590057.96,4489812.75,4z")
    page.locator(".searchbox-content-button").click()
    page.get_by_role("textbox", name="输入起点或在图区上选点").click()
    page.get_by_role("textbox", name="输入终点").click()
    page.get_by_role("textbox", name="输入起点或在图区上选点").click()
    page.get_by_role("textbox", name="输入起点或在图区上选点").fill("")
    page.get_by_role("textbox", name="输入起点或在图区上选点").click()
    page.get_by_role("textbox", name="输入起点或在图区上选点").fill("北京大学")
    page.get_by_role("textbox", name="输入起点或在图区上选点").press("Enter")
    page.get_by_role("textbox", name="输入终点或在图区上选点").fill("北京大学xi")
    page.get_by_text("北京大学-西门 北京市海淀区").click()
    #出现对应信息

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
```
## Route Planning Baseline Manual Observation

Tool:

- `uv run playwright codegen https://map.baidu.com`

Route case:

- Mode: 驾车
- Start: 北京南站
- End: 天安门广场

Manual steps:

1. 打开百度地图首页。
2. 点击路线入口。
3. 点击“驾车”模式。
4. 在起点输入框输入“北京南站”。
5. 点击候选项“北京南站 北京市丰台区”。
6. 在终点输入框输入“天安门广场”。
7. 点击候选项“天安门广场 北京市东城区”。
8. 点击终点候选项后，页面自动生成路线方案，不需要额外点击搜索按钮或按 Enter。
9. 页面左侧出现推荐路线、方案2、方案3等路线方案。
10. 点击具体方案后，出现路线细节步骤，例如“进入南站北环路，行驶240米”。

Observed locators:

- Route entry:
  - `page.locator(".searchbox-content-button")`

- Drive mode:
  - `page.locator(".tab-item.drive-tab")`

- Start input:
  - `page.get_by_role("textbox", name="输入起点或在图区上选点")`

- Start suggestion:
  - `page.get_by_text("北京南站 北京市丰台区")`

- End input:
  - `page.get_by_role("textbox", name="输入终点或在图区上选点")`

- End suggestion:
  - `page.get_by_text("天安门广场 北京市东城区")`

Route result indicators:

- `page.get_by_text("推荐路线")`
- `page.get_by_text("方案2")`
- `page.get_by_text("方案3")`
- text matching `分钟`
- text matching `公里`
- text matching `红绿灯`

Route detail indicators:

- text matching `进入`
- text matching `行驶`

Decision:

- Stage 3B 可以实现完整路线规划 baseline。
- 终点候选项点击后会自动触发路线规划，因此不需要单独提交按钮。
- 正式测试不应断言精确的分钟数、公里数、红绿灯数量。
- 正式测试只验证路线方案区域和路线细节区域出现。
codegen:
```python
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://map.baidu.com/@11590057.96,4489812.75,4z")
    page.locator(".searchbox-content-button").click()
    page.locator(".tab-item.drive-tab").click()
    page.get_by_role("textbox", name="输入起点或在图区上选点").click()
    page.get_by_role("textbox", name="输入起点或在图区上选点").fill("北京南站")
    page.get_by_text("北京南站 北京市丰台区").click()
    page.get_by_role("textbox", name="输入终点或在图区上选点").click()
    page.get_by_role("textbox", name="输入终点或在图区上选点").fill("天安门广场")
    page.get_by_text("天安门广场 北京市东城区").click()
    page.get_by_text("分钟9.2公里27个红绿灯").click()
    page.get_by_text("进入南站北环路，行驶240米").first.click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
```

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
