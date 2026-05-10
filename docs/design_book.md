# 基于 Python Playwright 的百度地图 Web 自动化测试实验设计书

## 1. 实验题目

**基于 Python Playwright 的百度地图 Web 端自动化测试实验**

被测对象：百度地图 Web 端
被测地址：`https://map.baidu.com`
测试工具：Playwright for Python、pytest、pytest-playwright、uv
测试类型：Web UI 自动化测试、端到端测试、兼容性测试、定位权限测试、异常输入测试、弱性能观察。

---

## 2. 实验背景与意义

百度地图是一个典型的复杂 Web 应用，具有地点搜索、路线规划、地图拖拽、缩放、定位、路线切换、地图图层渲染等功能。与普通表单页面相比，地图类 Web 应用具有更复杂的异步加载、动态 DOM、网络请求密集、地图瓦片渲染和权限交互特征，因此适合用来验证现代 Web 自动化测试工具的能力。

本实验选择 **Python 版 Playwright**，并使用 **uv** 管理 Python 环境。Playwright 官方提供 Python 版本，并推荐通过 Playwright Pytest 插件编写端到端测试。([Playwright][1])

---

## 3. 实验目标

### 3.1 总目标

基于 uv 构建 Python Playwright 自动化测试工程，对百度地图 Web 端进行端到端自动化测试，验证核心用户流程的功能正确性、交互稳定性和异常处理能力。

### 3.2 具体目标

1. 搭建基于 uv 的 Python 自动化测试项目。
2. 使用 pytest-playwright 管理浏览器测试 fixture。
3. 验证百度地图首页是否正常加载。
4. 验证地点搜索功能是否可用。
5. 验证搜索结果详情是否正常展示。
6. 验证路线规划入口和基础路线流程是否可用。
7. 验证地图缩放、拖拽等基础交互。
8. 验证定位权限允许、拒绝、模拟坐标等场景。
9. 验证桌面端和移动端视口下的基本可用性。
10. 生成截图、Trace、HTML 报告等实验结果证据。
11. 分析 Playwright 在复杂地图类 Web 应用测试中的优势和局限。

### 3.3 当前初始化阶段目标

当前项目处于工程初始化阶段，本阶段先完成以下工作：

1. 明确项目 README、目录 README 和设计书之间的职责边界。
2. 固化目录结构、运行命令、测试证据目录和文档维护规则。
3. 将测试计划拆分为后续可逐步实现的 Page Object、测试数据和 pytest 用例。
4. 暂不把半稳定 locator 作为最终实现提交；实际测试代码应在 codegen 探索后再落地。

---

## 4. 被测软件介绍

### 4.1 被测软件名称

百度地图 Web 端。

### 4.2 被测软件地址

```text
https://map.baidu.com
```

### 4.3 被测软件类型

Web 地图服务、位置服务、出行路线服务。

### 4.4 核心功能

本实验主要关注以下功能模块：

| 模块     | 功能说明                  |
| ------ | --------------------- |
| 首页加载   | 打开地图首页，加载搜索框、地图区域、控件  |
| 地点搜索   | 输入地点关键词并查看搜索结果        |
| 搜索结果详情 | 查看地点名称、地址、按钮、详情面板     |
| 路线规划   | 输入起点和终点，查看驾车、公交、步行等方案 |
| 地图交互   | 缩放、拖拽、点击地图标记          |
| 定位功能   | 允许定位、拒绝定位、模拟地理位置      |
| 响应式页面  | 桌面端和移动端视口适配           |
| 异常输入   | 空输入、特殊字符、无效地点         |

---

## 5. 实验范围

### 5.1 测试范围

本实验覆盖：

1. 百度地图首页可用性测试。
2. 地点搜索流程测试。
3. 搜索结果展示测试。
4. 路线规划基础流程测试。
5. 地图基本交互测试。
6. 定位权限测试。
7. 移动端视口测试。
8. 异常输入测试。
9. 截图、Trace、HTML 报告生成。
10. 自动化测试结果分析。

### 5.2 不测试范围

本实验不覆盖：

1. 不进行高并发压力测试。
2. 不批量采集百度地图数据。
3. 不绕过验证码、登录、权限或反自动化机制。
4. 不测试百度地图移动 App。
5. 不验证地图数据的绝对准确性。
6. 不进行安全漏洞扫描。
7. 不对公开网站进行高频请求或破坏性测试。

---

## 6. pyproject.toml 设计

