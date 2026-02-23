from concurrent.futures import ProcessPoolExecutor, as_completed

from src.execution.login_executor import execute_login
from src.execution.register_executor import execute_register


def run_parallel() -> dict:
    """
    Runs independent tests in parallel processes to avoid Playwright sync/thread issues.
    """
    tasks = {
        "login": execute_login,
        "register": execute_register,
    }

    results: dict = {}

    with ProcessPoolExecutor(max_workers=len(tasks)) as executor:
        futures = {executor.submit(fn): name for name, fn in tasks.items()}

        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception as e:
                results[name] = {"status": "failed", "error": str(e)}

    return results