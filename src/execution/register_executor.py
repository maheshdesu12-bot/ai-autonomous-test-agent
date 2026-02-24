import traceback

from src.config.config_loader import config
from src.db.mongo_client import users_collection
from src.agent.base_executor import BaseExecutor


BASE_URL = config["app"]["base_url"].rstrip("/")
REGISTER_URL = f"{BASE_URL}/register"

HEADLESS = bool(config["browser"].get("headless", True))
SLOW_MO = int(config["browser"].get("slow_mo", 0))


SELECTORS = {
    "name": "[data-test='register-name']",
    "email": "[data-test='register-email']",
    "password": "[data-test='register-password']",
    "submit": "[data-test='register-submit']",
    "success": "[data-test='register-success']",
    "error": "[data-test='register-error']",
}


executor = BaseExecutor(HEADLESS, SLOW_MO)


def save_user_to_db(name, email, password):

    existing = users_collection.find_one({"email": email})

    if existing:
        print("[DB] User already exists")
        return False

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    print("[DB] User saved")

    return True


def execute_register():

    users = executor.load_users("register")

    results = []

    def action(page):

        for user in users:

            email = user["email"]

            try:

                print(f"[Executor] Register: {email}")

                page.goto(REGISTER_URL)

                page.locator(SELECTORS["name"]).fill(user["name"])
                page.locator(SELECTORS["email"]).fill(user["email"])
                page.locator(SELECTORS["password"]).fill(user["password"])

                page.locator(SELECTORS["submit"]).click()

                page.wait_for_timeout(1500)

                # Safe detection
                success_visible = page.locator(
                    SELECTORS["success"]
                ).count() > 0

                error_visible = page.locator(
                    SELECTORS["error"]
                ).count() > 0

                current_url = page.url.lower()

                print(f"[Executor] Current URL: {current_url}")


                # SUCCESS CONDITIONS
                if (
                    success_visible
                    or "login" in current_url
                    or "dashboard" in current_url
                ):

                    save_user_to_db(
                        user["name"],
                        user["email"],
                        user["password"]
                    )

                    print("[Executor] Register success")

                    results.append(
                        executor.handle_success(
                            page,
                            "register",
                            email
                        )
                    )


                # ERROR CONDITIONS
                elif error_visible:

                    error = page.locator(
                        SELECTORS["error"]
                    ).inner_text()

                    print(f"[Executor] Register failed: {error}")

                    results.append(
                        executor.handle_failure(
                            page,
                            "register",
                            email,
                            error
                        )
                    )


                # FALLBACK SAFE FAILURE
                else:

                    print(
                        f"[Executor] Register failed - Unknown state (URL: {current_url})"
                    )

                    results.append(
                        executor.handle_failure(
                            page,
                            "register",
                            email,
                            f"Unknown state - URL: {current_url}"
                        )
                    )


            except Exception as e:

                print(f"[Executor] Exception for {email}: {e}")

                results.append(
                    executor.handle_failure(
                        page,
                        "register",
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