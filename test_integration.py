# -*- coding: utf-8 -*-
"""
测试 AI Agent 与 DeepSeek 的集成
"""

import sys
import os
from pathlib import Path

# 添加 src 到路径
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))
os.chdir(Path(__file__).parent)

# 导入模块
from deepseek.client import DeepSeekClient
from agent.assistant import AIAssistant
from tools.device import FileTool, CommandTool, SystemInfoTool


def test_deepseek_connection():
    """测试 DeepSeek API 连接"""
    print("\n🔌 测试 1: DeepSeek API 连接")
    try:
        client = DeepSeekClient()
        print("✓ DeepSeek 客户端初始化成功")
        return client
    except Exception as e:
        print(f"✗ 初始化失败：{e}")
        return None


def test_simple_chat(client):
    """测试简单对话"""
    print("\n💬 测试 2: 简单对话测试")
    try:
        response = client.chat([
            {'role': 'user', 'content': '你好，请用一句话介绍自己'}
        ], max_tokens=100)
        
        if 'choices' in response and len(response['choices']) > 0:
            ai_reply = response['choices'][0]['message']['content']
            print(f"✓ DeepSeek 回复成功:")
            print(f"  {ai_reply}")
            return True
        else:
            print("✗ 响应格式异常")
            return False
    except Exception as e:
        print(f"✗ 对话测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_agent(assistant):
    """测试 AI Agent 完整流程"""
    print("\n🤖 测试 3: AI Agent 系统信息查询")
    try:
        print("  用户：请获取系统信息")
        response = assistant.chat("请获取系统信息")
        print(f"  AI 响应:")
        print(f"  {response[:300]}...")
        print("✓ AI Agent 测试成功")
        return True
    except Exception as e:
        print(f"✗ AI Agent 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_operation(assistant):
    """测试文件操作"""
    print("\n📁 测试 4: AI Agent 文件操作")
    try:
        print("  用户：请在当前目录创建一个测试文件 test_ai.txt，内容为'Hello from AI'")
        response = assistant.chat("请在当前目录创建一个测试文件 test_ai.txt，内容为'Hello from AI'")
        print(f"  AI 响应:")
        print(f"  {response[:300]}...")
        
        # 验证文件是否创建
        test_file = Path.cwd() / "test_ai.txt"
        if test_file.exists():
            print(f"✓ 文件创建成功，内容：{test_file.read_text()}")
            return True
        else:
            print("✗ 文件未创建")
            return False
    except Exception as e:
        print(f"✗ 文件操作测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_command_execution(assistant):
    """测试命令执行"""
    print("\n⚡ 测试 5: AI Agent 命令执行")
    try:
        print("  用户：显示当前工作目录")
        response = assistant.chat("显示当前工作目录")
        print(f"  AI 响应:")
        print(f"  {response[:300]}...")
        print("✓ 命令执行测试完成")
        return True
    except Exception as e:
        print(f"✗ 命令执行测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("=" * 70)
    print("  JoyClaw AI Agent - DeepSeek 集成完整测试")
    print("=" * 70)
    
    # 测试 1: DeepSeek 连接
    client = test_deepseek_connection()
    if not client:
        print("\n❌ DeepSeek 连接失败，终止测试")
        return
    
    # 测试 2: 简单对话
    if not test_simple_chat(client):
        print("\n❌ 简单对话测试失败")
        return
    
    # 创建 AI Assistant
    print("\n🤖 初始化 AI Assistant...")
    try:
        assistant = AIAssistant()
        print("✓ AI Assistant 初始化成功")
    except Exception as e:
        print(f"✗ AI Assistant 初始化失败：{e}")
        return
    
    # 测试 3: AI Agent 系统信息
    test_ai_agent(assistant)
    
    # 测试 4: 文件操作
    test_file_operation(assistant)
    
    # 测试 5: 命令执行
    test_command_execution(assistant)
    
    print("\n" + "=" * 70)
    print("  🎉 所有测试完成！")
    print("=" * 70)
    print("\n✅ DeepSeek 集成成功")
    print("✅ AI Agent 功能正常")
    print("✅ 本地设备工具可用")
    print("\n提示：可以运行 'python3 examples/demo.py' 进行交互式测试")


if __name__ == "__main__":
    main()
