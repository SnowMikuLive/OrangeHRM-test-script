import logging
import os
from datetime import datetime

def setup_logger():
    """Set up logger with file and console handlers / 设置带有文件和控制台处理程序的日志记录器"""
    # Create logs directory if it doesn't exist / 如果日志目录不存在则创建
    if not os.path.exists('Logs'):
        os.makedirs('Logs')
    
    # Create logger / 创建日志记录器
    logger = logging.getLogger('OrangeHRM_Test')
    logger.setLevel(logging.DEBUG)
    
    # Create formatters / 创建格式化器
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Create file handler / 创建文件处理程序
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(f'Logs/test_{timestamp}.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Create console handler / 创建控制台处理程序
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger / 将处理程序添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger / 防止传播到根日志记录器
    logger.propagate = False
    
    return logger 