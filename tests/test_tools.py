# -*- coding: utf-8 -*-
"""
测试工具模块
"""
import pytest
import os
import sys
sys.path.insert(0, ".")

from src.tools import file_tools, command_tools


class TestFileTools:
    """文件工具测试"""
    
    def test_write_and_read(self, tmp_path):
        """测试写入和读取"""
        from src.tools.file_ops import FileTools
        tools = FileTools(str(tmp_path))
        
        # 写入
        result = tools.write_file("test.txt", "Hello Test")
        assert "成功" in result
        
        # 读取
        content = tools.read_file("test.txt")
        assert content == "Hello Test"
    
    def test_list_dir(self, tmp_path):
        """测试列出目录"""
        from src.tools.file_ops import FileTools
        tools = FileTools(str(tmp_path))
        
        # 创建文件
        tools.write_file("a.txt", "a")
        tools.write_file("b.txt", "b")
        
        # 列出
        result = tools.list_dir(".")
        assert "a.txt" in result
        assert "b.txt" in result
    
    def test_read_nonexistent(self):
        """测试读取不存在的文件"""
        with pytest.raises(ValueError, match="不存在"):
            file_tools.read_file("nonexistent_file_xyz.txt")


class TestCommandTools:
    """命令工具测试"""
    
    def test_execute_allowed(self):
        """测试允许的命令 - pwd"""
        success, output = command_tools.execute("pwd")
        assert success is True
        assert len(output) > 0
    
    def test_execute_echo(self):
        """测试允许的命令 - echo"""
        # echo 可能在白名单里
        success, output = command_tools.execute("echo hello")
        # 检查结果
        if success:
            assert "hello" in output
        else:
            # 如果 echo 不在白名单，应该返回失败
            assert "不在允许列表" in output or "不允许" in output
    
    def test_execute_not_allowed(self):
        """测试不允许的命令"""
        success, output = command_tools.execute("rm -rf /")
        assert success is False
        assert "不在允许列表" in output or "不允许" in output
    
    def test_list_allowed(self):
        """测试列出允许命令"""
        result = command_tools.list_allowed()
        assert "允许的命令" in result
