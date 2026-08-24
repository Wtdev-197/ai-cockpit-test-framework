"""CAN总线适配器 - 负责信号收发和解析"""
from typing import Dict, Any


class CANBusAdapter:
    """CAN总线通信适配器"""

    def __init__(self, channel: int = 0, bitrate: int = 500000):
        self.channel = channel
        self.bitrate = bitrate
        self._connected = False
        self._message_log = []

    def connect(self) -> bool:
        """连接CAN总线"""
        self._connected = True
        return True

    def disconnect(self) -> None:
        """断开连接"""
        self._connected = False

    def send_signal(self, signal_id: int, value: int) -> None:
        """发送CAN信号"""
        if not self._connected:
            raise ConnectionError("CAN总线未连接")
        self._message_log.append({
            "id": signal_id,
            "value": value,
            "direction": "tx"
        })

    def parse_response(self, raw_bytes: bytes) -> int:
        """解析CAN响应（大端序，修复字节序bug）"""
        if len(raw_bytes) < 2:
            raise ValueError("至少需要2字节数据")
        # 修复：使用大端序解析（之前错误地用了小端序或单字节）
        return int.from_bytes(raw_bytes[:2], byteorder='big')

    def get_last_message(self) -> Dict[str, Any]:
        """获取最后一条消息"""
        return self._message_log[-1] if self._message_log else {}