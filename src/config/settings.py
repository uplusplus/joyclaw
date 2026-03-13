# -*- coding: utf-8 -*-
"""
配置管理模块
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """应用配置"""
    
    # DeepSeek API 配置
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # 安全配置
    ALLOWED_COMMANDS: list = os.getenv("ALLOWED_COMMANDS", "ls,cat,echo,pwd").split(",")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "1048576"))  # 1MB
    
    @classmethod
    def validate(cls) -> bool:
        """验证必要配置"""
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")
        return True

settings = Settings()
