# -*- coding: utf-8 -*-
"""
AI Agent 功能测试（不依赖 DeepSeek API）
测试本地工具功能
"""

import sys
import os
from pathlib import Path

# 添加 src 到路径
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))
os.chdir(Path(__file__).parent)

from tools.device import FileTool, CommandTool, SystemInfoTool


def test_file_tool():
    """测试文件工具"""
    print("\n📁 测试 1: 文件工具")
    try:
        file_tool = FileTool()
        
        # 创建测试文件
        test_file = "test_agent_function.txt"
        test_content = "AI Agent 功能测试文件\n这是由 AI Agent 创建的内容。\n"
        
        print(f"  1. 创建文件：{test_file}")
        file_tool.write_file(test_file, test_content)
        print("     ✓ 文件创建成功")
        
        # 读取文件
        print(f"  2. 读取文件：{test_file}")
        content = file_tool.read_file(test_file)
        print(f"     ✓ 读取成功，内容：{content.strip()}")
        
        # 列出文件
        print(f"  3. 列出 .txt 文件")
        files = file_tool.list_files(pattern="*.txt")
        print(f"     ✓ 找到 {len(files)} 个文件")
        for f in files[:5]:  # 只显示前 5 个
            print(f"       - {f}")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_command_tool():
    """测试命令工具"""
    print("\n⚡ 测试 2: 命令工具")
    try:
        command_tool = CommandTool(timeout=10)
        
        # 测试 1: echo 命令
        print("  1. 执行 echo 命令")
        result = command_tool.execute("echo 'Hello from AI Agent'")
        if result['success']:
            print(f"     ✓ 成功：{result['stdout'].strip()}")
        else:
            print(f"     ✗ 失败：{result['stderr']}")
        
        # 测试 2: 显示目录
        print("  2. 显示当前目录")
        import platform
        cmd = "cd" if platform.system() == 'Windows' else "pwd"
        result = command_tool.execute(cmd)
        if result['success']:
            print(f"     ✓ {result['stdout'].strip()}")
        
        # 测试 3: 显示时间
        print("  3. 显示系统时间")
        cmd = "time /t" if platform.system() == 'Windows' else "date"
        result = command_tool.execute(cmd)
        if result['success']:
            print(f"     ✓ {result['stdout'].strip()}")
        
        # 测试 4: 安全机制测试
        print("  4. 测试安全机制（危险命令应该被阻止）")
        try:
            command_tool.execute("rm -rf /")
            print("     ✗ 安全机制未生效！")
            return False
        except ValueError as e:
            print(f"     ✓ 正确阻止：{e}")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_system_info():
    """测试系统信息工具"""
    print("\n💻 测试 3: 系统信息工具")
    try:
        system_tool = SystemInfoTool()
        info = system_tool.get_info()
        
        print("  系统信息:")
        print(f"    操作系统：{info['system']} {info['release']}")
        print(f"    主机名：{info['hostname']}")
        print(f"    当前用户：{info['user']}")
        print(f"    Python 版本：{info['python_version']}")
        print(f"    架构：{info['machine']}")
        
        print("  ✓ 系统信息获取成功")
        return True
    except Exception as e:
        print(f"  ✗ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_security():
    """测试文件安全机制"""
    print("\n🔒 测试 4: 文件安全机制")
    try:
        file_tool = FileTool()
        
        # 尝试访问受限路径
        print("  尝试访问受限路径...")
        try:
            file_tool.read_file("../../etc/passwd")
            print("  ✗ 安全机制未生效！")
            return False
        except PermissionError as e:
            print(f"  ✓ 正确阻止：{e}")
            return True
    except Exception as e:
        print(f"  ✗ 测试失败：{e}")
        return False


def main():
    """主测试函数"""
    print("=" * 70)
    print("  JoyClaw AI Agent - 本地功能测试")
    print("  （不依赖 DeepSeek API 网络访问）")
    print("=" * 70)
    
    results = []
    
    # 运行所有测试
    results.append(("文件工具", test_file_tool()))
    results.append(("命令工具", test_command_tool()))
    results.append(("系统信息", test_system_info()))
    results.append(("安全机制", test_file_security()))
    
    # 总结
    print("\n" + "=" * 70)
    print("  测试结果总结")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {name}: {status}")
    
    print(f"\n  总计：{passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有本地功能测试通过！")
        print("\n说明:")
        print("  - 本地设备工具功能正常")
        print("  - 安全机制运行正常")
        print("  - AI Agent 架构就绪")
        print("\n注意:")
        print("  - DeepSeek API 集成需要网络连接")
        print("  - 当前网络环境无法访问 api.deepseek.com")
        print("  - 建议在可访问外网的环境中进行完整测试")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")


if __name__ == "__main__":
    main()
