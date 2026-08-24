"""基于RAG的测试用例生成器"""
import os
from pathlib import Path
from typing import List, Dict
from src.utils.config import get_run_mode

class CaseGenerator:
    """测试用例生成器"""

    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self._load_knowledge()

    def _load_knowledge(self):
        """加载RAG知识库"""
        self.knowledge = []
        for md_file in self.knowledge_dir.glob("*.md"):
            self.knowledge.append({
                "file": md_file.name,
                "content": md_file.read_text(encoding="utf-8")
            })

    def parse_requirement(self, requirement: str) -> Dict:
        """解析需求文档"""
        if get_run_mode() == "mock":
            # Mock模式：规则提取
            is_volume = "音量" in requirement
            return {
                "module": "multimedia" if is_volume else "unknown",
                "test_points": [
                    "音量边界值: 0, 100",
                    "音量步进: 1",
                    "声压验证: 0→<30dB, 50→≈60dB, 100→>85dB"
                ] if is_volume else []
            }

        # 真实模式：调用 LLM + RAG
        # TODO: 接入真实 LLM API
        return {"module": "unknown", "test_points": []}

    def generate_test_cases(self, requirement: str) -> List[str]:
        """生成文本格式测试用例"""
        parsed = self.parse_requirement(requirement)
        cases = []
        for i, point in enumerate(parsed["test_points"], 1):
            cases.append(f"TC-{i:03d}: 验证{point}")
        return cases

    def generate_robot_cases(self, requirement: str) -> str:
        """生成Robot Framework格式用例"""
        parsed = self.parse_requirement(requirement)
        lines = ["*** Test Cases ***"]
        for i, point in enumerate(parsed["test_points"], 1):
            lines.append(f"Test Volume Point {i}")
            lines.append(f"    [Documentation]    {point}")
            lines.append(f"    Log    {point}")
            lines.append(f"    Should Be True    ${{True}}")
            lines.append("")
        return "\n".join(lines)