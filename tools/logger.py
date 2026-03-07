# A float ball class toolkit suitable for large-screen touch all-in-one machines
# Copyright (C) 2026 FkBlocks
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "running.log")

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
            fmt="[%(asctime)s][%(levelname)s]: %(message)s",
            datefmt="%H:%M:%S"
        )
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger

# 默认创建不清空日志的logger实例
logger = create_logger(clear_log=False)