计划配置示例：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "-v",
    "--browser=chromium",
    "--tracing=retain-on-failure",
    "--screenshot=only-on-failure",
    "--video=retain-on-failure",
    "--html=reports/report.html",
    "--self-contained-html",
]
```

说明：

| 参数                             | 作用             |
| ------------------------------ | -------------- |
| `--browser=chromium`           | 默认使用 Chromium  |
| `--tracing=retain-on-failure`  | 失败时保留 Trace    |
| `--screenshot=only-on-failure` | 失败时截图          |
| `--video=retain-on-failure`    | 失败时保留视频        |
| `--html=reports/report.html`   | 生成 HTML 报告     |

默认配置不启用 `--headed`，这样测试可以在无桌面环境和 CI 环境中运行。课堂演示需要显示浏览器窗口时，使用 `just test-headed` 或在 pytest 命令后追加 `--headed`。

Playwright Trace Viewer 可以回放测试过程，查看每一步操作时页面发生了什么，适合调试失败用例。([Playwright][5])

当前仓库已经在 `pyproject.toml` 中声明 `pytest`、`pytest-playwright`、
`pytest-html`、`playwright`、`ruff` 和 `pre-commit` 等开发依赖。后续实现测试
代码时，应同步补齐 pytest 默认配置，避免文档和实际命令出现偏差。

---

## 7. 测试策略设计

### 7.1 总体测试策略

采用以下流程：

```text
环境初始化
→ 手工探索百度地图页面
→ 使用 Playwright codegen 辅助定位元素
→ 编写 Page Object
→ 编写 pytest 测试用例
→ 执行测试
→ 收集截图、Trace、HTML 报告
→ 分析失败原因
→ 输出实验报告和 PPT
```

### 7.2 测试层次

| 层次                 | 测试内容                    |
| ------------------ | ----------------------- |
| Smoke Test         | 首页是否可打开，页面是否基本可用        |
| Functional Test    | 搜索、路线、详情、地图交互           |
| Permission Test    | 定位权限允许/拒绝               |
| Compatibility Test | Chromium、Firefox、WebKit |
| Responsive Test    | 桌面端与移动端视口               |
| Robustness Test    | 空输入、无效输入、特殊字符           |
| Evidence Test      | 截图、Trace、HTML 报告        |

### 7.3 稳定性策略

百度地图页面存在动态 DOM、广告弹窗、App 引导、异步加载等因素，因此测试脚本应遵循：

1. 不强依赖脆弱 CSS 选择器。
2. 优先使用文本、placeholder、role、可见元素。
3. 避免断言过于精确的路线时间。
4. 不断言实时交通状态的具体值。
5. 对核心流程使用较宽松但有效的断言。
6. 对失败用例保存截图和 Trace。
7. 对偶发失败进行复跑，识别 flaky 测试。

---

## 8. 测试数据设计

### 8.1 地点搜索数据

```python
SEARCH_KEYWORDS = [
    "天安门广场",
    "北京大学",
    "清华大学",
    "北京南站",
    "上海虹桥站",
    "咖啡",
    "医院",
    "银行",
]
```

### 8.2 异常输入数据

```python
INVALID_KEYWORDS = [
    "",
    "@@@###",
    "abcdefg不存在地点12345",
]
```

### 8.3 路线规划数据

| 起点    | 终点    | 测试目的  |
| ----- | ----- | ----- |
| 北京南站  | 天安门广场 | 中距离路线 |
| 北京大学  | 清华大学  | 短距离路线 |
| 上海虹桥站 | 东方明珠  | 上海路线  |
| 空输入   | 天安门广场 | 异常输入  |
| 不存在地点 | 北京大学  | 异常路线  |

### 8.4 定位模拟数据

| 城市 |         经度 |        纬度 |
| -- | ---------: | --------: |
| 北京 | 116.397128 | 39.916527 |
| 上海 | 121.475190 | 31.228833 |
| 广州 | 113.324520 | 23.119160 |

---

## 9. 测试用例设计

### 9.1 首页测试用例

| 编号          | 用例名称         | 操作步骤               | 预期结果           | 优先级 |
| ----------- | ------------ | ------------------ | -------------- | --- |
| TC-HOME-001 | 首页正常打开       | 访问百度地图首页           | 页面 body 可见，未崩溃 | P0  |
| TC-HOME-002 | 搜索框可用        | 定位搜索输入框            | 输入框可见或可交互      | P0  |
| TC-HOME-003 | 页面截图留证       | 打开首页后截图            | 生成首页截图         | P1  |
| TC-HOME-004 | Console 错误监听 | 监听页面 console error | 无阻断型错误         | P2  |

### 9.2 搜索功能测试用例

| 编号            | 用例名称   | 输入       | 预期结果           | 优先级 |
| ------------- | ------ | -------- | -------------- | --- |
| TC-SEARCH-001 | 搜索明确地点 | 天安门广场    | 页面出现相关文本或结果    | P0  |
| TC-SEARCH-002 | 搜索高校   | 北京大学     | 页面出现北京大学相关结果   | P0  |
| TC-SEARCH-003 | 搜索交通枢纽 | 北京南站     | 出现相关结果         | P1  |
| TC-SEARCH-004 | 搜索泛关键词 | 咖啡       | 出现 POI 结果或地图标记 | P1  |
| TC-SEARCH-005 | 空输入搜索  | 空字符串     | 页面不崩溃，有提示或无动作  | P1  |
| TC-SEARCH-006 | 无效地点搜索 | 不存在地点字符串 | 页面不崩溃，有无结果提示   | P1  |
| TC-SEARCH-007 | 特殊字符搜索 | `@@@###` | 页面不崩溃          | P2  |

