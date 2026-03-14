# -*- coding: utf-8 -*-
"""
LLM Agent 核心实现 - 支持 OpenAI Function Calling
"""
from openai import OpenAI
from typing import Optional, List, Dict, Any
import json
from ..config.settings import settings
from ..tools import file_tools, command_tools, TOOLS_SCHEMA


class LLMAgent:
    """通用 LLM Agent (支持 OpenAI Function Calling)"""
    
    def __init__(self, system_prompt: Optional[str] = None):
        """初始化 Agent
        
        Args:
            system_prompt: 自定义系统提示词
        """
        settings.validate()
        
        # 使用通用配置
        llm_config = settings.get_llm_config()
        
        self.client = OpenAI(
            api_key=llm_config["api_key"],
            base_url=llm_config["base_url"]
        )
        self.model = llm_config["model"]
        self.provider = llm_config["provider"]
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.messages: List[Dict[str, str]] = []
        self.max_tool_iterations = 5  # 防止工具调用死循环
    
    def _default_system_prompt(self) -> str:
        """默认系统提示词"""
        return f"""你是一个有用的 AI 助手，基于 {self.provider} 模型。

你具有以下能力：
1. 与用户进行自然语言对话
2. 通过工具操作本地文件（读取、写入、列出目录）
3. 执行安全的系统命令

当用户请求涉及文件操作或命令执行时，你应该主动使用相应的工具来完成。
例如：
- 用户说"帮我写一个文件" → 使用 write_file 工具
- 用户说"看看当前目录有什么" → 使用 list_dir 工具
- 用户说"读取 xxx 文件" → 使用 read_file 工具

请根据用户需求选择合适的工具执行操作。"""
    
    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """执行工具调用
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            执行结果
        """
        try:
            if tool_name == "read_file":
                return file_tools.read_file(arguments.get("file_path", ""))
            
            elif tool_name == "write_file":
                return file_tools.write_file(
                    arguments.get("file_path", ""),
                    arguments.get("content", "")
                )
            
            elif tool_name == "list_dir":
                return file_tools.list_dir(arguments.get("dir_path", "."))
            
            elif tool_name == "execute_command":
                success, output = command_tools.execute(arguments.get("command", ""))
                return output if success else f"错误: {output}"
            
            else:
                return f"未知工具: {tool_name}"
                
        except Exception as e:
            return f"工具执行错误: {str(e)}"
    
    def chat(self, user_input: str) -> str:
        """与 Agent 对话 (支持 Function Calling)
        
        Args:
            user_input: 用户输入
            
        Returns:
            Agent 响应
        """
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        
        # Function Calling 循环
        iteration = 0
        while iteration < self.max_tool_iterations:
            iteration += 1
            
            # 调用 LLM API (带工具定义)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt}
                ] + self.messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=2048
            )
            
            message = response.choices[0].message
            
            # 检查是否有工具调用
            if message.tool_calls:
                # 保存 assistant 消息 (包含 tool_calls)
                self.messages.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })
                
                # 执行每个工具调用
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    # 执行工具
                    result = self._execute_tool(tool_name, arguments)
                    
                    # 添加工具结果到消息历史
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                
                # 继续循环，让 LLM 处理工具结果
                continue
            
            # 没有工具调用，返回最终响应
            assistant_message = message.content or ""
            self.messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message
        
        # 达到最大迭代次数
        return "抱歉，工具调用次数超过限制，请简化您的请求。"
    
    def clear_history(self):
        """清除对话历史"""
        self.messages = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.messages.copy()
