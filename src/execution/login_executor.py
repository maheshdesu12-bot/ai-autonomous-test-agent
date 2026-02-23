from playwright.sync_api import sync_playwright
import traceback

from src.agent.selector_healer import heal_selector
from src.agent.dom_memory import capture_dom
from src.config.config_loader import config


BASE_URL = config["app"]["base_url"]
LOGIN_URL = f"{BASE_URL}/login"

HEADLESS = config["browser"]["headless"]
SLOW_MO = config["browser"]["slow_mo"]

LOGIN_DATA = config["test_data"]["login"]


SELECTORS = {
    "email": "[data-test='login-email']",
    "password": "[data-test='login-password']",
    "submit": "[data-test='login-submit']"
}


def safe_fill(page, field, value):

    try:
        page.locator(SELECTORS[field]).fill(value)

    except Exception:

        print(f"[Healer] Healing selector for {field}")

        healed = heal_selector(page, SELECTORS[field], field)

        SELECTORS[field] = healed

        page.locator(healed).fill(value)


def safe_click(page, field):

    try:
        page.locator(SELECTORS[field]).click()

    except Exception:

        healed = heal_selector(page, SELECTORS[field], field)

        SELECTORS[field] = healed

        page.locator(healed).click()


def execute_login():

    goal = "User login"

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=HEADLESS,
                slow_mo=SLOW_MO
            )

            page = browser.new_page()

            print("[Executor] Navigating:", LOGIN_URL)

            page.goto(LOGIN_URL)

            page.wait_for_load_state("networkidle")

            safe_fill(page, "email", LOGIN_DATA["email"])
            safe_fill(page, "password", LOGIN_DATA["password"])

            safe_click(page, "submit")

            page.wait_for_timeout(2000)

            current_url = page.url

            if "dashboard" in current_url.lower():

                print("[Executor] Login success")

                capture_dom(page, goal, "success")

                browser.close()

                return {
                    "status": "passed",
                    "error": None
                }

            error_element = page.locator("[data-test='login-error']")

            if error_element.count() > 0:

                error_text = error_element.inner_text()

                print("[Executor] Login failed:", error_text)

                capture_dom(page, goal, error_text)

                browser.close()

                return {
                    "status": "failed",
                    "error": error_text
                }

            print("[Executor] Unknown login failure")

            capture_dom(page, goal, "unknown failure")

            browser.close()

            return {
                "status": "failed",
                "error": "Unknown failure"
            }

    except Exception as e:

        print("[Executor] Login exception:", str(e))

        try:
            capture_dom(page, goal, str(e))
        except:
            pass

        return {
            "status": "failed",
            "error": str(e),
            "trace": traceback.format_exc()
        }