### 9.3 路线规划测试用例

| 编号           | 用例名称  | 起点   | 终点    | 预期结果         | 优先级 |
| ------------ | ----- | ---- | ----- | ------------ | --- |
| TC-ROUTE-001 | 驾车路线  | 北京南站 | 天安门广场 | 出现路线方案       | P0  |
| TC-ROUTE-002 | 公交路线  | 北京南站 | 天安门广场 | 出现公交方案       | P0  |
| TC-ROUTE-003 | 步行路线  | 北京大学 | 清华大学  | 出现步行方案       | P1  |
| TC-ROUTE-004 | 起终点交换 | 北京大学 | 清华大学  | 起终点互换后路线更新   | P1  |
| TC-ROUTE-005 | 空起点   | 空    | 天安门广场 | 页面提示或不执行路线   | P1  |
| TC-ROUTE-006 | 无效终点  | 北京大学 | 不存在地点 | 页面提示无结果或无法规划 | P2  |

### 9.4 地图交互测试用例

| 编号         | 用例名称  | 操作             | 预期结果   | 优先级 |
| ---------- | ----- | -------------- | ------ | --- |
| TC-MAP-001 | 地图放大  | 点击放大按钮或滚轮      | 地图画面变化 | P1  |
| TC-MAP-002 | 地图缩小  | 点击缩小按钮         | 地图画面变化 | P1  |
| TC-MAP-003 | 地图拖拽  | 拖拽地图区域         | 地图中心变化 | P1  |
| TC-MAP-004 | 点击标记点 | 搜索地点后点击 marker | 出现详情浮层 | P2  |
| TC-MAP-005 | 切换图层  | 点击图层按钮         | 地图样式变化 | P2  |

### 9.5 定位权限测试用例

| 编号         | 用例名称   | 配置                | 预期结果      | 优先级 |
| ---------- | ------ | ----------------- | --------- | --- |
| TC-GEO-001 | 允许定位   | 授予 geolocation 权限 | 页面可处理当前位置 | P1  |
| TC-GEO-002 | 拒绝定位   | 不授予权限             | 页面不崩溃，有提示 | P1  |
| TC-GEO-003 | 模拟北京坐标 | 设置北京经纬度           | 页面定位到北京附近 | P1  |
| TC-GEO-004 | 模拟上海坐标 | 设置上海经纬度           | 页面定位到上海附近 | P2  |

### 9.6 移动端测试用例

| 编号            | 用例名称  | 配置                    | 预期结果    | 优先级 |
| ------------- | ----- | --------------------- | ------- | --- |
| TC-MOBILE-001 | 移动端首页 | Pixel 5 视口            | 页面可打开   | P1  |
| TC-MOBILE-002 | 移动端搜索 | Pixel 5 视口            | 搜索功能可完成 | P1  |
| TC-MOBILE-003 | 移动端定位 | Pixel 5 + geolocation | 定位流程可处理 | P2  |

---

## 10. Page Object Model 设计

### 10.1 设计原则

使用 Page Object Model 的目的：

1. 将页面操作封装起来。
2. 测试用例只表达“业务流程”。
3. 页面元素变化时，只修改 `pages/baidu_map_page.py`。
4. 提高报告展示中的工程性。

### 10.2 `pages/baidu_map_page.py`

