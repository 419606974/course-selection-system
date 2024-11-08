#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/21 17:34
** @Author：Anonymous
** @Description：
**************************************************************
'''
from loguru import logger

import settings

# 定义基础日志处理器
logger.add(
    sink=settings.Config.LOG_BASE_DIR + "{time:%Y-%m-%d-%H-%M-%S}" + "-run.log",
    level="DEBUG",
    format="[{time:%Y-%m-%d %H:%M:%S}] | {level} | {file}:{function}:{line} | {message}",
    rotation="200 MB",
    retention=5,
    filter=lambda record: record["extra"].get("type") == "base",
)

# 为方便在其他模块中使用，提供带上下文的记录方法
base_logger = logger.bind(type='base')
audit_logger = logger.bind(type='audit')
# 导出logger供其他模块使用
__all__ = ["base_logger", "audit_logger"]
