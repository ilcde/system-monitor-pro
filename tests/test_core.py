import unittest
from core.system_info import SystemInfo

class TestSystemInfo(unittest.TestCase):
    def test_metrics_exist(self) -> None:
        info: SystemInfo = SystemInfo()
        metrics = info.get_system_metrics()
        self.assertIn("cpu_percent", metrics)
        self.assertIn("memory_percent", metrics)

if __name__ == '__main__':
    unittest.main()
