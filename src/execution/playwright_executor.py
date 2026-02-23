from playwright.sync_api import sync_playwright
import traceback

from src.agent.selector_healer import heal_selector
from src.agent.dom_memory import capture_dom
from src.config.config_loader import config


HEADLESS = config["browser"]["headless"]
SLOW_MO = config["browser"]["slow_mo"]


class PlaywrightExecutor:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.page = None


    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )

        self.page = self.browser.new_page()


    def stop(self):

        try:
            if self.browser:
                self.browser.close()

            if self.playwright:
                self.playwright.stop()

        except:
            pass


    def navigate(self, url):

        print("[Executor] Navigating:", url)

        self.page.goto(url)

        self.page.wait_for_load_state("networkidle")


    def safe_fill(self, selector, value, name="unknown"):

        try:

            self.page.locator(selector).fill(value)

        except Exception:

            print(f"[Healer] Healing selector for {name}")

            new_selector = heal_selector(
                self.page,
                selector,
                name
            )

            print("[Healer] Using:", new_selector)

            self.page.locator(new_selector).fill(value)


    def safe_click(self, selector, name="unknown"):

        try:

            self.page.locator(selector).click()

        except Exception:

            print(f"[Healer] Healing selector for {name}")

            new_selector = heal_selector(
                self.page,
                selector,
                name
            )

            print("[Healer] Using:", new_selector)

            self.page.locator(new_selector).click()


    def capture(self, goal, error):

        capture_dom(self.page, goal, error)


    def current_url(self):

        return self.page.url


    def element_exists(self, selector):

        return self.page.locator(selector).count() > 0