```python
from pathlib import Path
from playwright.sync_api import Page, expect


class BaiduMapPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://map.baidu.com"

    def goto(self) -> None:
        self.page.goto(self.url, wait_until="domcontentloaded")

    def expect_page_loaded(self) -> None:
        expect(self.page.locator("body")).to_be_visible()

    def search(self, keyword: str) -> None:
        # 百度地图 DOM 可能变化，因此这里作为初始定位策略。
        # 实际实验时应使用 codegen 生成更准确的 locator。
        search_input = self.page.locator("input").first
        expect(search_input).to_be_visible(timeout=15_000)
        search_input.fill(keyword)
        search_input.press("Enter")

    def expect_text_visible(self, text: str, timeout: int = 15_000) -> None:
        expect(self.page.get_by_text(text).first).to_be_visible(timeout=timeout)

    def screenshot(self, name: str) -> None:
        Path("test-results").mkdir(exist_ok=True)
        self.page.screenshot(
            path=f"test-results/{name}.png",
            full_page=True,
        )
```

---

## 11. 测试数据文件设计

### `data/test_data.py`

```python
SEARCH_KEYWORDS = [
    "天安门广场",
    "北京大学",
    "清华大学",
    "北京南站",
    "咖啡",
]

INVALID_KEYWORDS = [
    "",
    "@@@###",
    "abcdefg不存在地点12345",
]

ROUTE_CASES = [
    {
        "name": "beijing_south_to_tiananmen",
        "start": "北京南站",
        "end": "天安门广场",
    },
    {
        "name": "pku_to_tsinghua",
        "start": "北京大学",
        "end": "清华大学",
    },
]

GEO_LOCATIONS = {
    "beijing": {
        "longitude": 116.397128,
        "latitude": 39.916527,
    },
    "shanghai": {
        "longitude": 121.475190,
        "latitude": 31.228833,
    },
}
```

---

## 12. 测试脚本设计

### 12.1 首页测试：`tests/test_home.py`

```python
from playwright.sync_api import Page
from pages.baidu_map_page import BaiduMapPage


def test_homepage_can_be_opened(page: Page):
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()
    baidu_map.expect_page_loaded()
    baidu_map.screenshot("homepage")
```

### 12.2 搜索测试：`tests/test_search.py`

```python
import pytest
from playwright.sync_api import Page, expect
from pages.baidu_map_page import BaiduMapPage
from data.test_data import SEARCH_KEYWORDS, INVALID_KEYWORDS


@pytest.mark.parametrize("keyword", SEARCH_KEYWORDS)
def test_search_valid_keywords(page: Page, keyword: str):
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()
    baidu_map.search(keyword)

    expect(page.locator("body")).to_contain_text(keyword, timeout=20_000)
    baidu_map.screenshot(f"search-{keyword}")


@pytest.mark.parametrize("keyword", INVALID_KEYWORDS)
def test_search_invalid_keywords_should_not_crash(page: Page, keyword: str):
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()

    if keyword:
        baidu_map.search(keyword)
    else:
        # 空输入不一定触发搜索，这里只验证页面稳定性。
        page.locator("input").first.press("Enter")

    expect(page.locator("body")).to_be_visible()
    baidu_map.screenshot("search-invalid")
```

### 12.3 路线测试：`tests/test_route.py`

路线规划控件的 locator 需要通过 codegen 修正，因此实验设计中先写成“半稳定模板”。

```python
import pytest
from playwright.sync_api import Page, expect
from data.test_data import ROUTE_CASES


@pytest.mark.parametrize("case", ROUTE_CASES)
def test_route_planning_basic_flow(page: Page, case: dict):
    page.goto("https://map.baidu.com", wait_until="domcontentloaded")

    # 下面 locator 需要在实际运行时通过 codegen 修正。
    page.get_by_text("路线").first.click(timeout=15_000)

    inputs = page.locator("input")
    inputs.nth(0).fill(case["start"])
    inputs.nth(1).fill(case["end"])
    inputs.nth(1).press("Enter")

    expect(page.locator("body")).to_contain_text(
        case["end"],
        timeout=20_000,
    )

    page.screenshot(
        path=f"test-results/route-{case['name']}.png",
        full_page=True,
    )
```

### 12.4 定位测试：`tests/test_geolocation.py`

