import os
from pathlib import Path
from dotenv import load_dotenv


# 找到项目根目录的 .env 文件并加载
# __file__ 是 config.py 的路径，往上两级到项目根目录
_project_root = Path(__file__).resolve().parent.parent.parent
_env_path = _project_root / '.env'

# 关键：加载 .env 文件到环境变量
load_dotenv(dotenv_path=_env_path,override=False)

# 现在 os.getenv() 就能读到 .env 里的值了
def get_run_mode() ->  str:
    """
    获取运行模式,默认mock
    """
    return os.getenv('RUN_MODE', 'mock')  # 默认值为 'mock'

def get_llm_provider() -> str:
    """
    获取 LLM 提供商
    """
    return os.getenv('LLM_PROVIDER', 'mock')  # 默认值为 'mock'
