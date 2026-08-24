"""CAN总线适配器单元测试"""
import pytest
from src.cockpit.bus_adapter import CANBusAdapter


@pytest.fixture
def bus_adapter():
    adapter = CANBusAdapter()
    adapter.connect()
    yield adapter
    adapter.disconnect()


class TestCANBusAdapter:
    """总线适配器测试"""

    def test_parse_response_valid(self, bus_adapter):
        """测试正常解析：0x0032 = 50"""
        result = bus_adapter.parse_response(b'\x00\x32')
        assert result == 50

    def test_parse_response_max(self, bus_adapter):
        """测试最大值：0x0064 = 100"""
        result = bus_adapter.parse_response(b'\x00\x64')
        assert result == 100

    def test_parse_response_insufficient_data(self, bus_adapter):
        """测试数据不足应抛异常"""
        with pytest.raises(ValueError, match="至少需要2字节"):
            bus_adapter.parse_response(b'\x00')

    def test_send_signal(self, bus_adapter):
        """测试发送信号"""
        bus_adapter.send_signal(0x100, 50)
        msg = bus_adapter.get_last_message()
        assert msg["id"] == 0x100
        assert msg["value"] == 50