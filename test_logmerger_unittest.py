import unittest
import logmerger
import datetime
import random
import string


class TestLogMerger(unittest.TestCase):
    LOG_ENTRY = "[Wed Oct 25 2012 14:32:52 +0200] [error] [client 127.0.0.1] client denied by server configuration: /export/home/live/test"

    def test_log_entry(self):
        self.assertTrue(logmerger.log_entry(self.LOG_ENTRY), "Should convert to dict")

    def test_file_generator(self):
        filename = "test.log"
        with open(filename, "w") as f:
            f.write(self.LOG_ENTRY)
        ll = list(logmerger.log_read_generator(filename))[0]
        self.assertDictEqual(logmerger.log_entry(self.LOG_ENTRY), ll)

    @staticmethod
    def prepare_file(file_name):
        start_date = datetime.datetime(2009, 10, random.randint(1, 20), 18, 00)
        date = start_date
        delta = datetime.timedelta(milliseconds=random.randint(100, 2000))
        entry_count = random.randint(10 ** 3, 10 ** 4)
        with open(file_name, "w") as f:
            for i in range(entry_count):
                date = date + delta
                data = {
                    "date": "{}+0200".format(
                        date.strftime(logmerger.LOG_DATETIME_FORMAT)
                    ),
                    "level": random.choice(logmerger.LOG_LEVELS),
                    "source": "client {}".format(
                        "".join(
                            random.choice(string.ascii_lowercase) for i in range(10)
                        )
                    ),
                    "message": "message {}".format(
                        "".join(
                            random.choice(string.ascii_lowercase) for i in range(10)
                        )
                    ),
                }
                f.write(logmerger.LOG_FORMAT_OUTPUT.format(**data))

    @staticmethod
    def prepare_files():
        files = ["log1.txt", "log2.txt", "log3.txt"]
        for f in files:
            TestLogMerger.prepare_file(f)
        return files

    def test_parsing_logs_sorted(self):
        files = TestLogMerger.prepare_files()
        level = "info"
        logs = logmerger.parse_logs(files, level)
        file_handlers = []
        for f in files:
            file_handlers.append(
                {
                    "file_name": f,
                    "file_handler": logmerger.log_read_generator(f),
                    "current_log_entry": None,
                }
            )
        file_handlers = logmerger.init_file_handlers(file_handlers, level)
        entries = []
        while file_handlers:
            entries += [logmerger.get_next_log_entry(file_handlers, level)]
        self.assertListEqual(
            entries,
            sorted(entries, key=lambda x: x["current_log_entry"]["date_object"]),
        )


if __name__ == "__main__":
    unittest.main()
