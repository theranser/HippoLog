import os
import datetime

class HippoLog():
    def __init__(self, layer="DEBUG", log_depth=10):
        self.layer = layer
        self.log_depth = log_depth
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(SCRIPT_DIR, "logs")

        if not os.path.exists(logs_dir):
            os.mkdir(logs_dir)

        oldest_log = os.path.join(logs_dir, f"log{log_depth}.txt")
        if os.path.exists(oldest_log):
            os.remove(oldest_log)

        for i in range(log_depth - 1, 0, -1):
            src = os.path.join(logs_dir, f"log{i}.txt")
            dst = os.path.join(logs_dir, f"log{i + 1}.txt")
            if os.path.exists(src):
                os.rename(src, dst)

        latest_log = os.path.join(logs_dir, "latest.txt")
        first_log = os.path.join(logs_dir, "log1.txt")
        if os.path.exists(latest_log):
            os.rename(latest_log, first_log)

    def log(self, level, message):
        now = datetime.datetime.now()
        timestamp = now.strftime("%I:%M:%S:%f")[:-3] + " " + ("AM" if now.hour < 12 else "PM")
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "latest.txt")
        with open(log_path, "a") as f:
            f.write(f"{timestamp} - {level} - {message}\n")

    def debug(self, message):
        if self.layer == "DEBUG":
            self.log("DEBUG", message)

    def info(self, message):
        if self.layer in ("INFO", "DEBUG"):
            self.log("INFO", message)

    def warning(self, message):
        if self.layer in ("INFO", "DEBUG", "WARNING"):
            self.log("WARNING", message)

    def error(self, message):
        if self.layer in ("INFO", "DEBUG", "WARNING", "ERROR"):
            self.log("ERROR", message)
