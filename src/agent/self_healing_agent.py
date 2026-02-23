from src.execution.playwright_executor import execute_login_test
from src.healing.selector_healer import heal_selector


class SelfHealingAgent:

    def run(self):

        print("\nRunning test...")

        result = execute_login_test()

        if result["status"] == "passed":

            print("Test passed")

            return

        print("Test failed")

        print("Healing selector...")

        new_selector = heal_selector(
            result["error"],
            result["html"]
        )

        print("New selector:", new_selector)

        print("Retrying test...")

        result = execute_login_test({
            "email": new_selector,
            "password": "[data-test='login-password']",
            "submit": "[data-test='login-submit']"
        })

        print(result)