# -*- coding: utf-8 -*-
"""
DeepSeek Agent 核心实现
"""
from openai import OpenAI
from typing import Optional, List, Dict
from ..config.settings import settings
from ..tools import file_tools, command_tools


class DeepSeekAgent:
    """DeepSeek AI Agent"""
    
    def __init__(self, system_prompt: Optional[str] = None):
        """初始化 Agent
        
        Args:
            system_prompt: 自定义系统提示词
        """
        settings.validate()
        
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )
        self.model = settings.DEEPSEEK_MODEL
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.messages: List[Dict[str, str]] = []
    
    def _default_system_prompt(self) -> str:
        """默认系统提示词"""
        return """你是一个有用的 AI 助手，可以帮助用户完成任务。

你具有以下能力：
1. 与用户进行自然语言对话
2. 帮助用户理解和使用本地文件操作工具
3. 帮助用户理解和使用命令执行工具

可用工具：
- 文件操作：读取、写入、列出目录
- 命令执行：执行预定义的安全命令列表

请根据用户需求提供帮助。"""
    
    def chat(self, user_input: str) -> str:
        """与 Agent 对话
        
        Args:
            user_input: 用户输入
            
        Returns:
            Agent 响应
        """
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        
        # 调用 DeepSeek API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt}
            ] + self.messages,
            temperature=0.7,
            max_tokens=2048
        )
        
        # 提取响应
        assistant_message = response.choices[0].message.content
        
        # 保存对话历史
        self.messages.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def execute_tool(self, tool_name: str, *args, **kwargs) -> str:
        """执行工具
        
        Args:
            tool_name: 工具名称 (file_read, file_write, file_list, cmd_exec)
            
        Returns:
            执行结果
        """
        tools = {
            "file_read": lambda: file_tools.read_file(args[0] if args else ""),
            "file_write": lambda: file_tools.write_file(
                args[0] if len(args) > 0 else "",
                args[1] if len(args) > 1 else ""
            ),
            "file_list": lambda: file_tools.list_dir(args[0] if args else "."),
            "cmd_exec": lambda: str(command_tools.execute(args[0] if args else "")),
            "cmd_allowed": lambda: command_tools.list_allowed()
        }
        
        if tool_name not in tools:
            return f"未知工具: {tool_name}。可用工具: {list(tools.keys())}"
        
        try:
            return tools[tool_name]()
        except Exception as e:
            return f"工具执行错误: {str(e)}"
    
    def clear_history(self):
        """清除对话历史"""
        self.messages = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.messages.copy()
