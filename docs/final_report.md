# 百度地图 Web 自动化测试实验报告

## 1. 实验概述

本实验使用 Python Playwright、pytest、pytest-playwright 和 uv，对百度地图
Web 端进行端到端自动化测试。实验目标不是批量采集地图数据，也不绕过公开站点
的安全验证，而是在公开 Web 地图应用的真实约束下验证自动化测试工具的可用性、
证据留存能力和局限。

被测地址：`https://map.baidu.com`

测试环境：

- Python 3.12
- Chromium
- pytest + pytest-playwright
- pytest-html
- Playwright screenshot、trace、video 机制

## 2. 测试范围

已完成的自动化范围：

- 首页 smoke：验证百度地图首页可以打开。
- 搜索流程：在百度安全验证约束下验证搜索输入、搜索联想状态分类、搜索结果
  状态分类。
- 路线规划：验证路线面板、驾车路线 baseline、路线方案区域、路线细节区域。
- 定位权限：使用浏览器上下文模拟北京 geolocation。
- 移动端：使用移动端 viewport、touch 和 mobile context 打开页面。
- 证据产物：生成 HTML 报告、截图、受控失败 trace。

不覆盖的范围：

- 不绕过滑块、图像旋转、扫码等百度安全验证。
- 不验证地图数据绝对准确性。
- 不断言实时路线分钟数、公里数、红绿灯数量、价格、路况或路线几何。
- 不进行高频请求、批量采集、压力测试或安全扫描。

## 3. 执行结果

稳定套件当前包含 8 个测试：

| 模块 | 用例数 | 结果 |
| --- | ---: | --- |
| 首页 smoke | 1 | 通过 |
| 搜索流程 | 3 | 通过 |
| 路线规划 | 2 | 通过 |
| 定位权限 | 1 | 通过 |
| 移动端 | 1 | 通过 |

最新完整执行：

```text
8 passed in 37.68s
```

核心证据路径：

- `reports/report.html`
- `test-results/homepage.png`
- `test-results/search-input-keyword.png`
- `test-results/search-suggestion-input_cleared.png`
- `test-results/search-submission-map_navigation.png`
- `test-results/search-known-result-page-security_challenge.png`
- `test-results/route-panel-open.png`
- `test-results/route-result-beijing_south_to_tiananmen.png`
- `test-results/route-detail-beijing_south_to_tiananmen.png`
- `test-results/geolocation-beijing.png`
- `test-results/mobile-homepage.png`

## 4. 失败证据演示

为展示 Playwright 对失败诊断的支持，实验额外生成了一次受控失败证据。该失败
不属于常规 pytest 套件，不影响稳定套件通过率。

受控失败场景：

- 打开 `https://map.baidu.com`
- 故意等待页面中不存在的文本 `THIS_TEXT_IS_EXPECTED_TO_BE_ABSENT`
- 捕获失败时的截图和 trace

复现命令：

```bash
just agent-failure-demo
```

失败证据路径：

- `test-results/failure-demo/failure-demo-missing-text.png`
- `test-results/failure-demo/failure-demo-trace.zip`
- `test-results/failure-demo/failure-summary.txt`

Trace 查看命令：

```bash
uv run playwright show-trace test-results/failure-demo/failure-demo-trace.zip
```

该演示说明：当 UI 自动化失败时，Playwright 可以通过截图、DOM 快照、动作时间线
和 trace 回放帮助定位失败发生的位置和页面状态。

## 5. 重复执行稳定性记录

在最终稳定性记录前，重复执行曾暴露两个问题：

- 一次 `Page.goto` 出现 `net::ERR_NETWORK_CHANGED`。
- 路线结果断言曾被地图比例尺中的 `公里` 文本误触发，导致后续详情点击不稳定。

处理措施：

- `BaiduMapPage.goto_url()` 增加最多 3 次导航重试。
- 路线结果断言收紧为 `推荐路线`、`方案2`、`方案3`、`红绿灯` 等路线面板内更
  有意义的文本，不再使用地图比例尺也可能出现的泛化 `公里` 文本作为单独依据。

修复后连续运行 3 次稳定套件：

| 轮次 | 结果 | 耗时 |
| --- | --- | ---: |
| 1 | 8 passed | 39.94s |
| 2 | 8 passed | 41.30s |
| 3 | 8 passed | 37.68s |

稳定性结论：

- 修复后重复执行通过率：100%
- 已知主要外部风险：公开站点网络波动、百度安全验证、动态 DOM、地图数据实时变化
- 当前测试通过分类断言和宽松但有效的可见性断言降低 flaky 风险

## 6. 工具能力分析

Playwright 优势：

- 自动等待和 Locator API 适合处理复杂 Web UI。
- Browser Context 可以隔离 geolocation、mobile viewport、permissions 等场景。
- screenshot、trace、video、pytest-html 可以形成完整证据链。
- 与 pytest 参数化、mark 和 fixture 机制结合自然。

Playwright 局限：

- 公开地图站点存在反自动化与安全验证，完整搜索流程不能强行自动化。
- 地图瓦片、路线时长、路况、红绿灯数量等实时信息不适合精确断言。
- Headless 和 headed 行为存在差异，例如搜索联想和路线候选项的出现方式不同。
- 外部网络波动会影响端到端测试稳定性，需要重试和失败证据分析。

## 7. 总结

本实验已经形成可执行的 Web UI 自动化测试工程，并覆盖首页、搜索、路线、定位、
移动端和证据留存。实验没有绕过百度安全验证，而是将安全验证、URL 跳转、输入
被清空等现象作为公开站点自动化测试中的可观察结果进行记录。

最终结论：Python Playwright + pytest 适合复杂 Web 地图应用的端到端流程验证
和证据收集，但测试设计必须尊重公开站点的安全边界，并避免对实时地图数据做过
度精确断言。
