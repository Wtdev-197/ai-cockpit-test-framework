# 架构设计文档

## 设计原则

1. **测试代码与生产代码分离** — `src/` 与 `tests/` 严格隔离
2. **Fixture 可复用** — `conftest.py` 分层管理
3. **环境可复现** — `pip install -e .` 替代手动路径配置
4. **CI 即文档** — `.github/workflows/ci.yml` 定义了"如何验证项目"
5. **双层验证** — pytest 负责代码级逻辑验证，Robot Framework 负责业务级行为验收，各司其职

---

## 技术决策记录（ADR）

### ADR-001：选择 src-layout 而非 flat-layout

- **决策**：使用 `src/cockpit/` 而非直接 `cockpit/`
- **原因**：避免测试时意外导入未安装的源码，确保测试环境 ≈ 生产环境
- **收益**：测试更真实，包结构更清晰，符合 PEP 517/518 推荐

### ADR-002：使用 `python -m pytest`

- **决策**：始终以 `python -m pytest` 方式运行
- **原因**：保证 `sys.path` 一致性，避免 IDE 与终端行为不一致
- **收益**：本地、CI、Docker 行为完全一致

### ADR-003：可编辑安装

- **决策**：`pip install -e .`
- **原因**：一次配置，本地 / CI / Docker 行为完全一致
- **收益**：彻底解决 `ModuleNotFoundError`，无需改 `PYTHONPATH` 或 `sys.path`

### ADR-004：引入 Robot Framework 做业务级验收测试

- **决策**：在 pytest（代码级）之外，新增 Robot Framework 承担业务级 / 验收级测试（`tests/robot/`）
- **原因**：
  - pytest 擅长代码级逻辑验证、跑得快、能出 Python 覆盖率，但不擅长向非技术人员展示业务行为
  - Robot 用例以自然语言关键字驱动，可读性强，产品/测试同事也能评审用例
  - Robot 原生支持标签（`smoke` / `cockpit` / `slow`），可按标签灵活筛选用例，与 pytest marker 思路一致
  - Robot 通过 `importlib.import_module('src.cockpit.ivi_simulator')` 动态导入被测包，配合 `pip install -e .` 稳定导入 `src` 模块
- **收益**：
  - 形成 **pytest（快/细） + Robot（慢/全业务）** 双层验证体系，CI 中串联执行
  - 任一测试层失败即阻断合并，兼顾"代码质量"与"业务正确性"
  - 为后续接入 `robotframework-requests`（接口）、`robotframework-seleniumlibrary`（UI）预留扩展点
- **取舍**：Robot 测试的是运行时行为，Python 代码覆盖率仍由 pytest 层单独统计，不与 Robot 混用

---

## 分层结构

```
┌─────────────────────────────────────────────────────┐
│                   Test Runners                       │
├──────────────────────────────┬──────────────────────┤
│  pytest（代码级）            │  Robot Framework     │
│  tests/unit/         → 逻辑 │  tests/robot/        │
│  tests/integration/  → 协作 │   → 业务行为验收     │
│  conftest.py         → 夹具 │   → 标签化/可读性强  │
├──────────────────────────────┴──────────────────────┤
│                   src/cockpit/                       │
│           ivi_simulator.py  →  被测业务（IVI 模拟） │
├──────────────────────────────────────────────────────┤
│         GitHub Actions CI  →  push/PR 自动验证       │
└──────────────────────────────────────────────────────┘
```

---

## Fixture 分层策略（pytest 层）

| 层级 | 位置 | 作用域 |
|---|---|---|
| 全局共享 | `tests/conftest.py` | 跨目录复用（如 IVISimulator 实例） |
| 模块级 | `tests/unit/conftest.py` | 仅 unit 目录可见 |
| 函数级 | 测试文件内部 | 单文件内复用 |

> 原则：能放高层级就放高层级，避免过度耦合；敏感资源使用 `autouse=False` 按需启用。

---

## Robot 层组织策略

| 层级 | 位置 | 说明 |
|---|---|---|
| 测试用例 | `tests/robot/test_*.robot` | 业务场景，按被测模块拆分 |
| 公共关键字 | `tests/robot/keywords/ivi_keywords.robot` | 自定义关键字库，封装业务操作 |
| 公共资源 | `tests/robot/resources/common.robot`、`variables.robot` | 跨套件复用的关键字与变量 |
| 标签 | 用例级 `Tags`（如 `smoke` / `cockpit` / `slow`） | 按标签筛选执行，对应 pytest marker |
