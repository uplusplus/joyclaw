# JoyClaw - AI Agent 测试项目

## 1 项目目标

### 1.1 核心目标
在 joyclaw 项目中创建一个最小可用集的 AI Agent，用于验证其与多种 OpenAI API 兼容 LLM 的集成能力。

### 1.2 本地操作支持
支持对本地设备（如文件系统、本机命令等）的基础操作。

## 2 主要内容

### 2.1 多 LLM 支持
支持所有 OpenAI API 兼容的 LLM 服务：
- OpenAI (GPT-4o, GPT-4o-mini)
- DeepSeek
- 智谱 AI (GLM)
- 月之暗面 (Moonshot)
- 本地部署模型 (Ollama, vLLM 等)
- 其他兼容 OpenAI API 的服务

### 2.2 Agent 最小架构
设计与实现 AI Agent 的最小架构：能够解析输入、调用 LLM、通过 Function Calling 自动执行工具、输出结果。

**核心能力：**
- 支持自然语言操作本地文件（创建、读取、列出目录）
- 支持自然语言执行安全命令
- 通过 OpenAI Function Calling 实现工具自动调用

### 2.3 本地设备操作
实现本地设备基础操作能力，如安全的文件读写、命令执行。

### 2.4 演示与测试
提供基本演示脚本和测试。

## 3 验收标准

- [x] Agent 能与多种 LLM 模型交互
- [x] 能安全处理本地设备基础操作
- [x] 支持自然语言操作文件（Function Calling）
- [x] 结构清晰、易于后续扩展
- [x] 支持通过环境变量切换 LLM 提供商
- [x] 支持自定义 Base URL（兼容本地部署）
- [x] 提供常用 LLM 预设配置

## 4 项目结构

```
joyclaw/
├── README.md           # 项目说明
├── .env.example        # 配置示例
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

# 配置 LLM
cp .env.example .env
# 编辑 .env 设置 LLM_PROVIDER 和 LLM_API_KEY

# 运行演示
python examples/demo.py
```

## 6 配置说明

### 6.1 基本配置

```bash
# LLM 提供商 (openai, deepseek, zhipu, moonshot, ollama)
LLM_PROVIDER=deepseek

# API Key (必填，ollama 除外)
LLM_API_KEY=your_api_key

# Base URL (可选，不填则使用预设)
# LLM_BASE_URL=https://api.deepseek.com/v1

# Model (可选，不填则使用预设默认模型)
# LLM_MODEL=deepseek-chat
```

### 6.2 各提供商示例

**OpenAI:**
```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-xxx
LLM_MODEL=gpt-4o-mini
```

**DeepSeek:**
```bash
LLM_PROVIDER=deepseek
LLM_API_KEY=sk-xxx
```

**智谱 AI:**
```bash
LLM_PROVIDER=zhipu
LLM_API_KEY=xxx
LLM_MODEL=glm-4
```

**Ollama (本地):**
```bash
LLM_PROVIDER=ollama
LLM_MODEL=llama2
```

## 7 支持的 LLM 提供商

| 提供商 | LLM_PROVIDER | 默认模型 | Base URL |
|--------|--------------|----------|----------|
| OpenAI | openai | gpt-4o-mini | https://api.openai.com/v1 |
| DeepSeek | deepseek | deepseek-chat | https://api.deepseek.com/v1 |
| 智谱 AI | zhipu | glm-4 | https://open.bigmodel.cn/api/paas/v4 |
| 月之暗面 | moonshot | moonshot-v1-8k | https://api.moonshot.cn/v1 |
| Ollama | ollama | llama2 | http://localhost:11434/v1 |

## 8 更新日志

### 2026-03-14 - Function Calling 支持

**新增功能：**
- ✅ 实现 OpenAI Function Calling，Agent 可自动调用工具
- ✅ 支持自然语言操作文件（创建、读取、列出目录）
- ✅ 支持自然语言执行安全命令
- ✅ 添加 `tool_schemas.py` 定义工具 schema

**修复：**
- 🐛 修复 `demo.py` 路径问题，支持从任意目录运行

**验证：**
- 所有测试通过 (11 tests)
- 功能验证：自然语言创建文件、读取文件、列出目录均正常

### 2026-03-13 - 多 LLM 支持

**新增功能：**
- ✅ 支持 5 种 LLM 提供商：OpenAI, DeepSeek, 智谱 AI, 月之暗面, Ollama
- ✅ 统一配置系统 (`LLM_PROVIDER`, `LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`)
- ✅ 预设配置简化使用

## 9 许可证

MIT License - 详见 [LICENSE](LICENSE)
