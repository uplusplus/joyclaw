"""
测试系统信息工具
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tools import SystemInfoTool


class TestSystemInfoTool:
    """系统信息工具测试类"""
    
    @pytest.fixture
    def system_tool(self):
        """创建 SystemInfoTool 实例"""
        return SystemInfoTool()
    
    def test_get_system_info(self, system_tool):
        """测试获取系统信息"""
        info = system_tool.get_info()
        
        # 验证返回的是字典
        assert isinstance(info, dict)
        
        # 验证包含必需字段
        required_fields = [
            'system', 'release', 'version', 'machine',
            'processor', 'python_version', 'hostname', 'user'
        ]
        
        for field in required_fields:
            assert field in info, f"缺少字段：{field}"
            assert info[field] is not None, f"字段值为空：{field}"
    
    def test_system_name(self, system_tool):
        """测试系统名称"""
        info = system_tool.get_info()
        
        # 系统名称应该是 Windows、Linux 或 Darwin
        assert info['system'] in ['Windows', 'Linux', 'Darwin']
    
    def test_python_version_format(self, system_tool):
        """测试 Python 版本格式"""
        info = system_tool.get_info()
        
        # Python 版本应该是 X.Y.Z 格式
        version = info['python_version']
        parts = version.split('.')
        assert len(parts) >= 2, "Python 版本格式不正确"
        assert all(part.isdigit() for part in parts[:2]), "Python 版本数字格式不正确"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
