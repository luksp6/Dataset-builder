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

    def collect(self, callables: list[tuple[callable, tuple]]) -> list:
        """
        Ejecuta una lista de tareas concurrentes con sus argumentos.
        callables: lista de tuplas (func, args_tuple)
        Devuelve una lista con los resultados exitosos (los que no lanzaron excepción).
        """
        futures = [self.submit(func, *args) for func, args in callables]
        results = []
        for future in futures:
            try:
                result = future.result()
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"⚠️ Error en tarea concurrente: {e}")
        return results