```python
from playwright.sync_api import Browser, expect
from data.test_data import GEO_LOCATIONS


def test_geolocation_beijing(browser: Browser):
    location = GEO_LOCATIONS["beijing"]

    context = browser.new_context(
        geolocation=location,
        permissions=["geolocation"],
        locale="zh-CN",
        timezone_id="Asia/Shanghai",
    )

    page = context.new_page()
    page.goto("https://map.baidu.com", wait_until="domcontentloaded")

    expect(page.locator("body")).to_be_visible()

    page.screenshot(
        path="test-results/geolocation-beijing.png",
        full_page=True,
    )

    context.close()
```

### 12.5 移动端测试：`tests/test_mobile.py`

```python
from playwright.sync_api import Browser, expect


def test_mobile_viewport_homepage(browser: Browser):
    context = browser.new_context(
        viewport={"width": 393, "height": 852},
        is_mobile=True,
        has_touch=True,
        locale="zh-CN",
    )

    page = context.new_page()
    page.goto("https://map.baidu.com", wait_until="domcontentloaded")

    expect(page.locator("body")).to_be_visible()

    page.screenshot(
        path="test-results/mobile-homepage.png",
        full_page=True,
    )

    context.close()
```

---

## 13. Codegen 使用设计

百度地图页面元素比较复杂，建议先用 codegen 找定位器：

```bash
uv run playwright codegen https://map.baidu.com
```

Codegen 的使用流程：

1. 打开百度地图。
2. 手动输入“北京大学”。
3. 点击搜索。
4. 点击路线。
5. 输入起点和终点。
6. 观察生成的 Python 代码。
7. 将可用 locator 整理进 `BaiduMapPage`。

注意：不要直接把 codegen 生成的脚本原封不动作为最终代码。更好的做法是：

```text
Codegen 负责探索页面
Page Object 负责封装页面
pytest 负责组织用例
uv 负责管理环境和运行命令
```

---

## 14. 实验运行方案

### 14.1 运行全部测试

```bash
uv run pytest
```

仓库也提供了 `just` 快捷命令：

```bash
just test
```

在 Codex 等受限 sandbox 中，优先使用 workspace-safe cache 包装命令：

```bash
just agent-test
```

### 14.2 只运行首页测试

```bash
uv run pytest tests/test_home.py
```

### 14.3 只运行搜索测试

```bash
uv run pytest tests/test_search.py
```

### 14.4 使用 Chromium 有头模式运行

```bash
just test-headed
```

或直接使用 pytest 参数：

```bash
uv run pytest --browser chromium --headed
```

Playwright Python 的 pytest 插件支持通过 pytest CLI 指定浏览器和 headed 模式。([Playwright][6])

### 14.5 查看 HTML 报告

WSL/Linux：

```bash
xdg-open reports/report.html
```

Windows PowerShell：

```powershell
start reports/report.html
```

### 14.6 查看 Trace

失败后，Playwright 会在 `test-results/` 中生成 trace 文件。可以使用：

```bash
uv run playwright show-trace test-results/path/to/trace.zip
```

---

## 15. 实验结果记录设计

### 15.1 测试执行汇总表

| 用例编号          | 用例名称   | 浏览器      | 结果   |    耗时 | 证据文件            | 备注          |
| ------------- | ------ | -------- | ---- | ----: | --------------- | ----------- |
| TC-HOME-001   | 首页正常打开 | Chromium | Pass |  3.1s | homepage.png    | 正常          |
| TC-SEARCH-001 | 搜索北京大学 | Chromium | Pass |  6.8s | search.png      | 正常          |
| TC-ROUTE-001  | 路线规划   | Chromium | Fail | 15.2s | trace.zip       | locator 需修正 |
| TC-GEO-001    | 模拟北京定位 | Chromium | Pass |  5.4s | geolocation.png | 正常          |

### 15.2 缺陷记录模板

| 字段   | 内容                          |
| ---- | --------------------------- |
| 缺陷编号 | BUG-001                     |
| 缺陷标题 | Firefox 下路线规划按钮点击后无响应       |
| 所属模块 | 路线规划                        |
| 复现步骤 | 打开百度地图 → 点击路线 → 输入起点终点 → 回车 |
| 实际结果 | 页面未显示路线                     |
| 预期结果 | 页面应显示路线方案                   |
| 浏览器  | Firefox                     |
| 严重程度 | Medium                      |
| 优先级  | P1                          |
| 附件   | screenshot、trace.zip        |
| 分析   | 可能是 locator 不稳定或浏览器兼容差异     |

### 15.3 Flaky 用例记录表

