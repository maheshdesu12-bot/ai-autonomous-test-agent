from src.agent.login_agent import LoginAgent
from src.agent.register_agent import RegisterAgent
from src.agent.planner_agent import PlannerAgent
from src.reporting.html_reporter import generate_html_report


class OrchestratorAgent:

    def __init__(self):

        self.login_agent = LoginAgent()
        self.register_agent = RegisterAgent()
        self.planner = PlannerAgent()

    def run(self):

        print("\n[Orchestrator] Starting autonomous execution")

        plan = self.planner.create_plan()

        results = {}

        for step in plan:

            name = step["name"]

            if step["depends_on"]:

                dep = step["depends_on"]

                if results[dep]["status"] != "passed":

                    print(f"[Orchestrator] Skipping {name}")
                    results[name] = {
                        "status": "skipped"
                    }
                    continue

            if name == "register":

                results[name] = self.register_agent.run()

            elif name == "login":

                results[name] = self.login_agent.run()

        generate_html_report(results)

        return results


if __name__ == "__main__":

    agent = OrchestratorAgent()

    result = agent.run()

    print(result)