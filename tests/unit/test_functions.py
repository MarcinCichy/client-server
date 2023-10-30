import unittest
from unittest.mock import patch
import server_package.server_data as server_data
import server_package.server_response as server_response
from server_package.functions import SystemUtilities
from datetime import datetime, timedelta


class TestSystemUtilities(unittest.TestCase):

    def setUp(self):
        self.util = SystemUtilities()

    def test_uptime(self):
        mocked_time = datetime.now() - timedelta(hours=1, minutes=30)
        with patch.object(server_data, "START_TIME", new=mocked_time):
            result = self.util.uptime()
            self.assertEqual(result["uptime"], "1:30:00")

    def test_info(self):
        with patch.object(server_data, "VERSION", "1.0.0"):
            with patch.object(server_data, "DATE", "2023-01-01"):
                result = self.util.info()
                self.assertEqual(result, {"version": "1.0.0", "start_at": "2023-01-01"})

    def test_help_user(self):
        result = self.util.help(["user"])
        self.assertIn("uptime", result)
        self.assertIn("info", result)
        self.assertNotIn("stop", result)

    def test_help_admin(self):
        result = self.util.help(["admin"])
        self.assertIn("uptime", result)
        self.assertIn("info", result)
        self.assertIn("stop", result)

    def test_stop(self):
        result = self.util.stop()
        self.assertEqual(result, server_response.CONNECTION_CLOSE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
