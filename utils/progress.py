import sys
import time

class ProgressBar:
    def __init__(self, total=None, desc="Generating"):
        self.total = total
        self.desc = desc
        self.start_time = time.time()
        self.count = 0
    
    def update(self, n=1):
        self.count += n
        if self.count % 1000 == 0:
            self._print()

    def _print(self):
        elapsed = time.time() - self.start_time
        rate = self.count / elapsed if elapsed > 0 else 0
        sys.stderr.write(f"\r{self.desc}: {self.count} words | {rate:.0f} w/s")
        sys.stderr.flush()

    def close(self):
        sys.stderr.write("\n")
        sys.stderr.flush()