| 用例编号          | 失败次数 | 成功次数 | 是否 flaky | 原因分析        |
| ------------- | ---: | ---: | -------- | ----------- |
| TC-SEARCH-001 |    1 |    2 | 是        | 网络加载慢       |
| TC-ROUTE-001  |    2 |    1 | 是        | 页面动态 DOM 变化 |
| TC-HOME-001   |    0 |    3 | 否        | 稳定          |

---

## 16. 评价指标设计

### 16.1 功能指标

| 指标       | 计算方式           |
| -------- | -------------- |
| 用例通过率    | 通过用例数 / 总用例数   |
| P0 用例通过率 | P0 通过数 / P0 总数 |
| 搜索功能通过率  | 搜索通过数 / 搜索用例总数 |
| 路线功能通过率  | 路线通过数 / 路线用例总数 |

### 16.2 稳定性指标

| 指标        | 说明                |
| --------- | ----------------- |
| 重复执行通过率   | 同一用例连续运行 3 次的通过比例 |
| flaky 用例数 | 结果不稳定的用例数量        |
| 平均执行时间    | 测试套件总耗时 / 用例数     |
| 失败可诊断性    | 是否有截图、Trace、视频    |

### 16.3 用户侧性能观察指标

Playwright 不是 JMeter 的替代品，但可以观察用户侧响应时间：

| 指标       | 说明                 |
| -------- | ------------------ |
| 首页打开时间   | 从 `goto` 到 body 可见 |
| 搜索结果出现时间 | 从输入关键词到结果文本出现      |
| 路线结果出现时间 | 从提交路线到方案出现         |
| 页面错误数    | console error 数量   |
| 失败请求数    | requestfailed 数量   |

示例：

```python
import time
from playwright.sync_api import Page, expect


def test_search_response_time(page: Page):
    page.goto("https://map.baidu.com", wait_until="domcontentloaded")

    start = time.perf_counter()

    search_input = page.locator("input").first
    search_input.fill("北京大学")
    search_input.press("Enter")

    expect(page.locator("body")).to_contain_text("北京大学", timeout=20_000)

    duration = time.perf_counter() - start
    print(f"搜索结果出现时间：{duration:.2f}s")
```

---

## 17. 风险分析与应对策略

| 风险            | 影响         | 应对                             |
| ------------- | ---------- | ------------------------------ |
| 百度地图 DOM 经常变化 | locator 失效 | 使用 codegen 重新定位，封装 Page Object |
| 页面出现弹窗        | 阻塞操作       | 增加弹窗关闭逻辑                       |
| 网络波动          | 用例超时       | 增加合理 timeout，记录网络状态            |
| 路线结果实时变化      | 断言失败       | 不断言具体分钟数，只断言结果存在               |
| 浏览器兼容差异       | 不同浏览器结果不同  | 分浏览器记录结果                       |
| 定位权限受浏览器限制    | 定位用例失败     | 使用 browser context 显式配置权限      |
| 公开网站反自动化      | 页面异常       | 降低频率，不做高并发，不绕过限制               |
| 截图过大          | 报告文件变大     | 只在关键流程和失败时截图                   |

---

## 18. 实验报告结构建议

你的最终报告可以按这个结构写：

1. **概述**
   说明实验背景、选题原因、测试对象、工具选择。

2. **测试工具环境建立**
   重点写 uv、Python、pytest、Playwright、浏览器安装。

3. **测试工具的功能和使用流程**
   介绍 Playwright 的页面操作、locator、自动等待、截图、Trace、浏览器上下文、定位权限模拟。

4. **被测软件介绍**
   介绍百度地图 Web 端的搜索、路线、定位、地图交互。

5. **测试计划与测试用例设计**
   放测试范围、测试数据、测试用例表。

6. **测试工具的应用**
   放项目结构、核心代码、运行命令、截图、HTML 报告、Trace 分析。

7. **总结**
   总结 Playwright + pytest + uv 的优点、不足，以及和 JMeter/Wireshark 的互补关系。

这和老师给的报告内容要求是对齐的。

[1]: https://playwright.dev/python/docs/intro "Installation | Playwright Python"
[2]: https://docs.astral.sh/uv/ "uv"
[3]: https://docs.astral.sh/uv/guides/projects/ "Working on projects | uv"
[4]: https://pypi.org/project/pytest-playwright/ "pytest-playwright"
[5]: https://playwright.dev/python/docs/trace-viewer-intro "Trace viewer | Playwright Python"
[6]: https://playwright.dev/python/docs/test-runners "Pytest Plugin Reference | Playwright Python"
