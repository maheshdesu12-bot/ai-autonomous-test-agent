from playwright.sync_api import sync_playwright
import traceback

from src.config.config_loader import config
from src.agent.dom_memory import capture_dom
from src.reporting.html_reporter import save_screenshot


BASE_URL = config["app"]["base_url"].rstrip("/")
LOGIN_URL = f"{BASE_URL}/login"

HEADLESS = bool(config["browser"].get("headless", True))
SLOW_MO = int(config["browser"].get("slow_mo", 0))

LOGIN_DATA = config["test_data"]["login"]

SELECTORS = {
    "email": "[data-test='login-email']",
    "password": "[data-test='login-password']",
    "submit": "[data-test='login-submit']",
    "error": "[data-test='login-error']",
}


def execute_login() -> dict:
    """
    Returns:
      {"status":"passed","error":None,"screenshot": "...optional..."}
      {"status":"failed","error":"...","trace":"...","screenshot":"...optional..."}
    """
    test_name = "login"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
            page = browser.new_page()

            try:
                print(f"[Executor] Navigating: {LOGIN_URL}")
                page.goto(LOGIN_URL, wait_until="domcontentloaded")
                page.wait_for_load_state("networkidle")

                page.locator(SELECTORS["email"]).fill(LOGIN_DATA["email"])
                page.locator(SELECTORS["password"]).fill(LOGIN_DATA["password"])
                page.locator(SELECTORS["submit"]).click()

                page.wait_for_timeout(800)

                # Success signal: server redirects OR some UI element (you can enhance later)
                if "dashboard" in page.url.lower():
                    capture_dom(page, "Login", "success")
                    save_screenshot(page, test_name, "passed")
                    print("[Executor] Login success")
                    return {"status": "passed", "error": None}

                # UI error message
                err = None
                err_loc = page.locator(SELECTORS["error"])
                if err_loc.count() > 0:
                    err = err_loc.first.inner_text().strip()

                if not err:
                    # Fallback: if your server returns JSON, your UI might not show error element.
                    err = "Unknown login failure"

                capture_dom(page, "Login", err)
                shot = save_screenshot(page, test_name, "failed")

                print("[Executor] Login failed:", err)
                return {"status": "failed", "error": err, "screenshot": shot}

            finally:
                # IMPORTANT: close browser while Playwright is still active (inside `with`)
                browser.close()

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "trace": traceback.format_exc(),
        }