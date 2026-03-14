#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JoyClaw 演示脚本
演示 Agent 与多种 LLM 的交互和本地操作能力
"""
import sys
sys.path.insert(0, "..")

from src.agent import LLMAgent
from src.tools import file_tools, command_tools
from src.config.settings import settings


def demo_config():
    """演示配置能力"""
    print("=" * 50)
    print("⚙️  配置信息")
    print("=" * 50)
    
    llm_config = settings.get_llm_config()
    print(f"\n当前 LLM 配置:")
    print(f"  Provider: {llm_config['provider']}")
    print(f"  Model: {llm_config['model']}")
    print(f"  Base URL: {llm_config['base_url']}")
    print(f"  API Key: {llm_config['api_key'][:10]}...")


def demo_tools():
    """演示工具能力"""
    print("\n" + "=" * 50)
    print("🔧 工具能力演示")
    print("=" * 50)
    
    # 文件操作演示
    print("\n📁 文件操作:")
    
    # 写入测试文件
    result = file_tools.write_file("test_hello.txt", "Hello from JoyClaw Agent!")
    print(f"  写入: {result}")
    
    # 读取文件
    content = file_tools.read_file("test_hello.txt")
    print(f"  读取: {content}")
    
    # 列出目录
    print(f"\n📂 当前目录:\n{file_tools.list_dir('.')}")
    
    # 命令执行演示
    print("\n⚙️  命令执行:")
    success, output = command_tools.execute("pwd")
    print(f"  pwd: {output}")
    
    print(f"\n  {command_tools.list_allowed()}")


def demo_agent():
    """演示 Agent 对话能力"""
    print("\n" + "=" * 50)
    print("🤖 Agent 对话演示")
    print("=" * 50)
    
    try:
        agent = LLMAgent()
        print(f"\n当前使用: {agent.provider} ({agent.model})")
        
        # 测试对话
        questions = [
            "你好，请介绍一下你自己",
            "你能做什么？",
            "请用一句话解释什么是 AI Agent"
        ]
        
        for q in questions:
            print(f"\n👤 用户: {q}")
            response = agent.chat(q)
            print(f"🤖 Agent: {response}")
            
    except ValueError as e:
        print(f"\n⚠️  配置错误: {e}")
        print("请设置环境变量 LLM_API_KEY 或 DEEPSEEK_API_KEY")


def demo_interactive():
    """交互模式"""
    print("\n" + "=" * 50)
    print("💬 交互模式 (输入 'quit' 退出)")
    print("=" * 50)
    
    try:
        agent = LLMAgent()
        print(f"\n当前使用: {agent.provider} ({agent.model})")
        
        while True:
            user_input = input("\n👤 你: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
            
            response = agent.chat(user_input)
            print(f"🤖 Agent: {response}")
            
    except ValueError as e:
        print(f"\n⚠️  配置错误: {e}")
        print("请设置环境变量 LLM_API_KEY 或 DEEPSEEK_API_KEY")


def main():
    """主函数"""
    print("\n🎯 JoyClaw AI Agent 演示")
    
    # 配置演示
    demo_config()
    
    # 工具演示
    demo_tools()
    
    # Agent 演示 (需要 API Key)
    demo_agent()
    
    # 交互模式
    print("\n是否进入交互模式？(y/n): ", end="")
    choice = input().strip().lower()
    if choice == "y":
        demo_interactive()


if __name__ == "__main__":
    main()
