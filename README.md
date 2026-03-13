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
# 简单工具演示（无需 API Key）
python examples/simple_demo.py

# 完整 AI Agent 演示（需要 API Key 和网络）
python examples/demo.py
```

## 🧪 测试

### 本地功能测试（无需网络）
```bash
python test_local_features.py
```

### 完整集成测试（需要网络）
```bash
python test_integration.py
```

### 单元测试
```bash
python -m pytest tests/ -v
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

## 📊 测试状态

| 功能模块 | 状态 | 说明 |
|---------|------|------|
| 文件工具 | ✅ 通过 | 创建、读取、列出文件功能正常 |
| 命令工具 | ✅ 通过 | 安全命令执行、白名单机制正常 |
| 系统信息 | ✅ 通过 | 系统信息查询功能正常 |
| 安全机制 | ✅ 通过 | 路径限制、命令过滤正常 |
| DeepSeek API | ⚠️ 待测 | 代码完成，需网络环境测试 |

详细测试报告见 [TEST_REPORT.md](TEST_REPORT.md)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📚 相关文档

- [开发总结](DEVELOPMENT_SUMMARY.md) - 开发过程总结
- [测试报告](TEST_REPORT.md) - 详细测试报告
- [推送说明](PUSH_INSTRUCTIONS.md) - GitHub 推送指南
