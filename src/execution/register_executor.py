from playwright.sync_api import sync_playwright
import traceback

from src.agent.selector_healer import heal_selector
from src.agent.dom_memory import capture_dom
from src.config.config_loader import config


BASE_URL = config["app"]["base_url"]
REGISTER_URL = f"{BASE_URL}/register"

HEADLESS = config["browser"]["headless"]
SLOW_MO = config["browser"]["slow_mo"]

REGISTER_DATA = config["test_data"]["register"]


SELECTORS = {
    "name": "[data-test='register-name']",
    "email": "[data-test='register-email']",
    "password": "[data-test='register-password']",
    "submit": "[data-test='register-submit']"
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


def execute_register():

    goal = "User registration"

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=HEADLESS,
                slow_mo=SLOW_MO
            )

            page = browser.new_page()

            print("[Executor] Navigating:", REGISTER_URL)

            page.goto(REGISTER_URL)

            page.wait_for_load_state("networkidle")

            # FIX: use correct config keys
            safe_fill(page, "name", REGISTER_DATA["name"])
            safe_fill(page, "email", REGISTER_DATA["email"])
            safe_fill(page, "password", REGISTER_DATA["password"])

            safe_click(page, "submit")

            page.wait_for_timeout(2000)

            print("[Executor] Register success")

            capture_dom(page, goal, "success")

            browser.close()

            return {
                "status": "passed",
                "error": None
            }

    except Exception as e:

        print("[Executor] Register failed:", str(e))

        try:
            capture_dom(page, goal, str(e))
        except:
            pass

        return {
            "status": "failed",
            "error": str(e),
            "trace": traceback.format_exc()
        }