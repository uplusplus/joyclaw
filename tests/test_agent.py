# -*- coding: utf-8 -*-
"""
测试 Agent 模块
"""
import pytest
import os


class TestDeepSeekAgent:
    """DeepSeek Agent 测试"""
    
    def test_init_with_api_key(self):
        """测试有 API Key 时初始化成功"""
        # 确保 API Key 已设置
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            pytest.skip("DEEPSEEK_API_KEY 未设置，跳过此测试")
        
        import sys
        sys.path.insert(0, ".")
        from src.agent import DeepSeekAgent
        
        agent = DeepSeekAgent()
        assert agent.client is not None
        assert agent.model is not None
    
    def test_deepseek_chat(self):
        """测试 DeepSeek 对话功能"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            pytest.skip("DEEPSEEK_API_KEY 未设置，跳过此测试")
        
        import sys
        sys.path.insert(0, ".")
        from src.agent import DeepSeekAgent
        
        agent = DeepSeekAgent()
        
        # 测试简单对话
        response = agent.chat("你好，请用一句话回复")
        assert response is not None
        assert len(response) > 0
        print(f"\n✅ DeepSeek 响应: {response[:100]}...")
    
    def test_tool_execution(self):
        """测试工具执行"""
        import sys
        sys.path.insert(0, ".")
        from src.tools import file_tools
        
        # 这个测试不依赖 API
        with pytest.raises(ValueError):
            file_tools.read_file("nonexistent_xyz_file.txt")
    
    def test_clear_and_get_history(self):
        """测试历史管理"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            pytest.skip("DEEPSEEK_API_KEY 未设置，跳过此测试")
        
        import sys
        sys.path.insert(0, ".")
        from src.agent import DeepSeekAgent
        
        agent = DeepSeekAgent()
        
        # 发送一条消息
        agent.chat("测试消息")
        assert len(agent.get_history()) == 2  # user + assistant
        
        # 清除历史
        agent.clear_history()
        assert len(agent.get_history()) == 0
