# -*- coding: utf-8 -*-
"""
AI Agent 核心模块
实现 AI Agent 的最小架构：解析输入、调用 deepseek、输出结果
"""

import json
import re
from typing import Optional, List, Dict, Any, Callable
from enum import Enum

from ..deepseek import DeepSeekClient
from ..tools import FileTool, CommandTool, SystemInfoTool


class ToolType(Enum):
    """工具类型枚举"""
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    LIST_FILES = "list_files"
    EXECUTE_COMMAND = "execute_command"
    GET_SYSTEM_INFO = "get_system_info"


class Action:
    """动作类，表示要执行的操作"""
    
    def __init__(self, tool_type: ToolType, parameters: Dict[str, Any]):
        self.tool_type = tool_type
        self.parameters = parameters


class AIAssistant:
    """AI Agent 核心类"""
    
    def __init__(
        self,
        deepseek_client: Optional[DeepSeekClient] = None,
        file_tool: Optional[FileTool] = None,
        command_tool: Optional[CommandTool] = None,
        system_tool: Optional[SystemInfoTool] = None
    ):
        """
        初始化 AI Agent
        
        Args:
            deepseek_client: DeepSeek 客户端
            file_tool: 文件工具
            command_tool: 命令工具
            system_tool: 系统信息工具
        """
        self.deepseek = deepseek_client or DeepSeekClient()
        self.file_tool = file_tool or FileTool()
        self.command_tool = command_tool or CommandTool()
        self.system_tool = system_tool or SystemInfoTool()
        
        # 系统提示词
        self.system_prompt = self._build_system_prompt()
        
        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return """你是一个基于 DeepSeek 的 AI 助手，可以执行以下操作：

可用工具：
1. read_file(file_path) - 读取文件内容
2. write_file(file_path, content) - 写入文件内容
3. list_files(directory, pattern) - 列出目录中的文件
4. execute_command(command, cwd) - 执行系统命令
5. get_system_info() - 获取系统信息

请按照以下格式输出你的行动：
{
    "action": "工具名称",
    "parameters": {
        "参数名": "参数值"
    },
    "thought": "你的思考过程"
}

如果不需要执行工具，直接回复用户：
{
    "action": "reply",
    "content": "你的回复内容",
    "thought": "你的思考过程"
}

请确保：
1. 所有文件操作都在允许的路径范围内
2. 命令执行是安全的
3. 清晰解释你的每一步操作"""
    
    def chat(self, user_input: str, stream: bool = False) -> str:
        """
        处理用户输入并返回响应
        
        Args:
            user_input: 用户输入
            stream: 是否使用流式响应
            
        Returns:
            AI 助手的响应
        """
        # 添加用户消息到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # 调用 DeepSeek
        response = self.deepseek.chat(
            messages=[
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history[-10:],  # 保留最近 10 条消息
            stream=stream
        )
        
        if stream:
            return self._handle_stream_response(response)
        else:
            return self._handle_response(response)
    
    def _handle_response(self, response: Dict[str, Any]) -> str:
        """处理非流式响应"""
        try:
            # 提取 AI 回复
            ai_message = response['choices'][0]['message']['content']
            
            # 尝试解析为 JSON 动作
            action_data = self._extract_json(ai_message)
            
            if action_data and 'action' in action_data:
                # 执行工具
                result = self._execute_action(action_data)
                
                # 添加助手消息到历史
                self.conversation_history.append({
                    "role": "assistant",
                    "content": ai_message
                })
                
                return f"执行结果：{result}"
            else:
                # 普通回复
                self.conversation_history.append({
                    "role": "assistant",
                    "content": ai_message
                })
                
                return ai_message
                
        except Exception as e:
            return f"处理响应时出错：{e}"
    
    def _handle_stream_response(self, response) -> str:
        """处理流式响应"""
        full_content = ""
        
        for chunk in response:
            if 'choices' in chunk and len(chunk['choices']) > 0:
                delta = chunk['choices'][0].get('delta', {})
                if 'content' in delta:
                    full_content += delta['content']
                    print(delta['content'], end='', flush=True)
        
        print()  # 换行
        
        # 处理完整响应
        action_data = self._extract_json(full_content)
        
        if action_data and 'action' in action_data:
            result = self._execute_action(action_data)
            return f"\n执行结果：{result}"
        
        return full_content
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """
        从文本中提取 JSON 对象
        
        Args:
            text: 可能包含 JSON 的文本
            
        Returns:
            JSON 对象或 None
        """
        # 尝试直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # 尝试提取代码块中的 JSON
        json_pattern = r'```json\s*(\{.*?\})\s*```'
        match = re.search(json_pattern, text, re.DOTALL)
        
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        
        # 尝试提取大括号中的 JSON
        json_pattern = r'\{.*?\}'
        match = re.search(json_pattern, text, re.DOTALL)
        
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        
        return None
    
    def _execute_action(self, action_data: Dict[str, Any]) -> str:
        """
        执行动作
        
        Args:
            action_data: 动作数据
            
        Returns:
            执行结果
        """
        action = action_data.get('action', '').lower()
        parameters = action_data.get('parameters', {})
        thought = action_data.get('thought', '')
        
        print(f"\n思考：{thought}")
        print(f"执行动作：{action}")
        
        if action == 'reply':
            return action_data.get('content', '')
        
        elif action == 'read_file':
            file_path = parameters.get('file_path', '')
            if not file_path:
                return "错误：缺少文件路径参数"
            content = self.file_tool.read_file(file_path)
            return f"文件内容:\n{content}"
        
        elif action == 'write_file':
            file_path = parameters.get('file_path', '')
            content = parameters.get('content', '')
            if not file_path or not content:
                return "错误：缺少必要参数"
            self.file_tool.write_file(file_path, content)
            return f"文件已成功写入：{file_path}"
        
        elif action == 'list_files':
            directory = parameters.get('directory', '.')
            pattern = parameters.get('pattern')
            files = self.file_tool.list_files(directory, pattern)
            return f"文件列表:\n" + "\n".join(files)
        
        elif action == 'execute_command':
            command = parameters.get('command', '')
            cwd = parameters.get('cwd')
            if not command:
                return "错误：缺少命令参数"
            result = self.command_tool.execute(command, cwd)
            if result['success']:
                return f"命令执行成功:\n{result['stdout']}"
            else:
                return f"命令执行失败:\n{result['stderr']}"
        
        elif action == 'get_system_info':
            info = self.system_tool.get_info()
            return "系统信息:\n" + json.dumps(info, indent=2, ensure_ascii=False)
        
        else:
            return f"未知动作：{action}"
    
    def reset(self):
        """重置对话历史"""
        self.conversation_history = []
    
    def set_system_prompt(self, prompt: str):
        """设置系统提示词"""
        self.system_prompt = prompt
