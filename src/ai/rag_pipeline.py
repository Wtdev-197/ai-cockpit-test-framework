"""RAG管道 - MVP版本用简单文本匹配，后续接ChromaDB"""
from pathlib import Path
from typing import List, Dict
from src.utils.config import get_run_mode


class RAGPipeline:
    """RAG检索增强生成管道"""

    def __init__(self, knowledge_dir: Path, persist_dir: Path = None):
        self.knowledge_dir = knowledge_dir
        self.persist_dir = persist_dir
        self.documents = []
        self._load_documents()

    def _load_documents(self):
        """加载知识库文档"""
        for md_file in self.knowledge_dir.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            self.documents.append({
                "source": md_file.name,
                "content": content
            })

    def query(self, requirement: str, top_k: int = 3) -> List[Dict]:
        """检索相关知识（Mock模式：返回前top_k个文档）"""
        if get_run_mode() == "mock":
            results = []
            for doc in self.documents[:top_k]:
                results.append({
                    "source": doc["source"],
                    "content": doc["content"][:200] + "...",
                    "score": 0.95
                })
            return results

        # 真实模式：ChromaDB向量检索
        # TODO: 接入 ChromaDB + Embedding
        return []