from playwright.sync_api import sync_playwright
import traceback

from src.config.config_loader import config
from src.agent.dom_memory import capture_dom
from src.reporting.html_reporter import save_screenshot


BASE_URL = config["app"]["base_url"].rstrip("/")
REGISTER_URL = f"{BASE_URL}/register"

HEADLESS = bool(config["browser"].get("headless", True))
SLOW_MO = int(config["browser"].get("slow_mo", 0))

REGISTER_DATA = config["test_data"]["register"]

SELECTORS = {
    "name": "[data-test='register-name']",
    "email": "[data-test='register-email']",
    "password": "[data-test='register-password']",
    "submit": "[data-test='register-submit']",
    "success": "[data-test='register-success']",
    "error": "[data-test='register-error']",
}


def execute_register() -> dict:
    test_name = "register"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
            page = browser.new_page()

            try:
                print(f"[Executor] Navigating: {REGISTER_URL}")
                page.goto(REGISTER_URL, wait_until="domcontentloaded")
                page.wait_for_load_state("networkidle")

                page.locator(SELECTORS["name"]).fill(REGISTER_DATA["name"])
                page.locator(SELECTORS["email"]).fill(REGISTER_DATA["email"])
                page.locator(SELECTORS["password"]).fill(REGISTER_DATA["password"])
                page.locator(SELECTORS["submit"]).click()

                page.wait_for_timeout(800)

                # Success check
                if page.locator(SELECTORS["success"]).count() > 0:
                    capture_dom(page, "Register", "success")
                    save_screenshot(page, test_name, "passed")
                    print("[Executor] Register success")
                    return {"status": "passed", "error": None}

                err = None
                if page.locator(SELECTORS["error"]).count() > 0:
                    err = page.locator(SELECTORS["error"]).first.inner_text().strip()

                if not err:
                    err = "Register failed"

                capture_dom(page, "Register", err)
                shot = save_screenshot(page, test_name, "failed")

                print("[Executor] Register failed:", err)
                return {"status": "failed", "error": err, "screenshot": shot}

            finally:
                browser.close()

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "trace": traceback.format_exc(),
        }