"""
测试文件工具
"""

import pytest
import tempfile
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tools import FileTool


class TestFileTool:
    """文件工具测试类"""
    
    @pytest.fixture
    def temp_dir(self):
        """创建临时目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def file_tool(self, temp_dir):
        """创建 FileTool 实例"""
        return FileTool(base_dir=temp_dir)
    
    def test_read_nonexistent_file(self, file_tool):
        """测试读取不存在的文件"""
        with pytest.raises(FileNotFoundError):
            file_tool.read_file("nonexistent.txt")
    
    def test_write_and_read_file(self, file_tool):
        """测试写入和读取文件"""
        test_content = "Hello, JoyClaw!"
        file_path = "test.txt"
        
        # 写入文件
        result = file_tool.write_file(file_path, test_content)
        assert result is True
        
        # 读取文件
        content = file_tool.read_file(file_path)
        assert content == test_content
    
    def test_list_files(self, file_tool):
        """测试列出文件"""
        # 创建几个测试文件
        for i in range(3):
            file_tool.write_file(f"test{i}.txt", f"Content {i}")
        
        # 列出所有 txt 文件
        files = file_tool.list_files(pattern="*.txt")
        assert len(files) == 3
        
        # 验证文件列表
        assert "test0.txt" in files
        assert "test1.txt" in files
        assert "test2.txt" in files
    
    def test_path_security(self, file_tool):
        """测试路径安全性"""
        # 尝试访问 base_dir 之外的文件
        with pytest.raises(PermissionError):
            file_tool.read_file("../../etc/passwd")
    
    def test_create_nested_directories(self, file_tool):
        """测试创建嵌套目录"""
        file_path = "dir1/dir2/dir3/file.txt"
        content = "Nested file content"
        
        # 写入文件（应自动创建目录）
        result = file_tool.write_file(file_path, content)
        assert result is True
        
        # 验证文件存在
        full_path = Path(file_tool.base_dir) / file_path
        assert full_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
