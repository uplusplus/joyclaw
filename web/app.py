# -*- coding: utf-8 -*-
"""
JoyClaw Web 应用
提供 Web 界面与 AI Agent 交互
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
from pathlib import Path
import json
import traceback

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from agent.assistant import AIAssistant
from tools.device import FileTool, CommandTool, SystemInfoTool

app = Flask(__name__)
CORS(app)

# 初始化工具
file_tool = FileTool()
command_tool = CommandTool()
system_tool = SystemInfoTool()

# 全局 AI Assistant（可选，需要 API Key）
ai_assistant = None
try:
    ai_assistant = AIAssistant()
except Exception as e:
    print(f"⚠️ AI Assistant 未初始化: {e}")


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


# ==================== API 接口 ====================

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    与 AI Agent 对话
    POST: {"message": "用户消息"}
    """
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        if not ai_assistant:
            return jsonify({'error': 'AI Agent 未初始化，请检查 API Key 配置'}), 500
        
        # 调用 AI Agent
        response = ai_assistant.chat(message)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/files/list', methods=['GET'])
def list_files():
    """
    列出文件
    GET: ?directory=.&pattern=*.txt
    """
    try:
        directory = request.args.get('directory', '.')
        pattern = request.args.get('pattern', None)
        
        files = file_tool.list_files(directory, pattern)
        
        return jsonify({
            'success': True,
            'files': files,
            'directory': str(file_tool.base_dir / directory)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/files/read', methods=['GET'])
def read_file():
    """
    读取文件内容
    GET: ?path=file.txt
    """
    try:
        file_path = request.args.get('path', '')
        
        if not file_path:
            return jsonify({'error': '文件路径不能为空'}), 400
        
        content = file_tool.read_file(file_path)
        
        return jsonify({
            'success': True,
            'content': content,
            'path': file_path
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/files/write', methods=['POST'])
def write_file():
    """
    写入文件
    POST: {"path": "file.txt", "content": "内容"}
    """
    try:
        data = request.get_json()
        file_path = data.get('path', '')
        content = data.get('content', '')
        
        if not file_path:
            return jsonify({'error': '文件路径不能为空'}), 400
        
        result = file_tool.write_file(file_path, content)
        
        return jsonify({
            'success': result,
            'path': file_path
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/command/execute', methods=['POST'])
def execute_command():
    """
    执行命令
    POST: {"command": "命令", "cwd": "工作目录"}
    """
    try:
        data = request.get_json()
        command = data.get('command', '')
        cwd = data.get('cwd', None)
        
        if not command:
            return jsonify({'error': '命令不能为空'}), 400
        
        result = command_tool.execute(command, cwd)
        
        return jsonify({
            'success': result['success'],
            'stdout': result['stdout'],
            'stderr': result['stderr'],
            'return_code': result['return_code'],
            'command': command
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/system/info', methods=['GET'])
def system_info():
    """
    获取系统信息
    """
    try:
        info = system_tool.get_info()
        
        return jsonify({
            'success': True,
            'info': info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    获取对话历史
    """
    try:
        if ai_assistant and hasattr(ai_assistant, 'conversation_history'):
            history = ai_assistant.conversation_history
        else:
            history = []
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """
    清空对话历史
    """
    try:
        if ai_assistant:
            ai_assistant.reset()
        
        return jsonify({
            'success': True,
            'message': '对话历史已清空'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '资源不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


# ==================== 主函数 ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  JoyClaw Web 服务启动")
    print("  访问地址: http://localhost:5000")
    print("=" * 60)
    print("\n提示:")
    print("  - 按 Ctrl+C 停止服务")
    print("  - 首次运行请确保已安装 Flask: pip install flask flask-cors")
    print("  - AI Agent 需要 DeepSeek API Key 才能使用对话功能")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
