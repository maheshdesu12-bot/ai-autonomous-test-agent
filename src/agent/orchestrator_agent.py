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

            try:

                if name == "register":

                    print("[Orchestrator] Running register")

                    results[name] = self.register_agent.run()


                elif name == "login":

                    print("[Orchestrator] Running login")

                    results[name] = self.login_agent.run()


                else:

                    print(f"[Orchestrator] Unknown step: {name}")

                    results[name] = {
                        "status": "failed",
                        "error": "Unknown step"
                    }

            except Exception as e:

                print(f"[Orchestrator] Step failed: {name} → {e}")

                results[name] = {
                    "status": "failed",
                    "error": str(e)
                }


        generate_html_report(results)

        return results


if __name__ == "__main__":

    agent = OrchestratorAgent()

    result = agent.run()

    print(result)