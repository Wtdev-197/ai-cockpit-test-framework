"""AI用例生成管道集成测试"""
import pytest
from pathlib import Path
from src.ai.case_generator import CaseGenerator
from src.ai.rag_pipeline import RAGPipeline


@pytest.mark.ai
def test_requirement_parsing(project_root, sample_requirement):
    """测试需求解析"""
    knowledge_dir = project_root / "data" / "rag_knowledge"
    generator = CaseGenerator(knowledge_dir)

    parsed = generator.parse_requirement(sample_requirement)
    assert parsed["module"] == "multimedia"
    assert len(parsed["test_points"]) > 0


@pytest.mark.ai
def test_case_generation(project_root, sample_requirement, tmp_path):
    """测试用例生成"""
    knowledge_dir = project_root / "data" / "rag_knowledge"
    generator = CaseGenerator(knowledge_dir)

    cases = generator.generate_test_cases(sample_requirement)
    assert len(cases) > 0

    # 保存到临时文件
    output_file = tmp_path / "generated_tests.txt"
    output_file.write_text("\n".join(cases))
    assert output_file.exists()


@pytest.mark.ai
def test_rag_query(project_root):
    """RAG管道检索"""
    knowledge_dir = project_root / "data" / "rag_knowledge"
    persist_dir = project_root / "data" / "processed" / "rag_index"
    pipeline = RAGPipeline(knowledge_dir, persist_dir)

    results = pipeline.query("测试座舱音量调节功能", top_k=2)
    assert len(results) > 0
    assert "source" in results[0]