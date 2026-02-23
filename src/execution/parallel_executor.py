from concurrent.futures import ThreadPoolExecutor
from src.execution.login_executor import execute_login
from src.execution.register_executor import execute_register


def run_parallel_tests():

    with ThreadPoolExecutor(max_workers=2) as executor:

        futures = {

            "login": executor.submit(execute_login),
            "register": executor.submit(execute_register)
        }

        results = {}

        for name, future in futures.items():

            results[name] = future.result()

    return results