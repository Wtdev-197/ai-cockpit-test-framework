"""IVI座舱模拟器 - 零硬件模式下模拟座舱行为"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class IVIState:
    """座舱状态"""
    volume: int = 50  # 音量 0-100
    music_playing: bool = False
    current_track: str = ""
    temperature: float = 22.0  # 空调温度


class IVISimulator:
    """IVI模拟器, 用于无硬件模式下测试"""

    def __init__(self):
        self.states = IVIState()
        self._bus_message = []  # 模拟发送到总线的消息


