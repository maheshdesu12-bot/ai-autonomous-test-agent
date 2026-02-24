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


def validate_user_from_db(email, password):

    user = users_collection.find_one({
        "email": email,
        "password": password
    })

    return user is not None


def execute_login():

    users = executor.load_users("login")

    results = []

    def action(page):

        for user in users:

            email = user["email"]

            try:

                print(f"[Executor] Login: {email}")

                page.goto(LOGIN_URL)

                page.locator(SELECTORS["email"]).fill(user["email"])
                page.locator(SELECTORS["password"]).fill(user["password"])

                page.locator(SELECTORS["submit"]).click()

                page.wait_for_timeout(1000)

                success_visible = page.locator(
                    SELECTORS["success"]
                ).count() > 0

                error_visible = page.locator(
                    SELECTORS["error"]
                ).count() > 0


                if success_visible:

                    valid = validate_user_from_db(
                        user["email"],
                        user["password"]
                    )

                    if valid:

                        print("[Executor] Login success")

                        results.append(
                            executor.handle_success(
                                page,
                                "login",
                                email
                            )
                        )

                    else:

                        print("[Executor] Login DB validation failed")

                        results.append(
                            executor.handle_failure(
                                page,
                                "login",
                                email,
                                "DB validation failed"
                            )
                        )


                elif error_visible:

                    error = page.locator(
                        SELECTORS["error"]
                    ).inner_text()

                    print(f"[Executor] Login failed: {error}")

                    results.append(
                        executor.handle_failure(
                            page,
                            "login",
                            email,
                            error
                        )
                    )


                else:

                    print("[Executor] Login unknown state")

                    results.append(
                        executor.handle_failure(
                            page,
                            "login",
                            email,
                            "Unknown state"
                        )
                    )

            except Exception as e:

                print(f"[Executor] Exception for {email}: {e}")

                results.append(
                    executor.handle_failure(
                        page,
                        "login",
                        email,
                        str(e)
                    )
                )

        return results


    try:

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

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e),
            "trace": traceback.format_exc()
        }