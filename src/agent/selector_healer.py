import json
import os

from src.agent.llm_selector_healer import heal_selector_with_llm

MEMORY_FILE = "memory/selectors.json"


def load_selector_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE) as f:
        return json.load(f)


def save_selector(name, selector):

    data = load_selector_memory()

    data[name] = selector

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def heal_selector(page, failed_selector, element_name):

    print("[Healer] Attempting DOM + LLM healing")

    dom = page.content()

    new_selector = heal_selector_with_llm(
        dom,
        failed_selector,
        element_name
    )

    if new_selector:

        print("[Healer] LLM healed selector:", new_selector)

        save_selector(element_name, new_selector)

        return new_selector

    print("[Healer] Healing failed, using original")

    return failed_selector