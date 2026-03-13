# -*- coding: utf-8 -*-
"""
命令执行工具 - 安全的本地命令执行
"""
import subprocess
from typing import Optional, Tuple
from ..config.settings import settings


class CommandTools:
    """安全的命令执行工具"""
    
    def __init__(self):
        self.allowed_commands = settings.ALLOWED_COMMANDS
    
    def execute(self, command: str, timeout: int = 30) -> Tuple[bool, str]:
        """安全执行命令
        
        Args:
            command: 要执行的命令
            timeout: 超时时间（秒）
            
        Returns:
            (成功标志, 输出或错误信息)
        """
        # 解析命令
        parts = command.strip().split()
        if not parts:
            return False, "空命令"
        
        base_cmd = parts[0]
        
        # 验证命令是否在允许列表
        if base_cmd not in self.allowed_commands:
            return False, f"命令 '{base_cmd}' 不在允许列表中: {self.allowed_commands}"
        
        try:
            result = subprocess.run(
                command,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                return True, output if output else "(无输出)"
            else:
                return False, f"命令执行失败: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return False, f"命令执行超时 ({timeout}秒)"
        except Exception as e:
            return False, f"执行错误: {str(e)}"
    
    def list_allowed(self) -> str:
        """列出允许的命令"""
        return "允许的命令: " + ", ".join(self.allowed_commands)


# 创建默认实例
command_tools = CommandTools()
