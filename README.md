# JoyClaw - AI Agent 最小功能项目

基于 joyclaw 集成 deepseek 并操作本地设备的 AI Agent 最小功能项目。

## 🎯 项目目标

- 在 joyclaw 项目中创建一个最小可用集的 AI Agent，用于验证其与 deepseek 大模型的集成能力
- 支持对本地设备（如文件系统、本机命令等）的基础操作

## 📋 主要内容

### 1. DeepSeek 集成
- 集成 deepseek 模型并实现基本通信接口
- 支持 API 调用和流式响应

### 2. AI Agent 核心架构
- 解析用户输入
- 调用 deepseek 模型
- 处理和输出结果

### 3. 本地设备操作能力
- 安全的文件读写操作
- 安全的命令执行
- 系统信息查询

## 🚀 快速开始

### 环境要求
- Python 3.8+
- DeepSeek API Key

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置 API Key

创建 `.env` 文件：
```
DEEPSEEK_API_KEY=your_api_key_here
```

### 运行示例

```bash
python examples/demo.py
```

## 📁 项目结构

```
joyclaw/
├── src/
│   ├── agent/          # AI Agent 核心逻辑
│   ├── deepseek/       # DeepSeek 模型集成
│   └── tools/          # 本地设备工具
├── tests/              # 测试用例
├── examples/           # 演示脚本
├── requirements.txt    # 依赖列表
├── README.md          # 项目说明
└── LICENSE            # MIT 许可证
```

## 🧪 测试

```bash
python -m pytest tests/ -v
```

## 📝 验收标准

- ✅ Agent 能与 deepseek 模型双向交互
- ✅ 能安全处理本地设备基础操作
- ✅ 结构清晰、易于后续扩展

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
