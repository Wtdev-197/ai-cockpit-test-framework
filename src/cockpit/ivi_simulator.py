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
        self.state = IVIState()
        self.states = self.state
        self._bus_message = []  # 模拟发送到总线的消息

    def set_volume(self, volume: int) -> None:
        """设置音量并记录对应的总线消息"""
        if not 0 <= volume <= 100:
            raise ValueError("音量必须在 0 到 100 之间")

        self.state.volume = volume
        self._bus_message.append({
            "id": 0x100,
            "data": [volume],
        })

    def get_volume(self) -> int:
        """获取当前音量"""
        return self.state.volume

    def play_music(self, track: str) -> None:
        """开始播放指定曲目"""
        self.state.music_playing = True
        self.state.current_track = track

    def get_last_bus_message(self):
        """获取最后一条模拟总线消息"""
        return self._bus_message[-1] if self._bus_message else None

    def reset(self) -> None:
        """恢复初始状态并清空总线消息"""
        self.state = IVIState()
        self.states = self.state
        self._bus_message.clear()


