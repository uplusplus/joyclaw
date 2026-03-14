# -*- coding: utf-8 -*-
"""
配置管理模块 - 支持多种 OpenAI API 兼容的 LLM
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM 提供商预设配置
LLM_PRESETS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
    },
    "zhipu": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4",
    },
    "moonshot": {
        "base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-8k",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "default_model": "llama2",
    },
}


class Settings:
    """应用配置"""
    
    # LLM 提供商
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "deepseek")
    
    # 通用 LLM 配置（优先使用显式配置，否则使用预设）
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", os.getenv("DEEPSEEK_API_KEY", ""))
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "")
    
    # 兼容旧配置
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "")
    
    # 安全配置
    ALLOWED_COMMANDS: list = os.getenv("ALLOWED_COMMANDS", "ls,cat,echo,pwd,whoami,date").split(",")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "1048576"))  # 1MB
    
    @classmethod
    def _resolve_llm_config(cls):
        """解析 LLM 配置，处理预设和默认值"""
        # 优先级：显式配置 > 预设 > 旧配置 > 默认值
        
        # API Key
        api_key = cls.LLM_API_KEY or cls.DEEPSEEK_API_KEY
        if not api_key and cls.LLM_PROVIDER == "ollama":
            api_key = "ollama"  # Ollama 不需要真实 key
        
        # Base URL
        base_url = cls.LLM_BASE_URL or cls.DEEPSEEK_BASE_URL
        if not base_url and cls.LLM_PROVIDER in LLM_PRESETS:
            base_url = LLM_PRESETS[cls.LLM_PROVIDER]["base_url"]
        
        # Model
        model = cls.LLM_MODEL or cls.DEEPSEEK_MODEL
        if not model and cls.LLM_PROVIDER in LLM_PRESETS:
            model = LLM_PRESETS[cls.LLM_PROVIDER]["default_model"]
        
        return api_key, base_url, model
    
    @classmethod
    def get_llm_config(cls) -> dict:
        """获取 LLM 配置字典"""
        api_key, base_url, model = cls._resolve_llm_config()
        return {
            "provider": cls.LLM_PROVIDER,
            "api_key": api_key,
            "base_url": base_url,
            "model": model,
        }
    
    @classmethod
    def validate(cls) -> bool:
        """验证必要配置"""
        api_key, base_url, model = cls._resolve_llm_config()
        if not api_key:
            raise ValueError("LLM_API_KEY 或 DEEPSEEK_API_KEY 环境变量未设置")
        if not base_url:
            raise ValueError("LLM_BASE_URL 未设置且无预设配置")
        if not model:
            raise ValueError("LLM_MODEL 未设置且无预设配置")
        return True


settings = Settings()
