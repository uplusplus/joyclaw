"""
测试命令工具
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tools import CommandTool


class TestCommandTool:
    """命令工具测试类"""
    
    @pytest.fixture
    def command_tool(self):
        """创建 CommandTool 实例"""
        return CommandTool(timeout=10)
    
    def test_execute_valid_command(self, command_tool):
        """测试执行有效命令"""
        result = command_tool.execute("echo 'Hello'")
        
        assert result['success'] is True
        assert 'Hello' in result['stdout']
        assert result['returncode'] == 0
    
    def test_execute_invalid_command(self, command_tool):
        """测试执行无效命令"""
        with pytest.raises(ValueError):
            command_tool.execute("rm -rf /")
    
    def test_dangerous_command_blocked(self, command_tool):
        """测试危险命令被阻止"""
        dangerous_commands = [
            "rm -rf /",
            "format C:",
            "dd if=/dev/zero",
            "del /s /q *"
        ]
        
        for cmd in dangerous_commands:
            with pytest.raises(ValueError):
                command_tool.execute(cmd)
    
    def test_command_timeout(self):
        """测试命令超时"""
        command_tool = CommandTool(timeout=1)
        
        # 使用 sleep 命令测试超时（在 Linux/Mac 上）
        import platform
        if platform.system() != 'Windows':
            result = command_tool.execute("sleep 10")
            assert result['success'] is False
            assert '超时' in result['stderr'] or 'Timeout' in result['stderr']
    
    def test_get_current_directory(self, command_tool):
        """测试获取当前目录"""
        import platform
        
        if platform.system() == 'Windows':
            result = command_tool.execute("cd")
        else:
            result = command_tool.execute("pwd")
        
        assert result['success'] is True
        assert len(result['stdout'].strip()) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
