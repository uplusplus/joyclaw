# -*- coding: utf-8 -*-
"""
简单的交互式演示脚本
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tools import FileTool, CommandTool, SystemInfoTool


def main():
    """简单的工具演示"""
    print("=" * 60)
    print("  JoyClaw - 本地设备工具演示")
    print("=" * 60)
    
    # 演示文件工具
    print("\n📁 文件工具演示:")
    file_tool = FileTool()
    
    # 创建测试文件
    test_file = "hello_joyclaw.txt"
    test_content = "Hello, JoyClaw!\n这是第一个测试文件。\n"
    
    print(f"\n1. 创建文件：{test_file}")
    file_tool.write_file(test_file, test_content)
    print("   ✓ 文件创建成功")
    
    # 读取文件
    print(f"\n2. 读取文件：{test_file}")
    content = file_tool.read_file(test_file)
    print(f"   内容:\n{content}")
    
    # 列出文件
    print("\n3. 列出 .txt 文件:")
    files = file_tool.list_files(pattern="*.txt")
    for f in files:
        print(f"   - {f}")
    
    # 演示系统信息
    print("\n💻 系统信息:")
    system_tool = SystemInfoTool()
    info = system_tool.get_info()
    
    print(f"   操作系统：{info['system']} {info['release']}")
    print(f"   主机名：{info['hostname']}")
    print(f"   当前用户：{info['user']}")
    print(f"   Python 版本：{info['python_version']}")
    
    # 演示命令工具
    print("\n⚡ 命令工具演示:")
    command_tool = CommandTool()
    
    print("\n4. 执行命令：echo 'Hello from JoyClaw'")
    result = command_tool.execute("echo 'Hello from JoyClaw'")
    if result['success']:
        print(f"   输出：{result['stdout'].strip()}")
    else:
        print(f"   错误：{result['stderr']}")
    
    print("\n5. 显示当前目录:")
    import platform
    cmd = "cd" if platform.system() == 'Windows' else "pwd"
    result = command_tool.execute(cmd)
    if result['success']:
        print(f"   {result['stdout'].strip()}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\n提示：要使用完整的 AI Agent 功能，需要配置 DeepSeek API Key")
    print("请复制 .env.example 为 .env 并设置 DEEPSEEK_API_KEY")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n发生错误：{e}")
        import traceback
        traceback.print_exc()
