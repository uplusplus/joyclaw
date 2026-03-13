"""
JoyClaw 主模块入口
"""

__version__ = "0.1.0"
__author__ = "joy.you"
__description__ = "基于 DeepSeek 的 AI Agent 最小功能项目"

from .agent import AIAssistant
from .deepseek import DeepSeekClient, create_deepseek_client
from .tools import FileTool, CommandTool, SystemInfoTool

__all__ = [
    'AIAssistant',
    'DeepSeekClient',
    'create_deepseek_client',
    'FileTool',
    'CommandTool',
    'SystemInfoTool'
]
