# -*- coding: utf-8 -*-
"""
DeepSeek 模型集成模块
提供与 DeepSeek API 的通信接口
"""

from typing import Optional, List, Dict, Any, Generator
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class DeepSeekClient:
    """DeepSeek API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.deepseek.com"):
        """
        初始化 DeepSeek 客户端
        
        Args:
            api_key: DeepSeek API 密钥，如未提供则从环境变量读取
            base_url: API 基础 URL
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url
        
        if not self.api_key:
            raise ValueError("未找到 DeepSeek API Key，请设置 DEEPSEEK_API_KEY 环境变量")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> Dict[str, Any] | Generator[Dict[str, Any], None, None]:
        """
        与 DeepSeek 模型进行对话
        
        Args:
            messages: 消息列表，格式为 [{"role": "user/system/assistant", "content": "..."}]
            model: 模型名称
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成 token 数
            stream: 是否使用流式响应
            
        Returns:
            响应字典或生成器（流式响应时）
        """
        url = f"{self.base_url}/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        if stream:
            return self._stream_chat(url, headers, payload)
        else:
            return self._chat(url, headers, payload)
    
    def _chat(self, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
        """非流式聊天请求"""
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"DeepSeek API 请求失败：{e}")
    
    def _stream_chat(self, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """流式聊天请求"""
        try:
            response = requests.post(url, json=payload, headers=headers, stream=True, timeout=60)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data = line_str[6:]
                        if data == '[DONE]':
                            break
                        yield self._parse_stream_data(data)
        except requests.RequestException as e:
            raise Exception(f"DeepSeek 流式 API 请求失败：{e}")
    
    def _parse_stream_data(self, data: str) -> Dict[str, Any]:
        """解析流式响应数据"""
        import json
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {"error": "Failed to parse stream data"}


def create_deepseek_client() -> DeepSeekClient:
    """
    创建 DeepSeek 客户端实例
    
    Returns:
        DeepSeekClient 实例
    """
    return DeepSeekClient()
