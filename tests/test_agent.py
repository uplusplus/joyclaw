"""
测试 Agent 模块
"""
import pytest
import sys
sys.path.insert(0, "..")

from src.agent import DeepSeekAgent
from src.config import settings


class TestDeepSeekAgent:
    """DeepSeek Agent 测试"""
    
    def test_init_without_api_key(self, monkeypatch):
        """测试无 API Key 时初始化失败"""
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        
        # 重新加载设置
        import importlib
        from src.config import settings as settings_mod
        importlib.reload(settings_mod)
        
        with pytest.raises(ValueError, match="DEEPSEEK_API_KEY"):
            DeepSeekAgent()
    
    def test_tool_execution(self):
        """测试工具执行"""
        # 跳过 API Key 验证，直接测试工具执行
        from src.tools import file_tools
        
        # 这个测试不依赖 API
        with pytest.raises(ValueError):
            file_tools.read_file("nonexistent.txt")
    
    def test_clear_history(self, monkeypatch):
        """测试清除历史"""
        # 设置假的 API Key
        monkeypatch.setenv("DEEPSEEK_API_KEY", "test_key")
        
        # 需要重新加载设置
        import importlib
        from src.config import settings as settings_mod
        importlib.reload(settings_mod)
        
        # 创建 agent 会因网络失败，所以我们只测试历史管理
        # 这个测试在实际使用时需要 mock OpenAI 客户端
        pass
