import json
from pathlib import Path
from playwright.sync_api import sync_playwright

from src.reporting.html_reporter import save_screenshot
from src.agent.dom_memory import capture_dom


PROJECT_ROOT = Path(__file__).resolve().parents[2]
USERS_FILE = PROJECT_ROOT / "test_data" / "users.json"


class BaseExecutor:

    def __init__(self, headless=True, slow_mo=0):

        self.headless = headless
        self.slow_mo = slow_mo


    def load_users(self, section):

        if not USERS_FILE.exists():
            raise FileNotFoundError(f"Users file not found: {USERS_FILE}")

        with open(USERS_FILE, "r") as f:
            data = json.load(f)

        users = data.get(section, [])

        print(f"[Data] Loaded {len(users)} users for {section}")

        return users


    def run_browser(self, callback):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo
            )

            page = browser.new_page()

            try:
                return callback(page)

            finally:
                browser.close()


    def handle_success(self, page, test_name, user_id):

        capture_dom(page, test_name, "success")

        save_screenshot(
            page,
            f"{test_name}_{user_id}",
            "passed"
        )

        return {
            "status": "passed",
            "error": None
        }


    def handle_failure(self, page, test_name, user_id, error):

        capture_dom(page, test_name, "failed")

        save_screenshot(
            page,
            f"{test_name}_{user_id}",
            "failed"
        )

        return {
            "status": "failed",
            "error": error
        }