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

---

## 7 开发计划：支持 OpenAI API 兼容的多种 LLM

### 7.1 需求背景
当前 Agent 仅支持 DeepSeek，需要扩展为支持所有 OpenAI API 兼容的 LLM 服务，包括但不限于：
- OpenAI (GPT-4, GPT-3.5)
- DeepSeek
- 智谱 AI (GLM)
- 月之暗面 (Moonshot)
- 本地部署模型 (Ollama, vLLM 等)
- 其他兼容 OpenAI API 的服务

### 7.2 开发任务

| 序号 | 任务 | 说明 | 状态 |
|------|------|------|------|
| 1 | 重构配置模块 | 支持多 LLM 配置，API Key、Base URL、模型名称均可配置 | ✅ 完成 |
| 2 | 重构 Agent 初始化 | 从硬编码 DeepSeek 改为通用 LLM 客户端 | ✅ 完成 |
| 3 | 添加 LLM 提供商预设 | 提供常用 LLM 的默认配置模板 | ✅ 完成 |
| 4 | 更新 .env.example | 添加新配置项示例 | ✅ 完成 |
| 5 | 更新测试用例 | 支持多 LLM 测试 | ✅ 完成 |
| 6 | 更新 Demo | 展示多 LLM 切换能力 | ✅ 完成 |

### 7.3 配置设计

```bash
# .env 配置示例
# LLM 提供商选择
LLM_PROVIDER=deepseek  # openai, deepseek, zhipu, moonshot, ollama, custom

# 通用配置 (适用于所有提供商)
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# 或使用提供商预设 (自动填充 base_url)
# LLM_PROVIDER=openai
# LLM_API_KEY=sk-xxx
# LLM_MODEL=gpt-4
```

### 7.4 验收标准

- [x] 支持通过环境变量切换不同 LLM 提供商
- [x] 支持自定义 Base URL（兼容本地部署）
- [x] 提供常用 LLM 预设配置
- [x] 所有测试用例通过
- [x] Demo 展示多 LLM 切换
