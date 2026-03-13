# -*- coding: utf-8 -*-
"""
本地设备工具模块
提供安全的文件操作和命令执行功能
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, List
import json


class FileTool:
    """文件操作工具"""
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        初始化文件工具
        
        Args:
            base_dir: 基础目录，限制文件操作范围，如未提供则使用当前目录
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
    
    def read_file(self, file_path: str) -> str:
        """
        读取文件内容
        
        Args:
            file_path: 文件路径（相对或绝对路径）
            
        Returns:
            文件内容
        """
        path = self._safe_path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在：{path}")
        
        if not path.is_file():
            raise ValueError(f"不是文件：{path}")
        
        try:
            return path.read_text(encoding='utf-8')
        except Exception as e:
            raise Exception(f"读取文件失败：{e}")
    
    def write_file(self, file_path: str, content: str) -> bool:
        """
        写入文件内容
        
        Args:
            file_path: 文件路径
            content: 要写入的内容
            
        Returns:
            是否成功
        """
        path = self._safe_path(file_path)
        
        # 创建父目录（如果不存在）
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            raise Exception(f"写入文件失败：{e}")
    
    def list_files(self, directory: str = ".", pattern: Optional[str] = None) -> List[str]:
        """
        列出目录中的文件
        
        Args:
            directory: 目录路径
            pattern: 文件匹配模式（如 "*.txt"）
            
        Returns:
            文件列表
        """
        path = self._safe_path(directory)
        
        if not path.exists():
            raise FileNotFoundError(f"目录不存在：{path}")
        
        if not path.is_dir():
            raise ValueError(f"不是目录：{path}")
        
        try:
            if pattern:
                files = [f.name for f in path.glob(pattern) if f.is_file()]
            else:
                files = [f.name for f in path.iterdir() if f.is_file()]
            return files
        except Exception as e:
            raise Exception(f"列出文件失败：{e}")
    
    def _safe_path(self, file_path: str) -> Path:
        """
        获取安全的路径（限制在 base_dir 内）
        
        Args:
            file_path: 文件路径
            
        Returns:
            安全的路径对象
        """
        path = Path(file_path)
        
        # 如果是相对路径，转换为绝对路径
        if not path.is_absolute():
            path = self.base_dir / path
        
        # 规范化路径
        path = path.resolve()
        
        # 检查是否在 base_dir 内
        try:
            path.relative_to(self.base_dir.resolve())
        except ValueError:
            raise PermissionError(f"访问被拒绝：路径超出允许范围 ({self.base_dir})")
        
        return path


class CommandTool:
    """命令执行工具"""
    
    # 允许的命令白名单
    ALLOWED_COMMANDS = {
        'ls', 'dir', 'pwd', 'cd', 'cat', 'type', 'echo',
        'date', 'time', 'whoami', 'hostname', 'ipconfig',
        'ping', 'curl', 'wget', 'head', 'tail', 'grep',
        'find', 'locate', 'python', 'python3', 'node',
        'npm', 'pip', 'git', 'docker'
    }
    
    # 禁止的危险参数
    DANGEROUS_ARGS = {
        '-rm', '-rmrf', 'rm -rf', '/d', '/s',
        'format', 'del', 'erase', 'dd', 'mkfs'
    }
    
    def __init__(self, timeout: int = 30):
        """
        初始化命令工具
        
        Args:
            timeout: 命令执行超时时间（秒）
        """
        self.timeout = timeout
    
    def execute(self, command: str, cwd: Optional[str] = None) -> dict:
        """
        安全地执行命令
        
        Args:
            command: 要执行的命令
            cwd: 工作目录
            
        Returns:
            执行结果字典，包含 stdout, stderr, return_code
        """
        # 安全检查
        self._validate_command(command)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=cwd
            )
            
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'success': result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                'stdout': '',
                'stderr': '命令执行超时',
                'return_code': -1,
                'success': False
            }
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'return_code': -1,
                'success': False
            }
    
    def _validate_command(self, command: str) -> None:
        """
        验证命令是否安全
        
        Args:
            command: 要验证的命令
            
        Raises:
            ValueError: 命令不安全时抛出
        """
        # 转换为小写进行检查
        cmd_lower = command.lower().strip()
        
        # 检查是否包含危险参数
        for dangerous in self.DANGEROUS_ARGS:
            if dangerous in cmd_lower:
                raise ValueError(f"禁止使用危险参数：{dangerous}")
        
        # 提取命令名
        parts = cmd_lower.split()
        if not parts:
            raise ValueError("命令不能为空")
        
        cmd_name = parts[0]
        
        # 检查命令是否在白名单中（仅检查第一个命令）
        # 注意：这只是一个基本的安全检查，生产环境需要更严格的验证
        if cmd_name not in self.ALLOWED_COMMANDS:
            # 允许绝对路径的命令
            if not (cmd_name.startswith('/') or cmd_name.startswith('c:\\') or cmd_name.startswith('C:\\')):
                raise ValueError(f"命令不在允许列表中：{cmd_name}")


class SystemInfoTool:
    """系统信息工具"""
    
    def get_info(self) -> dict:
        """
        获取系统信息
        
        Returns:
            系统信息字典
        """
        import platform
        import socket
        
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': socket.gethostname(),
            'user': os.getenv('USER') or os.getenv('USERNAME')
        }
