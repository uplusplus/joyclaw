# -*- coding: utf-8 -*-
"""
JoyClaw AI Agent 演示脚本
展示 AI Agent 与 DeepSeek 集成的基本功能
"""

import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from agent import AIAssistant
from deepseek import DeepSeekClient
from tools import FileTool, CommandTool, SystemInfoTool


def demo_basic_chat():
    """演示基本对话功能"""
    print("=" * 60)
    print("演示 1: 基本对话")
    print("=" * 60)
    
    assistant = AIAssistant()
    
    questions = [
        "你好，你能做什么？",
        "请获取系统信息",
        "列出当前目录的文件"
    ]
    
    for question in questions:
        print(f"\n👤 用户：{question}")
        print("🤖 AI:")
        response = assistant.chat(question)
        print(response)
        print("-" * 60)


def demo_file_operations():
    """演示文件操作功能"""
    print("\n" + "=" * 60)
    print("演示 2: 文件操作")
    print("=" * 60)
    
    assistant = AIAssistant()
    
    # 创建测试文件
    test_content = """这是一个测试文件。
JoyClaw AI Agent 演示项目。
"""
    
    questions = [
        f'请在当前目录创建文件 "test_demo.txt"，内容为：{test_content}',
        "读取刚才创建的 test_demo.txt 文件",
        "列出当前目录的所有 .txt 文件"
    ]
    
    for question in questions:
        print(f"\n👤 用户：{question}")
        print("🤖 AI:")
        response = assistant.chat(question)
        print(response)
        print("-" * 60)


def demo_command_execution():
    """演示命令执行功能"""
    print("\n" + "=" * 60)
    print("演示 3: 命令执行")
    print("=" * 60)
    
    assistant = AIAssistant()
    
    questions = [
        "显示当前工作目录",
        "显示系统时间",
        "显示当前用户信息"
    ]
    
    for question in questions:
        print(f"\n👤 用户：{question}")
        print("🤖 AI:")
        response = assistant.chat(question)
        print(response)
        print("-" * 60)


def demo_interactive():
    """交互式演示"""
    print("\n" + "=" * 60)
    print("演示 4: 交互式对话")
    print("=" * 60)
    print("输入 'quit' 或 'exit' 退出对话\n")
    
    assistant = AIAssistant()
    
    while True:
        try:
            user_input = input("👤 用户：").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("🤖 AI: 再见！")
                break
            
            if not user_input:
                continue
            
            print("🤖 AI:")
            response = assistant.chat(user_input)
            print(response)
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n🤖 AI: 再见！")
            break
        except Exception as e:
            print(f"发生错误：{e}")


def demo_tools_directly():
    """直接演示工具功能"""
    print("\n" + "=" * 60)
    print("演示 5: 工具直接调用")
    print("=" * 60)
    
    # 文件工具
    print("\n📁 文件工具演示:")
    file_tool = FileTool()
    print(f"当前目录：{file_tool.base_dir}")
    
    # 创建测试文件
    test_file = "demo_test.txt"
    test_content = "Hello, JoyClaw!\n"
    file_tool.write_file(test_file, test_content)
    print(f"✓ 创建文件：{test_file}")
    
    # 读取文件
    content = file_tool.read_file(test_file)
    print(f"✓ 读取文件内容：{content.strip()}")
    
    # 列出文件
    files = file_tool.list_files(pattern="*.txt")
    print(f"✓ .txt 文件列表：{files}")
    
    # 系统信息工具
    print("\n💻 系统信息工具演示:")
    system_tool = SystemInfoTool()
    info = system_tool.get_info()
    print(f"系统：{info['system']} {info['release']}")
    print(f"主机名：{info['hostname']}")
    print(f"Python 版本：{info['python_version']}")
    
    # 命令工具
    print("\n⚡ 命令工具演示:")
    command_tool = CommandTool()
    result = command_tool.execute("echo 'Hello from command tool'")
    if result['success']:
        print(f"✓ 命令执行成功：{result['stdout'].strip()}")
    else:
        print(f"✗ 命令执行失败：{result['stderr']}")


def main():
    """主函数"""
    import sys
    
    print("\n" + "=" * 60)
    print("  JoyClaw AI Agent 演示")
    print("  基于 DeepSeek 的本地设备 AI Agent")
    print("=" * 60)
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        print(f"\n使用命令行参数: {choice}")
    else:
        print("\n请选择演示模式:")
        print("1. 基本对话演示")
        print("2. 文件操作演示")
        print("3. 命令执行演示")
        print("4. 交互式对话")
        print("5. 工具直接调用演示")
        print("6. 运行所有演示")
        print("\n提示: 也可以直接运行 'python demo.py 5' 来指定模式")
        
        try:
            choice = input("\n请输入选项 (1-6): ").strip()
            if not choice:
                choice = '5'  # 空输入默认运行工具演示
        except EOFError:
            # 非交互环境，默认运行工具演示
            print("\n检测到非交互环境，默认运行工具直接调用演示...")
            choice = '5'
    
    try:
        if choice == '1':
            demo_basic_chat()
        elif choice == '2':
            demo_file_operations()
        elif choice == '3':
            demo_command_execution()
        elif choice == '4':
            demo_interactive()
        elif choice == '5':
            demo_tools_directly()
        elif choice == '6':
            demo_tools_directly()
            print("\n\n⚠️  注意：以下演示需要有效的 DeepSeek API Key")
            print("=" * 60)
            try:
                demo_basic_chat()
                demo_file_operations()
                demo_command_execution()
            except Exception as e:
                print(f"\n⚠️  AI 对话演示需要配置 API Key: {e}")
        else:
            print("无效选项！")
            return
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n演示已中断")
    except Exception as e:
        print(f"\n发生错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
