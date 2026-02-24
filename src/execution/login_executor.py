import traceback

from src.config.config_loader import config
from src.db.mongo_client import users_collection
from src.agent.base_executor import BaseExecutor


BASE_URL = config["app"]["base_url"].rstrip("/")
LOGIN_URL = f"{BASE_URL}/login"

HEADLESS = bool(config["browser"].get("headless", True))
SLOW_MO = int(config["browser"].get("slow_mo", 0))


SELECTORS = {
    "email": "[data-test='login-email']",
    "password": "[data-test='login-password']",
    "submit": "[data-test='login-submit']",

    "success": "[data-test='login-success']",
    "error": "[data-test='login-error']",
}


executor = BaseExecutor(HEADLESS, SLOW_MO)


def validate_login_success(email, password, page):

    success_visible = page.locator(
        SELECTORS["success"]
    ).count() > 0

    error_visible = page.locator(
        SELECTORS["error"]
    ).count() > 0

    db_user = users_collection.find_one({
        "email": email,
        "password": password
    })

    if success_visible:
        return True

    if db_user and not error_visible:
        return True

    return False


def execute_login():

    users = executor.load_users("login")

    results = []

    def action(page):

        for user in users:

            email = user["email"]
            password = user["password"]

            try:

                print(f"[Executor] Login: {email}")

                page.goto(LOGIN_URL)

                page.locator(SELECTORS["email"]).fill(email)
                page.locator(SELECTORS["password"]).fill(password)

                page.locator(SELECTORS["submit"]).click()

                page.wait_for_timeout(1500)

                success = validate_login_success(
                    email,
                    password,
                    page
                )

                if success:

                    print("[Executor] Login SUCCESS")

                    results.append(
                        executor.handle_success(
                            page,
                            "login",
                            email
                        )
                    )

                else:

                    print("[Executor] Login FAILED")

                    results.append(
                        executor.handle_failure(
                            page,
                            "login",
                            email,
                            "Invalid credentials"
                        )
                    )

            except Exception as e:

                print(f"[Executor] Login exception: {e}")

                results.append(
                    executor.handle_failure(
                        page,
                        "login",
                        email,
                        str(e)
                    )
                )

        return results


    executor.run_browser(action)

    overall = (
        "passed"
        if all(r["status"] == "passed" for r in results)
        else "failed"
    )

    return {
        "status": overall,
        "results": results
    }