# AI Cockpit Test Framework — 项目详细介绍

> 面向智能座舱（AI Cockpit / IVI）的自动化测试框架
> 基于 `pytest`，支持单元测试、接口测试与持续集成（CI）

---

## 一、项目简介

`ai-cockpit-test-framework` 是一个**工程化、可扩展、可 CI 的自动化测试框架**，用于验证智能座舱系统中 IVI（车载信息娱乐系统）的核心逻辑与接口行为。

本项目重点解决：
- 复杂 Python 项目的 **模块导入问题**（`ModuleNotFoundError: No module named 'src'`）
- 测试用例的 **分层与可维护性**
- 本地与 CI 环境 **一致的测试执行方式**

---

## 二、技术栈

| 类别 | 技术 |
|---|---|
| 测试框架 | pytest |
| 项目结构 | `src` layout（PEP 517/518） |
| 依赖管理 | pip / requirements.txt |
| 测试组织 | 单元测试 / 功能测试 |
| 工程化 | GitHub Actions CI |
| 代码规范 | PEP8 / pytest 命名规范 |

---

## 三、目录结构

```
ai-cockpit-test-framework/
├── src/
│   └── cockpit/
│       ├── __init__.py
│       └── ivi_simulator.py      # 被测业务代码
├── tests/
│   ├── unit/
│   │   └── test_ivi_simulator.py
│   └── conftest.py               # pytest 夹具
├── docs/
│   ├── PROJECT_INTRO.md          # 项目介绍（本文件）
│   └── ARCHITECTURE.md           # 架构设计文档
├── .github/
│   └── workflows/
│       └── ci.yml                # CI 流水线
├── pyproject.toml                # 项目元信息
├── pytest.ini                    # pytest 配置
├── requirements.txt
└── README.md
```

---

## 四、核心设计亮点

### 1️⃣ 解决 `ModuleNotFoundError: No module named 'src'`

**问题背景**：pytest 默认不会自动识别 `src` 目录。

**解决方案（均已验证）**：

```bash
# ✅ 推荐方式 1：模块方式运行
python -m pytest tests/

# ✅ 推荐方式 2：可编辑安装（最规范）
pip install -e .

# ✅ 推荐方式 3：pytest.ini
# [pytest]
# pythonpath = .
```

### 2️⃣ 测试分层设计

| 层级 | 说明 |
|---|---|
| unit | 单模块逻辑验证 |
| integration | 多模块协作 |
| e2e | 端到端流程（预留） |

### 3️⃣ 可 CI / 可复现

- ✅ 本地执行 = CI 执行
- ✅ 不依赖 IDE 配置
- ✅ 不依赖硬编码路径

---

## 五、如何运行测试

### ✅ 安装依赖
```bash
pip install -r requirements.txt
pip install -e .
```

### ✅ 运行所有测试
```bash
python -m pytest tests/ -v
```

### ✅ 运行指定测试
```bash
python -m pytest tests/unit/test_ivi_simulator.py -v
```

### ✅ 运行指定测试类 / 方法
```bash
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator -v
```

### ✅ 生成覆盖率报告
```bash
pytest --cov=src --cov-report=term --cov-report=html
```

---

## 六、CI/CD 说明

每次 `push / PR` 自动执行：

- ✅ 依赖安装
- ✅ 模块路径校验
- ✅ 全量测试执行
- ✅ 测试失败即阻断合并

CI 配置位于：`.github/workflows/ci.yml`

---

##七、Robot Framework 业务级验收测试

### 为什么同时用 pytest + Robot？

| 层 | 框架 | 验证粒度 | 受众 |
|---|---|---|---|
| 单元测试 | pytest | 函数/类级别逻辑 | 开发人员 |
| 集成/验收测试 | Robot Framework | 业务场景/端到端行为 | 开发 + 测试 + 产品 |

**设计决策**：pytest 负责"代码对不对"，Robot 负责"行为对不对"。两层互补，CI 中任一层失败都阻断合并。

### 目录结构
tests/
├── robot/
│ ├── init.robot
│ ├── test_ivi_simulator.robot # IVI 模拟器业务用例
│ ├── resources/
│ │ ├── common.robot # 公共关键字
│ │ └── variables.robot # 环境变量
│ └── keywords/
│ └── ivi_keywords.robot # 自定义关键字库
└── unit/
└── test_ivi_simulator.py # pytest 单元测试
### 运行方式
1.安装
pip install robotframework
2.运行全部 Robot 用例
robot --outputdir results tests/robot/
3.按标签运行（冒烟测试）
robot --include smoke --outputdir results tests/robot/
4.带变量运行
robot --variable ENV:staging --outputdir results tests/robot/
5.查看报告（运行后自动生成）
results/log.html → 详细步骤日志
results/report.html → 汇总报告
### 技术亮点

- ✅ Robot 用例通过 `importlib` 动态导入 `src` 包，不依赖硬编码路径
- ✅ 标签体系（`smoke` / `cockpit` / `slow`）支持灵活筛选
- ✅ CI 中 `if: always()` 保证失败也上传报告产物
- ✅ 非技术人员可读的用例描述，支持产品/测试协作评审

### 与 pytest 的关系

| 维度 | pytest | Robot |
|---|---|---|
| 执行速度 | 快（秒级） | 较慢（分钟级，涉及运行时） |
| 覆盖率统计 | ✅ pytest-cov | ❌ 不适用 |
| 用例可读性 | 需懂 Python | 自然语言风格 |
| 适合场景 | 逻辑验证、回归 | 验收测试、Demo 演示 |

## 八、适用场景

- 智能座舱 / IVI 系统测试
- Python 自动化测试框架教学
- pytest 工程化最佳实践示例
