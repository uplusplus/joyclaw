# JoyClaw Web 前端使用指南

## 🌟 功能概览

JoyClaw Web 提供了一个现代化的 Web 界面，用于与 AI Agent 进行交互。

### 主要功能

1. **💬 对话功能**
   - 与 AI Agent 进行对话
   - 查看对话历史
   - 清空对话历史

2. **📁 文件管理**
   - 列出文件列表
   - 读取文件内容
   - 创建/编辑文件
   - 保存文件

3. **⚡ 命令执行**
   - 执行系统命令
   - 查看执行结果
   - 常用命令快捷方式

4. **💻 系统信息**
   - 查看操作系统信息
   - 查看硬件配置
   - 查看用户信息

## 🚀 启动方式

### 方式 1: 快速启动脚本（推荐）

**Windows**:
```bash
双击 start_web.bat
```

**Linux/Mac**:
```bash
chmod +x start_web.sh
./start_web.sh
```

### 方式 2: 命令行启动

```bash
# 安装依赖
pip3 install flask flask-cors

# 启动服务
cd web
python3 app.py

# 访问页面
浏览器打开: http://localhost:5000
```

## 📋 API 接口文档

### 1. 对话接口

**POST /api/chat**
```json
请求: {"message": "用户消息"}
响应: {"success": true, "response": "AI 回复"}
```

### 2. 文件操作接口

**GET /api/files/list**
```
参数: directory, pattern
响应: {"success": true, "files": ["file1.txt", "file2.txt"]}
```

**GET /api/files/read**
```
参数: path
响应: {"success": true, "content": "文件内容"}
```

**POST /api/files/write**
```json
请求: {"path": "file.txt", "content": "内容"}
响应: {"success": true}
```

### 3. 命令执行接口

**POST /api/command/execute**
```json
请求: {"command": "命令", "cwd": "工作目录"}
响应: {
    "success": true,
    "stdout": "输出",
    "stderr": "错误",
    "return_code": 0
}
```

### 4. 系统信息接口

**GET /api/system/info**
```json
响应: {
    "success": true,
    "info": {
        "system": "Windows",
        "release": "10",
        "machine": "AMD64",
        "hostname": "HOSTNAME",
        "user": "username",
        "python_version": "3.10.0"
    }
}
```

## 🎨 界面说明

### 侧边栏
- **对话**: AI 对话界面
- **文件**: 文件管理界面
- **命令**: 命令执行界面
- **系统**: 系统信息界面

### 主内容区
根据选择的功能显示相应的操作界面

## 🔧 技术栈

- **后端**: Flask (Python Web 框架)
- **前端**: HTML5 + CSS3 + JavaScript
- **样式**: 现代化响应式设计
- **通信**: RESTful API

## 📁 项目结构

```
web/
├── app.py              # Flask 应用主文件
├── templates/
│   └── index.html      # 主页面模板
└── static/
    ├── css/
    │   └── style.css   # 样式文件
    └── js/
        └── app.js      # JavaScript 文件
```

## 🎯 使用示例

### 1. 对话示例
```
用户: 你好，请获取系统信息
AI: [返回系统信息]
```

### 2. 文件操作示例
```
1. 在文件面板输入目录路径 "."
2. 输入模式 "*.txt"
3. 点击"列出文件"
4. 点击文件名查看内容
5. 在编辑器中修改并保存
```

### 3. 命令执行示例
```
1. 输入命令: pwd
2. 点击"执行"
3. 查看输出结果

或使用快捷命令按钮
```

## ⚠️ 注意事项

1. **API Key**: AI 对话功能需要配置 DeepSeek API Key
2. **网络**: 对话功能需要访问 DeepSeek API
3. **安全**: 文件操作限制在项目目录内
4. **命令**: 只能执行白名单内的命令

## 🐛 故障排除

### 无法启动服务
```bash
# 检查 Python 版本
python3 --version

# 安装依赖
pip3 install flask flask-cors
```

### AI 对话无响应
- 检查 `.env` 文件中的 API Key 配置
- 检查网络连接
- 查看控制台错误信息

### 文件操作失败
- 检查文件路径是否正确
- 检查文件权限
- 确认文件在允许的目录范围内

## 📸 截图

（待添加）

---

**开发时间**: 2026-03-13  
**版本**: 1.0.0  
**作者**: JoyClaw Team
