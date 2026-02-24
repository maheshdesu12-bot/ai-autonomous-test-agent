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

    # optional UI selectors
    "success": "[data-test='register-success']",
    "error": "[data-test='register-error']",
}


executor = BaseExecutor(HEADLESS, SLOW_MO)


# --------------------------------------------------
# Optional memory storage ONLY (not validation)
# --------------------------------------------------

def save_user_to_memory(name, email, password):

    existing = users_collection.find_one({"email": email})

    if existing:
        return False

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    return True


# --------------------------------------------------
# Main executor
# --------------------------------------------------

def execute_register():

    users = executor.load_users("register")

    results = []

    def action(page):

        for user in users:

            name = user["name"]
            email = user["email"]
            password = user["password"]

            try:

                print(f"[Executor] Register: {email}")

                # Capture BEFORE state
                existed_before = users_collection.find_one({
                    "email": email
                })

                page.goto(REGISTER_URL)

                page.locator(SELECTORS["name"]).fill(name)
                page.locator(SELECTORS["email"]).fill(email)
                page.locator(SELECTORS["password"]).fill(password)

                page.locator(SELECTORS["submit"]).click()

                page.wait_for_timeout(1500)

                print(f"[Executor] URL after register: {page.url}")

                # Capture AFTER state
                existed_after = users_collection.find_one({
                    "email": email
                })

                success_visible = page.locator(
                    SELECTORS["success"]
                ).count() > 0

                error_visible = page.locator(
                    SELECTORS["error"]
                ).count() > 0

                page_content = page.content().lower()

                # -----------------------------------------
                # SUCCESS CRITERIA
                # -----------------------------------------

                success = False

                # Case 1: DB state changed (most reliable)
                if not existed_before and existed_after:
                    success = True

                # Case 2: UI success selector visible
                elif success_visible:
                    success = True

                # Case 3: success message visible
                elif (
                    "registration successful" in page_content
                    or "registered successfully" in page_content
                    or "account created" in page_content
                    or "user created" in page_content
                ):
                    success = True

                # Case 4: error visible
                elif error_visible:
                    success = False

                # -----------------------------------------
                # RESULT HANDLING
                # -----------------------------------------

                if success:

                    save_user_to_memory(
                        name,
                        email,
                        password
                    )

                    print("[Executor] Register SUCCESS")

                    results.append(
                        executor.handle_success(
                            page,
                            "register",
                            email
                        )
                    )

                else:

                    print("[Executor] Register FAILED")

                    results.append(
                        executor.handle_failure(
                            page,
                            "register",
                            email,
                            "Registration failed or user already exists"
                        )
                    )

            except Exception as e:

                print(f"[Executor] Exception during register: {e}")

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