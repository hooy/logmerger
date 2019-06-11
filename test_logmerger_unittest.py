import unittest
import logmerger
import datetime


class TestLogMerger(unittest.TestCase):
    def test_log_entry(self):
        self.assertTrue(
            logmerger.log_entry(
                "[Wed Oct 25 2012 14:32:52 +0200] [error] [client 127.0.0.1] client denied by server configuration: /export/home/live/test"
            ),
            "Should convert to dict",
        )

    def test_proper_output(self):
        self.assertRegex(
            logmerger.prepare_output(
                {
                    "date": "Wed Oct 25 2012 14:32:52 +0200",
                    "level": "error",
                    "source": "client 127.0.0.1",
                    "message": "client denied by server configuration: /export/home/live/test",
                    "date_object": datetime.datetime(
                        2012,
                        10,
                        25,
                        14,
                        32,
                        52,
                        tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                    ),
                }
            ),
            logmerger.LOG_FORMAT_RE,
            "Log entry dict should properly map to log format regex",
        )

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")


if __name__ == "__main__":
    unittest.main()
