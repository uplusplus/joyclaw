# JoyClaw - AI Agent 测试项目

## 1 项目目标

### 1.1 核心目标
在 joyclaw 项目中创建一个最小可用集的 AI Agent，用于验证其与 deepseek 大模型的集成能力。

### 1.2 本地操作支持
支持对本地设备（如文件系统、本机命令等）的基础操作。

## 2 主要内容

### 2.1 DeepSeek 集成
集成 deepseek 模型并实现基本通信接口。

### 2.2 Agent 最小架构
设计与实现 AI Agent 的最小架构：能够解析输入、调用 deepseek、输出结果。

### 2.3 本地设备操作
实现本地设备基础操作能力，如安全的文件读写、命令执行。

### 2.4 演示与测试
提供基本演示脚本和测试。

## 3 验收标准

- [x] Agent 能与 deepseek 模型双向交互
- [x] 能安全处理本地设备基础操作
- [x] 结构清晰、易于后续扩展

## 4 项目结构

```
joyclaw/
├── README.md           # 项目说明
├── src/
│   ├── agent/         # Agent 核心实现
│   ├── tools/         # 本地操作工具
│   └── config/        # 配置文件
├── tests/             # 测试用例
├── examples/          # 演示脚本
└── requirements.txt   # Python 依赖
```

## 5 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 DeepSeek API Key
export DEEPSEEK_API_KEY=your_api_key

# 运行演示
python examples/demo.py
```

## 6 许可证

MIT License - 详见 [LICENSE](LICENSE)
