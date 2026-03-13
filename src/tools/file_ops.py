# -*- coding: utf-8 -*-
"""
文件操作工具 - 安全的文件读写能力
"""
import os
from pathlib import Path
from typing import Optional
from ..config.settings import settings


class FileTools:
    """安全的文件操作工具"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir).resolve()
    
    def read_file(self, file_path: str) -> str:
        """安全读取文件内容
        
        Args:
            file_path: 相对或绝对文件路径
            
        Returns:
            文件内容
            
        Raises:
            ValueError: 文件不存在或超过大小限制
        """
        path = self._resolve_path(file_path)
        
        if not path.exists():
            raise ValueError(f"文件不存在: {file_path}")
        
        if not path.is_file():
            raise ValueError(f"不是文件: {file_path}")
        
        size = path.stat().st_size
        if size > settings.MAX_FILE_SIZE:
            raise ValueError(f"文件过大 ({size} bytes), 超过限制 {settings.MAX_FILE_SIZE}")
        
        return path.read_text(encoding="utf-8")
    
    def write_file(self, file_path: str, content: str) -> str:
        """安全写入文件
        
        Args:
            file_path: 文件路径
            content: 要写入的内容
            
        Returns:
            操作结果消息
        """
        path = self._resolve_path(file_path)
        
        # 检查内容大小
        if len(content.encode("utf-8")) > settings.MAX_FILE_SIZE:
            raise ValueError(f"内容过大, 超过限制 {settings.MAX_FILE_SIZE}")
        
        # 确保父目录存在
        path.parent.mkdir(parents=True, exist_ok=True)
        
        path.write_text(content, encoding="utf-8")
        return f"成功写入 {len(content)} 字符到 {file_path}"
    
    def list_dir(self, dir_path: str = ".") -> str:
        """列出目录内容
        
        Args:
            dir_path: 目录路径
            
        Returns:
            目录内容列表
        """
        path = self._resolve_path(dir_path)
        
        if not path.exists():
            raise ValueError(f"目录不存在: {dir_path}")
        
        if not path.is_dir():
            raise ValueError(f"不是目录: {dir_path}")
        
        items = []
        for item in sorted(path.iterdir()):
            prefix = "📁 " if item.is_dir() else "📄 "
            items.append(f"{prefix}{item.name}")
        
        return "\n".join(items) if items else "(空目录)"
    
    def _resolve_path(self, file_path: str) -> Path:
        """解析并验证路径安全性"""
        # 如果是相对路径，基于 base_dir 解析
        path = Path(file_path)
        if not path.is_absolute():
            path = self.base_dir / path
        
        path = path.resolve()
        
        # 防止目录遍历攻击
        if not str(path).startswith(str(self.base_dir)):
            raise ValueError(f"路径超出允许范围: {file_path}")
        
        return path


# 创建默认实例
file_tools = FileTools()
