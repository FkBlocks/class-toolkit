import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), 'log')
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "./running.log")

def create_logger(clear_log=False):
    """创建logger实例

    Args:
        clear_log: 是否清空日志（仅在主程序启动时为True）
    """
    # 清空日志文件，只记录最近一次的运行
    if clear_log:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 程序启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    logger = logging.getLogger("ClassHelper")
    logger.setLevel(logging.INFO)

    # 避免重复添加handler
    if not logger.handlers:
        file_handler = logging.FileHandler(
            log_file,
            encoding='utf-8',
            mode='a'
        )

        fmt = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%H:%M:%S"
        )
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger

# 默认创建不清空日志的logger实例
logger = create_logger(clear_log=False)