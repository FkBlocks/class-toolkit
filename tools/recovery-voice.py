from pycaw.pycaw import AudioUtilities
from logger import logger

def set_volume_to_max():
    """
    将系统主音量设置为100%
    """
    try:
        logger.info("启动音量恢复")
        # 获取默认音频设备
        devices = AudioUtilities.GetSpeakers()
        logger.info(f"找到音频设备: {devices.FriendlyName}")
        # 使用设备的 EndpointVolume 属性
        volume = devices.EndpointVolume

        # 设置音量为100% (范围是0.0到1.0，1.0是100%)
        volume.SetMasterVolumeLevelScalar(1.0, None)

        # 获取当前音量级别（-65.25到0.0）
        current_level = volume.GetMasterVolumeLevel()
        # 获取当前音量百分比（0.0到1.0）
        current_scalar = volume.GetMasterVolumeLevelScalar()

        logger.info(f"当前音量级别: {current_level:.2f} dB")
        logger.info(f"当前音量百分比: {current_scalar * 100:.0f}%")
        logger.info("音量已恢复到100%")

    except Exception as e:
        logger.error(f"设置音量失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    set_volume_to_max()