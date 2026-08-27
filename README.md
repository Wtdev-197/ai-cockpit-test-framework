# AI Cockpit Test Framework

> 面向智能座舱（AI Cockpit / IVI）系统的**工程化自动化测试框架**
> 基于 pytest · GitHub Actions CI · src-layout · 可复现构建

[![CI](https://github.com/Wtdev-197/ai-cockpit-test-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/Wtdev-197/ai-cockpit-test-framework/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)]()

---
📖 [项目详细介绍](docs/PROJECT_INTRO.md) · [架构设计文档](docs/ARCHITECTURE.md)

---

## 架构概览

```
┌─────────────────────────────────────────────┐
│              Test Runner (pytest)            │
├─────────────────────────────────────────────┤
│  tests/unit/          →  IVI 核心逻辑验证   │
│  tests/integration/   →  多模块协作验证     │
│  conftest.py          →  共享 fixture       │
├─────────────────────────────────────────────┤
│              src/cockpit/                    │
│  ivi_simulator.py    →  被测业务（IVI 模拟）│
├─────────────────────────────────────────────┤
│  GitHub Actions CI  →  push/PR 自动验证     │
└─────────────────────────────────────────────┘
```

---

## 快速开始
# 1. 克隆仓库
git clone https://github.com/Wtdev-197/ai-cockpit-test-framework.git
cd ai-cockpit-test-framework

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\activate

# 3. 可编辑安装（解决模块导入问题的标准做法）
pip install -e .

# 4. 运行全部测试
python -m pytest tests/ -v

# 5. 生成测试结果和覆盖率报告
python -m pytest tests/ `
	--cov=src `
	--cov-report=term-missing `
	--cov-report=html:htmlcov `
	--html=results/pytest-report.html `
	--self-contained-html
# 测试结果：results/pytest-report.html
# 源码覆盖率：htmlcov/index.html
```

---

## 如何运行测试

1. 运行所有测试
python -m pytest tests/ -v

2.运行指定目录
python -m pytest tests/unit/ -v

3.运行指定测试文件
python -m pytest tests/unit/test_ivi_simulator.py -v

4.运行指定测试类 / 方法,运行指定类中的所有测试
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator -v

5.运行指定的单个测试方法
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_initialization -v

6.按标记运行,只运行标记为 slow 的用例
python -m pytest tests/ -v -m "slow"

7.跳过标记为 slow 的用例
python -m pytest tests/ -v -m "not slow"

8.生成完整报告
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html:htmlcov --html=results/pytest-report.html --self-contained-html

报告用途：
- `results/pytest-report.html`：查看测试通过/失败、耗时、错误堆栈和每条用例详情。
- `htmlcov/index.html`：查看模块、文件和源码行覆盖率，点击文件可定位未覆盖行。
- 终端输出：直接查看总体覆盖率和缺失行，不打开浏览器也能快速判断结果。

运行 Robot Framework 测试
# 安装 Robot Framework 及常用库
pip install robotframework
pip install robotframework-requests
pip install robotframework-seleniumlibrary  # 如涉及 UI 自动化
1.运行所有 Robot 用例
robot tests/robot/
2.或指定输出目录（推荐，保持干净）：
robot --outputdir results tests/robot/
3.运行指定的 Robot 测试文件
robot tests/robot/test_ivi_simulator.robot
4.运行指定的测试用例（按名称）
robot --test "IVI Simulator Should Initialize Correctly" tests/robot/
5.按标签运行（推荐，和 pytest marker 一个思路）
# 只跑冒烟测试
robot --include smoke tests/robot/
# 跳过慢用例
robot --exclude slow tests/robot/
# 组合标签
robot --include "smoke AND cockpit" tests/robot/
6.带变量参数运行（Robot 的核心能力）
robot --variable ENV:staging --variable BROWSER:chrome tests/robot/
7.生成 & 查看报告：Robot 运行完会自动生成三个文件：log.html（详细执行日志（最常用）），report.html（汇总报告），output.xml（机器可读结果（可二次处理））
# 用浏览器打开报告
open report.html        # macOS
start report.html       # Windows
8.和 pytest 混合执行（完整验证）
# 先跑 pytest
python -m pytest tests/ -v
# 再跑 robot
robot --outputdir results tests/robot/
# 或合并到一条命令（CI 中用）
python -m pytest tests/ -v && robot --outputdir results tests/robot/
```
---

### ✅ 为什么用 `python -m pytest` 而不是裸 `pytest`？

裸 `pytest` 不会将项目根目录加入 `sys.path`，导致 `from src.xxx import yyy` 失败。
`python -m pytest` 会将当前目录加入 `sys.path`，这是 Python 官方推荐的执行方式。

### ✅ 为什么用 `pip install -e .` 而不是改 `PYTHONPATH`？

| 方案 | 问题 |
|---|---|
| 改 `PYTHONPATH` | 每台机器都要配，CI 也要配，不可复现 |
| 改 `sys.path` | 污染代码，团队协作灾难 |
| `pip install -e .` ✅ | 一次配置，所有环境一致 |

### ✅ 为什么用 `src` 布局？

- 防止测试时意外导入开发中的源码（而不是安装的版本）
- 强制通过安装后的包路径导入，更接近生产环境
- PEP 517/518 推荐结构

---

## CI/CD 流水线

每次 `push` 或 `pull_request` 自动执行：

- ✅ Python 3.10+ 多版本验证
- ✅ 依赖安装与可编辑安装
- ✅ 全量测试执行
- ✅ 覆盖率检查（阈值可配置）
- ✅ 失败即阻断合并

配置文件：`.github/workflows/ci.yml`

---

## 技术栈

| 类别 | 技术 |
|---|---|
| 测试框架 | pytest 7.x |
| 覆盖率 | pytest-cov |
| 包管理 | pip + pyproject.toml |
| CI | GitHub Actions |
| Python | 3.10+ |
| 架构模式 | src-layout · fixture 分层 · marker 分组 |

---

## 项目亮点总结

- 🔧 **不是 Demo**：解决了真实工程中的模块导入问题
- 🏗️ **工程化思维**：可编辑安装 + CI + 覆盖率
- 📐 **架构规范**：src-layout、fixture 分层、marker 分组
- 🔄 **可复现**：任何人 clone 下来 3 步跑通
- 🚀 **可扩展**：新模块只需 `src/` 下建包 + `tests/` 下建文件

---

## License

MIT
