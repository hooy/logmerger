import sys
import re
from datetime import datetime

LOG_DATETIME_FORMAT = "%a %b %d %Y %H:%M:%S %z"
LOG_FORMAT_INPUT = (
    r"\[(?P<date>.+)\]\s\[(?P<level>.+)\]\s\[(?P<source>.+)\]\s(?P<message>.+)"
)
LOG_FORMAT_RE = re.compile(LOG_FORMAT_INPUT)
LOG_FORMAT_OUTPUT = "[{date}] [{level}] [{source}] {message}\n"

# log levels are ordered and higher level includes lower ones
LOG_LEVELS = ["info", "warning", "error", "critical"]
LOG_LEVEL_PRIORITY = {}
for i, ll in enumerate(LOG_LEVELS):
    LOG_LEVEL_PRIORITY.update({ll: LOG_LEVELS[i:]})


def log_entry(log_string: str):
    """Converts log entry string to object using LOG_FORMAT_INPUT"""
    log = re.search(LOG_FORMAT_RE, log_string)
    entry = False
    if log:
        entry = dict(log.groupdict())
        entry.update(
            {"date_object": datetime.strptime(entry["date"], LOG_DATETIME_FORMAT)}
        )

    return entry


def log_read_generator(file_name: str):
    """Opens file with given file_name and creates generator from
    that which yields line by line
    """
    with open(file_name, "r") as f:
        for line in f:
            entry = log_entry(line)
            if entry:
                yield entry


def get_next_entry(fh: dict, level: str):
    try:
        entry = next(fh["file_handler"])
        while (
            entry["level"] not in LOG_LEVEL_PRIORITY[level]
        ):  # find first entry with corresponding level
            entry = next(fh["file_handler"])
        fh["current_log_entry"] = entry
        return fh
    except StopIteration:  # EOF
        return None


def get_next_log_entry(file_handlers: list, level: str):
    """Takes earliest current entry from file_handlers,
    updates is, if file is ended removes handler
    """
    index, log = min(
        enumerate(file_handlers), key=lambda x: x[1]["current_log_entry"]["date_object"]
    )
    earliest = log.copy()  # save for return
    log = get_next_entry(log, level)
    if not log:  # need to delete fh
        del file_handlers[index]
    return earliest


def prepare_output(log_entry: dict):
    return LOG_FORMAT_OUTPUT.format(**log_entry)


def init_file_handlers(file_handlers: list, level: str):
    """Going through all the lines of each handler until we find
    log entry with corresponding level given; Will remove any handlers
    if file is empty or reached end of file without needed level found
    """
    inited_file_handlers = []
    for fh in file_handlers:
        next_entry = get_next_entry(fh, level)
        if next_entry:
            inited_file_handlers.append(next_entry)
    return inited_file_handlers


def parse_logs(files: list, level: str):
    file_handlers = []
    level = "info"
    for f in files:
        file_handlers.append(
            {
                "file_name": f,
                "file_handler": log_read_generator(f),
                "current_log_entry": None,
            }
        )
    file_handlers = init_file_handlers(file_handlers, level)
    while file_handlers:
        fh = get_next_log_entry(file_handlers, level)
        yield prepare_output(fh["current_log_entry"])


def main():
    files = [
        "log.txt",
        "log2.txt",
        "log3.txt",
        "log4.txt",
        "biglog1.txt",
        "biglog2.txt",
        "biglog3.txt",
    ]
    parse_logs(files, "info")


if __name__ == "__main__":
    main()
