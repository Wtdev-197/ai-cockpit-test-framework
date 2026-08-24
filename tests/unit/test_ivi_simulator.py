"""IVI模拟器单元测试"""
import pytest
from src.cockpit.ivi_simulator import IVISimulator


class TestIVISimulator:
    """IVI模拟器测试"""

    def test_set_volume_valid(self, ivi_simulator):
        """测试合法音量设置"""
        ivi_simulator.set_volume(50)
        assert ivi_simulator.get_volume() == 50

    def test_set_volume_boundary_min(self, ivi_simulator):
        """测试音量下限边界"""
        ivi_simulator.set_volume(0)
        assert ivi_simulator.get_volume() == 0

    def test_set_volume_boundary_max(self, ivi_simulator):
        """测试音量上限边界"""
        ivi_simulator.set_volume(100)
        assert ivi_simulator.get_volume() == 100

    @pytest.mark.parametrize("invalid_volume", [-1, 101, 200])
    def test_set_volume_invalid(self, ivi_simulator, invalid_volume):
        """测试非法音量值应抛出异常"""
        with pytest.raises(ValueError):
            ivi_simulator.set_volume(invalid_volume)

    def test_play_music(self, ivi_simulator):
        """测试播放音乐"""
        ivi_simulator.play_music("离不开你的依赖")
        assert ivi_simulator.state.music_playing is True
        assert ivi_simulator.state.current_track == "离不开你的依赖"

    def test_bus_message_on_volume_change(self, ivi_simulator):
        """测试音量变化时发送总线消息"""
        ivi_simulator.set_volume(50)
        msg = ivi_simulator.get_last_bus_message()
        assert msg is not None
        assert msg["id"] == 0x100
        assert 50 in msg["data"]