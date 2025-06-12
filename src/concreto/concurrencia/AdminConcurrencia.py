from concurrent.futures import ProcessPoolExecutor
from threading import Lock

class AdminConcurrencia:
    _instance = None
    _lock = Lock()

    def __init__(self, max_workers=4):
        self._executor = ProcessPoolExecutor(max_workers=max_workers)

    @classmethod
    def get_instance(cls, max_workers=4):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(max_workers)
        return cls._instance

    def submit(self, func, *args, **kwargs):
        return self._executor.submit(func, *args, **kwargs)

    def map(self, func, iterable):
        return self._executor.map(func, iterable)

    def shutdown(self, wait=True):
        self._executor.shutdown(wait=wait)