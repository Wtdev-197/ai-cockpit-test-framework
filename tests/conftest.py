"""pytest全局fixture配置"""
import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from src.cockpit.ivi_simulator import IVISimulator

# 加载 .env 文件到环境变量
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=_project_root / ".env", override=False)


@pytest.fixture(scope="function")
def ivi_simulator():
    """每个测试函数独立的IVI模拟器（自动注入，无需每个文件重复定义）"""
    sim = IVISimulator()
    yield sim
    sim.reset()


@pytest.fixture(scope="session")
def project_root():
    """项目根目录路径"""
    return _project_root


@pytest.fixture(scope="session")
def sample_requirement(project_root):
    """读取示例需求文档"""
    req_file = project_root / "data" / "raw" / "sample_requirement.txt"
    if req_file.exists():
        return req_file.read_text(encoding="utf-8")
    return "测试座舱音量调节功能"